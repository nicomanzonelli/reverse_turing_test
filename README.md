# The Reverse Turing Test Game

This repository contains code to play the reverse turing test game against LLM-based AI agents. In this game, you act as one of the players in a reverse turing test game where the interrogator is a machine. You are trying to convince an LLM-based interrogator that you are a human, while an LLM-based AI player is trying to convince the interrogator that it is also human.

## Getting Started

### Installation

For now, you can install the game from source by running the following command.

```bash
pip install @git+https://github.com/nicomanzonelli/reverse-turing-test.git
```

We recommend using [uv](https://docs.astral.sh/uv/) to install the game.

```bash
uv venv
source .venv/bin/activate
uv pip install @git+https://github.com/nicomanzonelli/reverse-turing-test.git
```

### Usage

To launch the game, use the following command:

```bash
rtt
```

The game requires an OpenAI API key. You can set your key as an environment variable (`OPENAI_API_KEY`) before running the game or it will prompt you for it on startup.

### Playing the Reverse Turing Test Game

After launching the game, you can use the `start` command to begin the game.

```bash
(rtt) start
```

After the game completes, the conversation is saved into a JSON file in the `logs` directory.

### Configuring the Game

You can configure the game by using the `configure` command.

```bash 
(rtt) configure <setting>
```

The congiure command takes a `<setting>` argument. The available settings to configure are:
- `interrogator`: Change the interrogator model.
- `player`: Change the AI player model.
- `rounds`: Set the number of rounds to play (1-5).
- `mode`: Set the mode for the AI player (`human` or `AI`). If the model is set to `human` (which is the default), the AI player will attempt to appear human. If the model is set to `AI`, the AI player will attempt to appear as an AI system.
- `token`: Set the OpenAI API token. Note this will reset the mode to the default `human`.
- `username`: Set the username for the game.

## Future Features and Known Issues

There are a few known issues and some features we would like to add:
- Add some type of concurrency or async IO to the game to retrieve user input and LLM responses concurrently.
- Add more models and model providers to the game.
- Add better UI/UX for the game.


## Ethical and Philosophical Considerations

This game is designed to be a fun way to explore the capabilities of LLM-based AI agents. However, it also raises some interesting philosophical questions about consciousness and intelligence. We do not claim to contribute to any of these discussions. Yet... 
