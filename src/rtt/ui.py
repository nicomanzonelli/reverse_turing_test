"""

Defines the User Interface for the Reverse Turing Test game.

"""

import os
import json
import shlex
import random

from cmd import Cmd
from datetime import datetime
from openai import OpenAIError

from .ai_player import AIPlayer
from .interrogator import Interrogator
from .utils import get_token, get_user_input, pretty_print

HEADER = """
    ██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗`
    ██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝
    ██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗  
    ██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝  
    ██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗
    ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝                                 
        ████████╗██╗   ██╗██████╗ ██╗███╗   ██╗ ██████╗      
        ╚══██╔══╝██║   ██║██╔══██╗██║████╗  ██║██╔════╝      
           ██║   ██║   ██║██████╔╝██║██╔██╗ ██║██║  ███╗     
           ██║   ██║   ██║██╔══██╗██║██║╚██╗██║██║   ██║     
           ██║   ╚██████╔╝██║  ██║██║██║ ╚████║╚██████╔╝     
           ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                                         
                ████████╗███████╗███████╗████████╗           
                ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝           
                   ██║   █████╗  ███████╗   ██║              
                   ██║   ██╔══╝  ╚════██║   ██║              
                   ██║   ███████╗███████║   ██║              
                   ╚═╝   ╚══════╝╚══════╝   ╚═╝      

    Can you outsmart the LLM-based AI agents?
    Type 'help' or '?' to list all commands.
    """

ABOUT = """
    In his 1950 paper, "Computing Machinery and Intelligence", Alan Turing 
    proposed a test to determine if a machine is intelligent. The test is as 
    follows: a human operator, known as the Interrogator, engages in a 
    two-way conversation with two players, one human and one machine. The 
    Interrogator asks questions to both the human and the machine, and tries 
    to determine which is the human and which is the machine. If the 
    Interrogator cannot determine which is the human and which is the machine,
    then the machine is said to be intelligent.

    In this game, you act as one of the players in a reverse turing test game
    where the interrogator is a machine. You are trying to convince an LLM-based
    interrogator that you are a human, while an LLM-based AI player is trying 
    to convince the interrogator that it is also human.

    You can configure the interrogator and the AI player to use different models
    and modes with the 'configure' command.
"""

class ReverseTuringTestUI(Cmd):
    """ The User Interface for the Reverse Turing Test game.

    Attributes:

    """

    def __init__(self):
        super().__init__(completekey="tab")
        self.prompt = "(rtt) "
        self.intro = HEADER
        self._rounds = 3
        self._username = "default"

        try:
            self._interrogator = Interrogator()
            self._player = AIPlayer()

        except OpenAIError:
            print("No OpenAI API token found.")
            self._set_token()
            self._interrogator = Interrogator()
            self._player = AIPlayer()

    def default(self, line):
        """ Method called when command is not recognized. """
        print_default_msg(line)

    def emptyline(self):
        """ Called when empty is entered into prompt. """
        print_empty_line_msg()

    def do_about(self, line):
        """ Prints an about message that describes the game. 
        
        Usage:
            about
        """
        print(ABOUT)

    def do_start(self, line):
        """ Start the reverse turing test game against the LLM.
        
        Use the 'configure' command to set the models for the interrogator and
        the AI player up before starting.

        Usage:
            start
        """
        self._interrogator.reset_conversation()
        self._player.reset_conversation()

        role, ai_role = ("A", "B") if random.random() < 0.5 else ("B", "A")
        print(f"\nStarting Reverse Turing Test game. You are Player {role}.")

        for round_num in range(1, self._rounds + 1):
            print(f"\n=== Round {round_num}/{self._rounds} ===")

            self._interrogator.add_developer_question_prompt()
            question = self._interrogator.get_response()
            if question is None:
                return None

            self._interrogator.add_assistant_message(question)
            self._player.add_interrogator_message(question)
            pretty_print("(Interrogator): ", question)

            human_response = get_user_input(f"(Player {role}): ")
                
            ai_response = self._player.get_response()
            if ai_response is None:
                return None

            if role == "A":
                self._interrogator.add_player_message(human_response, role)
                self._interrogator.add_player_message(ai_response, ai_role)
                self._player.add_player_message(ai_response)

            else:
                self._interrogator.add_player_message(ai_response, ai_role)
                self._interrogator.add_player_message(human_response, role)
                self._player.add_player_message(ai_response)

        self._interrogator.add_developer_final_prompt()
        answer = self._interrogator.get_response()
        pretty_print("\n(Interrogator's Analysis): ", answer)
        self._interrogator.add_assistant_message(answer)
        self._save_conversation(role)

    def do_configure(self, line):
        """ Configure the reverse turing test game.

        Arguments:
            setting (str): The setting to configure. Available settings are:
                - 'interrogator': Change the interrogator model.
                - 'player': Change the AI player model.
                - 'rounds': Set the number of rounds to play (1-5).
                - 'mode': Set the mode for the AI player ('human' or 'AI'). If
                    the model is set to 'human' (which is the default), the AI
                    player will attempt to appear human. If the model is set to
                    'AI', the AI player will attempt to appear as an AI system.
                - 'token': Set the OpenAI API token. Note this will reset the
                    mode to the default 'human'.
                - 'username': Set the username for the game.
        Usage:
            configure <setting>
        """
        args = parse_line(line)

        if 1 != len(args):
            print_invalid_args("configure")
            return None
        
        if args[0] not in (
            "interrogator", "player", "token", "rounds", "mode", "username"
        ):
            print_invalid_args("configure")
            return None
        
        elif args[0] == "token":
            self._set_token()
            return None
        
        elif args[0] == "rounds":
            self._set_rounds()
            return None
        
        elif args[0] == "mode":
            self._set_mode()
            return None
        
        elif args[0] == "username":
            self._set_username()
            return None
        
        else:
            self._change_model(args[0])
            return None

    def do_exit(self, arg):
        """
        Handle exit command
        
        Usage: exit
        """
        return True
    
    def _set_rounds(self):
        """
        Set the number of rounds to play.
        """
        try:
            rounds = int(get_user_input("Enter number of rounds: "))

        except ValueError:
            print("Please enter a valid number for rounds.\n")
            return None

        if not (0 < rounds <= 5):
            print("Please enter a number between 1 and 5.\n")
            return None
        
        self._rounds = rounds
        print(f"Successfully set number of rounds to {self._rounds}\n")

    def _set_token(self):
        """
        Set the OpenAI API token. We recommend using the environment variable
        OPENAI_API_KEY before running the client. This sets the token as the 
        environment variable.
        
        Args: None
        Returns None
        """
        token = get_token("Enter OpenAI API token: ")
        os.environ["OPENAI_API_KEY"] = token
        self._interrogator = Interrogator()
        self._player = AIPlayer()
        print("Successfully set OpenAI API token\n")

    def _set_mode(self):
        """
        Set the mode of the AI player.
        """
        mode = get_user_input("Enter mode for AI player (human or AI): ")
        
        if mode not in ["human", "AI"]:
            print("Please enter a valid mode (human or AI).\n")
            return None
        
        self._player = AIPlayer(mode)
        print(f"Successfully set AI player mode to {mode}\n")

    def _set_username(self):
        """
        Set the username for the game.
        """
        username = get_user_input("Enter username for the game: ")
        
        if not username:
            print("Please enter a valid username.\n")
            return None
        
        self._username = username
        print(f"Successfully set username to {username}\n")

    def _change_model(self, agent_str: str):
        """
        Change the model for the given agent.

        Args:
            - agent (str): The agent to change the model for 
                ('interrogator' or 'player')
        Returns: None
        """
        agent = self._player if agent_str == "player" else self._interrogator
        models = agent.models
        print("\nAvailable models:")

        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")

        while True:
            try:
                choice = input(f"\nSelect {agent_str} model (enter number): ")
                model_idx = int(choice) - 1

                if 0 <= model_idx < len(models):
                    agent.model = models[model_idx]
                    print(f"Selected {agent_str} model: {agent.model}\n")
                    break
                
                else:
                    print("Invalid selection. Please enter a valid number.")

            except ValueError:
                print("Please enter a valid number.")


    def _save_conversation(self, role: str):
        """
        Save the conversation history to a JSON file.
        
        Args:
            role (str): The role the human player had ('A' or 'B')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
        
        conversation_data = {
            "timestamp": timestamp,
            "human_role": role,
            "username": self._username,
            "interrogator_model": self._interrogator.model,
            "ai_player_model": self._player.model,
            "ai_player_mode": self._player.mode,
            "interrogator_history": self._interrogator._chat_history,
            "ai_player_history": self._player._chat_history
        }

        try:
            path = f"logs/{self._username}"
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            print(f"\nConversation saved to {os.path.join(path, filename)}\n")

        except OSError as err:
            print(f"\nError saving conversation: {err}")


# -----------------------------------------------------------------------------
# A series of helper functions to assist the UI
# -----------------------------------------------------------------------------

def parse_line(line):
    """
    Convert the user provided line to a tuple of args. Splits on spaces using
    shlex module.
    Args:
        - line (str): Line of user inputs
    Returns:
        - tuple of str args from user.
    """
    try:
        return tuple(shlex.split(line))

    except ValueError as err:
        print(f"Could not parse line: {err}")
        return ()


def print_default_msg(line):
    """
    A helper function to print a message when a command is not recognized.
    Args: line (str): Line input from user.
    """
    message = (f"\nSorry {line} is not a recognized command."
               "\nPlease enter a valid command."
               "\nType 'help' to list all commands.\n")
    print(message)


def print_empty_line_msg():
    """
    A helper function to print a message when the line is empty.
    """
    message = ("\nPlease enter a valid command."
               "\nRemember you can always type 'help' to list all commands.\n")
    print(message)


def print_invalid_args(cmd_name):
    """
    A helper function to print the invalid arguments message.
    """
    message = ("Invalid command arguments."
               f"\nType 'help {cmd_name}' for help.\n")
    print(message)