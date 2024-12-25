""" openai_agent.py

This module contains the OpenAIAgent class, which is used to interact with
the OpenAI API.

"""

from openai import OpenAI, OpenAIError, AuthenticationError

class OpenAIAgent:
    """ A generic OpenAI agent for the Reverse Turing Test game. 
    
    Attributes:
        _client (OpenAI): The OpenAI client.
        _models (list[str]): The list of available models.
        _chat_history (list[dict]): The chat history.
    """

    def __init__(self, developer_prompt: str, model: str):
        """ Initialize the OpenAIAgent. 
        
        Args:
            developer_prompt (str): The developer prompt.
        """
        self._client = OpenAI()
        self._model = model

        self._models = [
            "gpt-4o",
            "gpt-4o-mini",
            "o1-mini",
            "o1-preview",
            "gpt-3.5-turbo"
        ]

        self._chat_history = [
            {"role": "developer", "content": developer_prompt}
        ]

    @property
    def model(self):
        """ Get the model. """
        return self._model
    
    @model.setter
    def model(self, model: str):
        """ Set the model. """
        self._model = model

    @property
    def models(self):
        """ Get the list of available models. """
        return self._models
    
    @models.setter
    def models(self, models):
        """ Set the list of available models. """
        raise NotImplementedError("Setting models is not supported")
    
    def reset_conversation(self):
        """ Reset the chat history. """
        self._chat_history = [self._chat_history[0]]
    
    def get_response(self, temperature: float = 1.0) -> str:
        """ Get a response from the OpenAI API. 
        
        Args:
            model (str): The model to use.
            temperature (float): The temperature to use.

        Returns:
            str: The response from the OpenAI API.
        """
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=self._chat_history,
                temperature=temperature
            )
            return response.choices[0].message.content

        except OpenAIError as err:
            print(f"{err.message}\n")
            return None
        
        except AuthenticationError as err:
            print(f"{err.message}\n")
            return None
