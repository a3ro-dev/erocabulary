import logging
import time
from telegram.ext import Updater, CommandHandler
from utils import ai
import psutil
import openai
from utils import cleaner

openai.api_key = "OPENAI_API_KEY" # your openai api key from https://platform.openai.com/account/api-keys

class TelegramBot:
  def __init__(self, token):
    self.updater = Updater(token=token, use_context=True) # initializing the updater class with token
    self.dispatcher = self.updater.dispatcher # initializing the dispatcher object from updater class
    self.ai = ai.Ai() # initializing the ai object from class Ai for generating responses
    self.bot = self.updater.bot # initializing the bot from updater class
    self.cleaner = cleaner.Cleaner() # initializing the cleaner object from class cleaner which clears log files
    self.admin = 6130657076 # admin account id "change it to your account id"
    self.log_file = f"log_{time.strftime('%Y%m%d-%H%M%S')}.log" # log file for logging

        # Create a new log file for each run of the bot
    log_file = f"logs/log_{time.strftime('%Y%m%d-%H%M%S')}.log"
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # defining the logging format
                            level=logging.INFO, filename=log_file)
    console = logging.StreamHandler() # definining console 
    console.setLevel(logging.DEBUG) # defining the logging level which is set to DEBUG

    # Add the console handler to the logger
    logging.getLogger('').addHandler(console) # adding the console handler which is console which prints the messages on the console like the print function

        # Print login status to console
    if self.bot.get_me():
      logging.info(f"Logged in as {self.bot.get_me().first_name}") #type: ignore
    else:
      logging.error("Failed to log in.")
      print("Failed to log in.")
    """
    Just a cool looking console output code which tells which account the bot has logged into
    """

        # Print computer information to console
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    print(f"CPU: {cpu_percent}% {'🔥' if cpu_percent > 80 else ''} | Memory: {memory_percent}% {'☁' if memory_percent > 80 else ''} | Disk: {disk_percent}% {':floppy_disk:' if disk_percent > 80 else ''}") # again just for cool looking it tells the current cpu memory and disk usage and availability

  def start(self, update, context): # the /start command which sends greeting message to the user to get the user started
    try:
      logging.info(f"/start invoked!")
      context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there! I am erocabulary, designed to help you improve your vocabulary")
      message = "To get started, just type /help and I'll show you the way. Let's expand our vocabulary together 😊"
      context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
      logging.error(e)

  def help(self, update, context): # /help command to send the help menu to the user
    try:
      logging.info("/help invoked!")
      message = """
👋 Welcome to @erocabulary_bot Here are some of my available commands:

⭐ /start  [sends a greeting message to get you started.]

📚 /send_vocab  [improves your vocabulary by sending a random English word with its definition and use case.]

📝 /compose <topic> [composes a poem, story, or ideas.]

🗣️ /pronounce <word> [learn to pronounce a word.]

✍🏻 /rewrite <content> [rephrases and rewrites the given content with correct English.]

📖 /meaning <word/phrase>  [gets you the definition and sentence example of the requested word/phrase.]

📝 /essay <topic>  [provides you with an essay of 200 words on the given topic.]

📧 /email <email formal or informal | content | information | context>  [writes an email on the given information.]

✉ /letter <letter formal or informal | topic | information | context> [writes a letter on the given information.]

🔤 /summarise <paragraph> [produces a summmary on the given paragraph | information | topic]

🌐 /ping  [the round-trip latency in milliseconds between this bot and the Telegram servers.]

ℹ /dev  [information regarding the desveloper of this bot.]

*DEBUG*

📥 /stats  [gets you some statistics about the bot.]

❌ /logs [retrieves the log file for debugging.]

🔁 /restart [restarts the bot (admin only)]

🎫/tick [sends your message to the developers of this bot]

I'm your one-stop-shop for all things English related, designed to help you enhance your language skills with ease and convenience. Start improving your English language proficiency today!
"""
      context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
      logging.error(e)

  def ping(self, update, context): # calculates the round trip latency in milliseconds
    try:
      start_time = time.time()
      context.bot.send_message(chat_id=update.effective_chat.id, text="Pinging..")
      end_time = time.time()
      message = f"Pong! Latency is {round((end_time - start_time) * 1000, 2)}ms"
      context.bot.send_message(chat_id=update.effective_chat.id ,text=message)
      logging.info(f"/ping invoked!\n By: {update.effective_user.username}")
    except Exception as e:
      logging.error(e)

  def send_vocab(self, update, context): # the main key feature, the /send_vocab thing which sends a word with it's meaning to the user and sentence example
    try:
      user = update.effective_user
      message = ""
      self.ai.get_prompt(prompt="""Please provide me an English word or phrase, Gen Z term, Instagram or texting abbreviation, or any emotion along with its meaning/definition, use case, and a sentence example. Please format your response as follows:

  Word: [insert word or phrase]
  Definition: [insert definition]
  Use-Case: [insert sentence example]

  Please make sure to leave a line after each heading.""")
      response = self.ai.generate_response()
      message += f"{response}"
      # Send the response message to the user
      context.bot.send_message(chat_id=user.id, text=message)
      logging.info(f"/send_vocab invoked!\n response: {response}\n By: {update.effective_user.username}")
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response.\nErrorMessage:\n{e}")

  def meaning(self, update, context): # basically the same as /send_vocab but takes the word of which the meaning has to be sent of
    try:
      text = update.message.text
      word = text.replace('/meaning ', '')
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating definitions and sentence example for: {word}")
      message = ""
      self.ai.get_prompt(prompt=f"""Please tell me the the meaning/definition, use case(sentence example) of {word} in this format
              Word: [insert word or phrase]
              Definition: [insert definition]
              Use-Case: [insert sentence example]""")
      response = self.ai.generate_response()
      # send the response to the user
      message += f"{response}"
      context.bot.send_message(chat_id=update.effective_chat.id, text=message)
      logging.info(f"/meaning invoked!\n prompt: {word}\n response: {response}\n By: {update.effective_user.username}")
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response.\nErrorMessage:\n{e}")

  def email(self, update, context): # generates an email on the given prompt and sends it to the user
    try:
      text = update.message.text
      email_info = text.replace('/email ', '')
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating response for : {email_info}")
      email = ""
      self.ai.get_prompt(prompt=f"""Please write an email on the following information/context {email_info}""")
      response = self.ai.generate_response()
      email += f"{response}"
          # Send the email message to the user
      context.bot.send_message(chat_id=update.effective_chat.id, text=email)
      logging.info(f"/email invoked!\n prompt: {email_info}\n response: {email}\n By: {update.effective_user.username}")
    except Exception as e:
        logging.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response. \nErrorMessage:\n{e}")

  def letter(self, update, context): # generate an email on the given prompt and sends it to the user
    try:
      text = update.message.text
      letter_info = text.replace('/letter ', '')
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating response for : {letter_info}")
      letter = ""
      self.ai.get_prompt(prompt=f"""Please write a on the following information/context {letter_info}""")
      response = self.ai.generate_response()
      letter += f"{response}"
          # Send the letter message to the user
      context.bot.send_message(chat_id=update.effective_chat.id, text=letter)
      logging.info(f"/letter invoked!\n prompt: {letter_info}\n response: {letter}\n By: {update.effective_user.username}")
    except Exception as e:
        logging.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response. \nErrorMessage:\n{e}")

  def summarise(self, update, context): # generate a summary of the given prompt and sends it to the user
    try:
  
      text = update.message.text
      summary_info = text.replace('/summarise ', '')
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating response for : {summary_info}")
      summary = ""
      self.ai.get_prompt(prompt=f"""Please write a summary on the following information/paragraph: \n\n{summary_info}, also tell approx. word count""")
      response = self.ai.generate_response()
      summary += f"{response}"
          # Send the email message to the user
      context.bot.send_message(chat_id=update.effective_chat.id, text=summary)
      logging.info(f"/summarise invoked!\n prompt: {summary_info}\n response: {summary}\n By: {update.effective_user.username}")    
    except Exception as e:
        logging.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response. \nErrorMessage:\n{e}")

  def essay(self, update, context): # generates an essay on the give topic, basically an outline and sends to the user
    try:
      text = update.message.text
      essay_info = text.replace('/essay ', '')
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating response for : {essay_info}")
      essay = ""
      self.ai.get_prompt(prompt=f"""Please write me an essay on {essay_info}, also please use high quality vocabulary and keep it in simple language, also do mention approx. word count""")
      response = self.ai.generate_response()
      essay += f"{response}"
        # Send the essay message to the user
      context.bot.send_message(chat_id=update.effective_chat.id, text=essay)
      logging.info(f"/essay invoked!\n prompt: {essay_info}\n response: {essay}\n By: {update.effective_user.username}") 
    except Exception as e:
        logging.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response.\nErrorMessage:\n{e}")

  def stats(self, update, context): # tells the current cpu memory and disk usage and sends it to the debugger
    try:
      logging.info("/stats invoked!")
      cpu_percent = psutil.cpu_percent()
      memory_percent = psutil.virtual_memory().percent
      disk_percent = psutil.disk_usage('/').percent
      message = f"CPU: {cpu_percent}% {'🔥' if cpu_percent > 80 else ''} \nMemory: {memory_percent}% {'☁' if memory_percent > 80 else ''} \nDisk: {disk_percent}% {'💾' if disk_percent > 80 else ''}"
      context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating stats.\nErrorMessage:\n{e}")

  def logs(self, update, context): # sends the logs over the chats, might not send if it's too long
    try:
      logging.info("/logs invoked!")
      with open (self.log_file, 'r') as f:
        log = f.read()
        context.bot.send_message(chat_id=update.effective_chat.id, text=log)
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating stats.\nErrorMessage:\n{e}")

  def restart_bot(self ,update, context):
    try:
      logging.info("/restart invoked!")
        # Check if the user is an admin
      if update.effective_user.id == self.admin:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Restarting...")
        try:
          self.cleaner.clean_logs()
          self.cleaner.clear_cache()
        except Exception as e:
          logging.error(e)
          context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while clearing junk files\nErrorMessage:\n{e}")
        try:
          import os
          import sys
          os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
          logging.error(e)
          context.bot.send_message(chat_id=update.effective_chat.id, text=f"Restart Successful\n")
      else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while restarting bot.\nErrorMessage:\n{e}")

  def dev_info(self, update, context):
    try:
      logging.info("/dev_info invoked!")
      dev_info = """
 👨🏻<200d>💻 Developer Information:
   Name: Akshat Singh
   🇮🇳 Nationality
   🌐 Languages: English, Hindi
   🐙 Github: github.com/a3ro-dev/
   📬 Telegram: @a3roxyz

      """
      context.bot.send_message(chat_id=update.effective_chat.id, text=dev_info)
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating developer_info.\nErrorMessage:\n{e}")

  # def talk(self, update, context):
  #   try:
  #       if update.message.text == "/talk":
  #           logging.info("/talk invoked!")
  #           context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am Erocabulary")
  #           while True:
  #               user_input = update.message.text
  #               if user_input in ["/stop", "stop"]:
  #                   context.bot.send_message(chat_id=update.effective_chat.id, text="Goodbye!")
  #                   break
  #               prompt = f"{user_input}\n"
  #               response = openai.Completion.create(
  #                   engine="text-davinci-002",
  #                   prompt=prompt,
  #                   max_tokens=1024,
  #                   n=1,
  #                   stop=None,
  #                   temperature=0.8
  #               )
  #               bot_response = response.choices[0].text.strip()

  #               # check for grammar errors
  #               grammar_check = openai.Completion.create(
  #                   engine="text-davinci-002",
  #                   prompt=f"Please check the grammar for the following text: {user_input}",
  #                   max_tokens=1024,
  #                   n=1,
  #                   stop=None,
  #                   temperature=0.8
  #               )
  #               grammar_errors = grammar_check.choices[0].text.strip()

  #               # send bot response and grammar check result
  #               context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)
  #               if "No errors" not in grammar_errors:
  #                   context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {grammar_errors}")
  #   except Exception as e:
  #       logging.error(e)
  #       context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating talk.\nErrorMessage:\n{e}")

  """
  self.talk wasn't implemented as it had problems with hallucinating contexts and repeating messages again and again, as for the ethical use of AI
  this function wasn't implemented as it was also sending inappropriate messages to the users and was typically out of control 
  if you do find a better way to implement this, do send a push to it.
  """
  def compose(self, update, context): # composes an idea, poem or context/story on the given idea or context or topic
    try:
      text = update.message.text
      compose_info=text.replace("/compose", "")
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating response for : {compose_info}")
      self.ai.get_prompt(prompt=f"compose me a {compose_info} in a very high quality english vocabulary and no grammatical errors also make it sound like original words")
      compose = ""
      response = self.ai.generate_response()
      compose += f"{response}"
      context.bot.send_message(chat_id=update.effective_chat.id, text=compose)
      logging.info(f"/compose invoked\n prompt: {compose_info}\n response: {compose}\n By: {update.effective_user.username}")
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response.\nErrorMessage:\n{e}")

  def rewrite(self, update, context): # rewrites or rephrases a sentence or idea with no grammatical errors, useful for idek what 💀💀
    try:
      text = update.message.text
      rewrite_info=text.replace("/rewrite", "")
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating response for : {rewrite_info}")
      self.ai.get_prompt(prompt=f"rewrite this {rewrite_info} in a very high quality english vocabulary and no grammatical errors also make it sound like original words")
      rewrite = ""
      response = self.ai.generate_response()
      rewrite += f"{response}"
      context.bot.send_message(chat_id=update.effective_chat.id, text=rewrite)
      logging.info(f"/rewrite invoked\n prompt: {rewrite_info}\n response: {rewrite}\n By: {update.effective_user.username}")
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating response.\nErrorMessage:\n{e}")

  def ticket(self, update, context): # useful for sending messages to self.admin, and it also rectifies what issue or what the user is trying to convey
    try:
      logging.info("/ticket invoked")
      text = update.message.text
      ticket_info=text.replace("/ticket", "")
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Creating issue check for : {ticket_info}")
      self.ai.get_prompt(prompt=f"explain me what problem the user has? in computer type clear technical language")
      ticket = ""
      response = self.ai.generate_response()
      ticket += f"{response}"
      context.bot.send_message(chat_id=self.admin, text=f"{ticket}\n\nIssue Raised by: {update.effective_user.username}")
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Issue Sent to admin: \n{ticket}")
    except Exception as e:
      logging.error(e)

  def pronounce(self, update, context): # sends the pronunciation practice for a word for the user to pronounce it, useful feature i guess....
    try:
      text = update.message.text
      word = text.replace("/pronounce", "")
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating pronunciation for : {word}")
      self.ai.get_prompt(prompt=f"teach me how can i pronounce {word}?, explain it to me in simple english in 2-3 lines")
      pronunciation = ""
      response = self.ai.generate_response()
      pronunciation = f"{response}"
      context.bot.send_message(chat_id=update.effective_chat.id, text=pronunciation)
    except Exception as e:
      logging.error(e)
      context.bot.send_message(chat_id=update.effective_chat.id, text=f"Exception occured while generating pronunciation.\nErrorMessage:\n{e}")

  def run(self): # the run function which basically calls all the handlers and all stuff for the bot to handle the commands
    start_handler = CommandHandler('start', self.start)
    help_handler = CommandHandler('help', self.help)
    send_vocab_handler = CommandHandler('send_vocab', self.send_vocab)
    meaning_handler = CommandHandler('meaning', self.meaning)
    email_handler = CommandHandler('email', self.email)
    essay_handler = CommandHandler('essay', self.essay)
    ping_handler = CommandHandler('ping', self.ping)
    stats_handler = CommandHandler('stats', self.stats)
    error_handler = CommandHandler('logs', self.logs)
    restart_handler = CommandHandler('restart', self.restart_bot)
    dev_info_handler = CommandHandler('dev', self.dev_info)
    letter_handler = CommandHandler('letter', self.letter)
    summmary_handler = CommandHandler('summarise', self.summarise)
    # talk_handler = CommandHandler('talk', self.talk) ""ded""
    compose_handler = CommandHandler('compose', self.compose)
    rewrite_handler = CommandHandler('rewrite', self.rewrite)
    ticket_handler = CommandHandler('ticket', self.ticket)
    pronounce_handler = CommandHandler('pronounce', self.pronounce)

    self.dispatcher.add_handler(start_handler)
    self.dispatcher.add_handler(help_handler)
    self.dispatcher.add_handler(send_vocab_handler)
    self.dispatcher.add_handler(meaning_handler)
    self.dispatcher.add_handler(email_handler)
    self.dispatcher.add_handler(essay_handler)
    self.dispatcher.add_handler(ping_handler)
    self.dispatcher.add_handler(stats_handler)
    self.dispatcher.add_handler(error_handler)
    self.dispatcher.add_handler(restart_handler)
    self.dispatcher.add_handler(dev_info_handler)
    self.dispatcher.add_handler(letter_handler)
    self.dispatcher.add_handler(summmary_handler)
    # self.dispatcher.add_handler(talk_handler)
    self.dispatcher.add_handler(compose_handler)
    self.dispatcher.add_handler(rewrite_handler)
    self.dispatcher.add_handler(ticket_handler)
    self.dispatcher.add_handler(pronounce_handler)
#--------------------------------------------------------------------------------------------------------------------------------
    self.updater.start_polling()
    self.updater.idle()

TG = TelegramBot(token="TELEGRAM_BOT_TOKEN") # put your telegram bot token which you got from botfather on telegram
"""
Step 1: Find BotFather account
Step 2: Create a new bot and generate token
Step 3: Put that token here
"""
TG.run()