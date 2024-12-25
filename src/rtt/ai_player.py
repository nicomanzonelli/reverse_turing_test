""" ai_player.py

This module contains the AIPlayer class, which is used to play the reverse
turing test game against the interrogator.

"""

from .openai_agent import OpenAIAgent

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_MODE = "human"

class AIPlayer(OpenAIAgent):
    """ The AI player in the reverse turing test game. """

    def __init__(self, mode: str = DEFAULT_MODE):
        self._mode = mode
        rules = "You are a player in a reverse turing test game. Your goal is " \
            f"to convince the user that you are an {mode} by responding to " \
            "the user's questions."
        super().__init__(rules, DEFAULT_MODEL)

    @property
    def mode(self):
        """ Get the mode of the AI player. """
        return self._mode

    def add_interrogator_message(self, message: str):
        """ Add a message from the interrogator to the chat history. """
        self._chat_history.append(
            {"role": "user", "content": message}
        )

    def add_player_message(self, message: str):
        """ Add a message from the player to the chat history. """
        self._chat_history.append(
            {"role": "assistant", "content": message}
        )
