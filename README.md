# Erocabulary

This is a Python-based Telegram bot for learning English language vocabulary and grammar. The bot offers a variety of commands for different language learning purposes, such as word meanings, pronunciation, composition, writing letters and essays, and more.

## Setup
Before running the script, you need to install the following dependencies:

- python-telegram-bot
- psutil
- grok

You also need to have a grok api key

## Features
The bot supports the following commands:

⭐ `/start` - Sends a greeting message.<br>
📚 `/send_vocab` - Improves your vocabulary by sending a random English word with its definition and use case.<br>
📝 `/compose` topic - Composes a poem, story, or ideas.<br>
🗣️ `/pronounce` word - Learn to pronounce a word.<br>
✍🏻 `/rewrite` content - Rephrases and rewrites the given content with correct English.<br>
📖 `/meaning` word/phrase - Provides the definition and sentence example of the requested word/phrase.<br>
📝 `/essay` topic - Provides an essay on the given topic.<br>
📧 `/email` details - Writes an email on the given information.<br>
✉ `/letter` details - Writes a letter on the given information.<br>
🔤 `/summarise` paragraph - Produces a summary of the given paragraph or topic.<br>
🌐 `/ping` - Shows the round-trip latency in milliseconds between this bot and Telegram servers.<br>
ℹ `/dev` - Information regarding the developer of this bot.<br>

## How it works
The script initializes the Telegram bot using the python-telegram-bot library and uses a Large Language Model at it's core for generating responses. The bot is designed to respond to user input and commands through message handlers. The handlers are defined in the script, and each handler is responsible for performing a specific task based on the command it receives.

The script also includes logging capabilities, using the logging library to record various bot activities in log files. The bot uses the psutil library to get information about the computer's resources, such as CPU and memory usage.

## Contributing
If you would like to contribute to this project, feel free to submit a pull request.

## License
MIT LICENSE
