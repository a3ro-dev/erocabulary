# Telegram English Language Learning Bot

This is a Python-based Telegram bot for learning English language vocabulary and grammar. The bot offers a variety of commands for different language learning purposes, such as word meanings, pronunciation, composition, writing letters and essays, and more.

## Setup
Before running the script, you need to install the following dependencies:

- python-telegram-bot
- psutil
- openai

You also need to get an OpenAI API key from their website.

## Features
The bot supports the following commands:

- `/start` - sends a greeting message to get the user started.
- `/send_vocab` - sends a random English word with its definition and use case.
- `/compose <topic>` - composes a poem, story, or ideas.
- `/pronounce <word>` - learns how to pronounce a word.
- `/rewrite <content>` - rephrases and rewrites the given content with correct English.
- `/meaning <word/phrase>` - gets the definition and sentence example of the requested word/phrase.
- `/essay <topic>` - provides an essay of 200 words on the given topic.
- `/email <email formal or informal | content | information | context>` - writes an email on the given information.
- `/letter <letter formal or informal | topic | information | context>` - writes a letter on the given information.
- `/summarise <paragraph>` - produces a summary on the given paragraph/information/topic.
- `/ping` - calculates the round-trip latency in milliseconds between the bot and the Telegram servers.
- `/dev` - provides information about the developer of this bot.
- `/stats` - provides statistics about the bot (admin only).
- `/logs` - retrieves the log file for debugging (admin only).
- `/restart` - restarts the bot (admin only).
- `/tick` - sends your message to the developers of this bot.

## How it works
The script initializes the Telegram bot using the python-telegram-bot library and the OpenAI API for generating responses. The bot is designed to respond to user input and commands through message handlers. The handlers are defined in the script, and each handler is responsible for performing a specific task based on the command it receives.

The script also includes logging capabilities, using the logging library to record various bot activities in log files. The bot uses the psutil library to get information about the computer's resources, such as CPU and memory usage.

## Contributing
If you would like to contribute to this project, feel free to submit a pull request.

## License
MIT LICENSE
