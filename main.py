import logging
import time
import os
import sys
import psutil
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from utils import cleaner
from utils.ai import Ai
import asyncio

class TelegramBot:
    def __init__(self, token: str):
        self.app = Application.builder().token(token).build()  # Use Application.builder() for the new version
        self.ai = Ai(api_key='Groq Cloud Api Key') # Replace 'Groq Cloud Api Key' with your own key
        self.cleaner = cleaner.Cleaner()
        self.admin_id = 6130657076  # Admin account ID
        self.log_file = f"logs/log_{time.strftime('%Y%m%d-%H%M%S')}.log"

        # Run the asynchronous setup_logging method
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.setup_logging())
        self.register_handlers()

    async def setup_logging(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            filename=self.log_file
        )
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(console)

        bot = Bot(token=self.app.bot.token)
        me = await bot.get_me()
        if me:
            logging.info(f"Logged in as {me.first_name}")
        else:
            logging.error("Failed to log in.")
            print("Failed to log in.")

        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        print(f"CPU: {cpu_percent}% {'🔥' if cpu_percent > 80 else ''} | Memory: {memory_percent}% {'☁' if memory_percent > 80 else ''} | Disk: {disk_percent}% {'💾' if disk_percent > 80 else ''}")

    def register_handlers(self):
        commands = [
            ("start", self.start),
            ("help", self.help),
            ("ping", self.ping),
            ("send_vocab", self.send_vocab),
            ("meaning", self.meaning),
            ('rewrite', self.rewrite),
            ("email", self.email),
            ("letter", self.letter),
            ("summarise", self.summarise),
            ("compose", self.compose),
            ('pronounce', self.pronounce),
            ("essay", self.essay),
            ("stats", self.stats),
            ("logs", self.logs),
            ("restart", self.restart_bot),
            ("dev", self.dev_info)
        ]
    
        for command, handler in commands:
            self.app.add_handler(CommandHandler(command, handler))

    def log_user_action(self, update: Update, action: str):
        user = update.effective_user
        if user:
            logging.info(f"{action} invoked by {user.username}")
        else:
            logging.info(f"{action} invoked by an unknown user")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.send_message(update, "Hello there! I am erocabulary, designed to help you improve your vocabulary.")
        await self.send_message(update, "To get started, just type /help and I'll show you the way. Let's expand our vocabulary together 😊")
        self.log_user_action(update, "/start")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = """
👋 Welcome to @erocabulary_bot Here are some of my available commands:

⭐ /start - Sends a greeting message.
📚 /send_vocab - Improves your vocabulary by sending a random English word with its definition and use case.
📝 /compose <topic> - Composes a poem, story, or ideas.
🗣️ /pronounce <word> - Learn to pronounce a word.
✍🏻 /rewrite <content> - Rephrases and rewrites the given content with correct English.
📖 /meaning <word/phrase> - Provides the definition and sentence example of the requested word/phrase.
📝 /essay <topic> - Provides an essay on the given topic.
📧 /email <details> - Writes an email on the given information.
✉ /letter <details> - Writes a letter on the given information.
🔤 /summarise <paragraph> - Produces a summary of the given paragraph or topic.
🌐 /ping - Shows the round-trip latency in milliseconds between this bot and Telegram servers.
ℹ /dev - Information regarding the developer of this bot.
        """
        await self.send_message(update, message)
        self.log_user_action(update, "/help")

    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        start_time = time.time()
        await self.send_message(update, "Pinging...")
        latency = round((time.time() - start_time) * 1000, 2)
        await self.send_message(update, f"Pong! Latency is {latency}ms")
        self.log_user_action(update, "/ping")

    async def send_vocab(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.generate_and_send_response(update, "Please provide me an English word or phrase, Gen Z term, Instagram or texting abbreviation, or any emotion along with its meaning/definition, use case, and a sentence example.")

    async def meaning(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        word = self.extract_text(update.message.text, "/meaning")
        await self.generate_and_send_response(update, f"Please tell me the meaning/definition and use-case of {word}.")

    async def rewrite(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        content = self.extract_text(update.message.text, "/rewrite")
        await self.generate_and_send_response(update, f"Please rephrase and rewrite the following content with correct grammar and punctuation: {content}")

    async def email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        email_info = self.extract_text(update.message.text, "/email")
        await self.generate_and_send_response(update, f"Please write an email on the following information/context: {email_info}")

    async def letter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        letter_info = self.extract_text(update.message.text, "/letter")
        await self.generate_and_send_response(update, f"Please write a letter on the following information/context: {letter_info}")

    async def pronounce(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        word = self.extract_text(update.message.text, "/pronounce")
        await self.generate_and_send_response(update, f"Please pronounce the word {word}.")

    async def summarise(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        summary_info = self.extract_text(update.message.text, "/summarise")
        await self.generate_and_send_response(update, f"Please write a summary on the following information/paragraph: {summary_info}")

    async def essay(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        essay_info = self.extract_text(update.message.text, "/essay")
        await self.generate_and_send_response(update, f"Please write an essay on {essay_info}.")

    async def compose(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        topic = self.extract_text(update.message.text, "/compose")
        await self.generate_and_send_response(update, f"Please compose a poem, story, or ideas on the following topic: {topic}")

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        message = f"CPU: {cpu_percent}% {'🔥' if cpu_percent > 80 else ''} \nMemory: {memory_percent}% {'☁' if memory_percent > 80 else ''} \nDisk: {disk_percent}% {'💾' if disk_percent > 80 else ''}"
        await self.send_message(update, message)
        self.log_user_action(update, "/stats")

    async def logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            with open(self.log_file, 'r') as f:
                log = f.read()
                await self.send_message(update, log)
        except Exception as e:
            await self.handle_exception(update, e, "reading logs")

    async def restart_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user and update.effective_user.id == self.admin_id:
            await self.send_message(update, "Restarting...")
            try:
                self.cleaner.clean_logs()
                self.cleaner.clear_cache()
                os.execl(sys.executable, sys.executable, *sys.argv)
            except Exception as e:
                await self.handle_exception(update, e, "restarting bot")
        else:
            await self.send_message(update, "You are not authorized to use this command.")
            self.log_user_action(update, "Unauthorized /restart attempt")

    async def dev_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        dev_info = """
👨🏻‍💻 Developer Information:
   Name: Akshat Singh
   🇮🇳 Nationality: Indian
   🌐 Languages: English, Hindi
   🐙 GitHub: github.com/a3ro-dev/
   📬 Telegram: @a3roxyz
        """
        await self.send_message(update, dev_info)
        self.log_user_action(update, "/dev_info")

    async def send_message(self, update: Update, text: str):
        await update.message.reply_text(text)

    async def generate_and_send_response(self, update: Update, prompt: str):
        try:
            response = self.ai.generate_response(text=prompt)
            await self.send_message(update, response)
            self.log_user_action(update, "Response generated")
        except Exception as e:
            await self.handle_exception(update, e, "generating response")

    async def handle_exception(self, update: Update, exception: Exception, context: str):
        logging.error(f"Exception occurred during {context}: {exception}")
        await self.send_message(update, f"Exception occurred while {context}. ErrorMessage: {exception}")

    def extract_text(self, message_text: str, command: str) -> str:
        return message_text.replace(command, "").strip()

    def run(self):
        self.app.run_polling()

if __name__ == "__main__":
    bot = TelegramBot("YOUR_BOT_TOKEN") # from telegram docs or readme.md
    bot.run()