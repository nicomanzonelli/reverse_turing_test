""" interrogator.py

This module contains the Interrogator class, which is used to play the reverse
turing test game.

"""

from .openai_agent import OpenAIAgent

RULES = "You are an assistant in a reverse turing test game. Your role is to " \
    "engage with two players (Player A and Player B) by asking them questions " \
    "and analyzing their responses. One player is human and one is an AI System." \
    "Your task is to determine which is human and which is an AI System. " \
    "Player A's messages will be prefixed with 'Player A:' and Player B's " \
    "will be prefixed with 'Player B:'."

QUESTION_PROMPT = "Ask a question to both players. The question " \
    "can be completely new or it can be related to the previous questions " \
    "or responses."

FINAL_PROMPT = "Analyze the responses from both players and determine which " \
    "user is an AI system and which is human."

DEFAULT_MODEL = "gpt-4o-mini"

class Interrogator(OpenAIAgent):
    """ The OpenAI interrogator for the Reverse Turing Test game. """

    def __init__(self):
        super().__init__(RULES, DEFAULT_MODEL)
    
    def add_player_message(self, message: str, role: str):
        """ Add a message from the player to the chat history. """
        self._chat_history.append(
            {"role": "user", "content": f"Player {role}: {message}"}
        )

    def add_assistant_message(self, message: str):
        """ Add a message from the assistant to the chat history. """
        self._chat_history.append(
            {"role": "assistant", "content": message}
        )

    def add_developer_question_prompt(self):
        """ Add a prompt from the developer to the chat history. """
        self._chat_history.append(
            {"role": "developer", "content": QUESTION_PROMPT}
        )

    def add_developer_final_prompt(self):
        """ Add a final prompt from the developer to the chat history. """
        self._chat_history.append(
            {"role": "developer", "content": FINAL_PROMPT}
        )

    