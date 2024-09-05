from groq import Groq
import logging
import time


# Set up logging
log_file = f"log_{time.strftime('%Y%m%d-%H%M%S')}.log"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO, filename=log_file)


class Ai:
  """
  This class provides a gateway to the Large Language Model for response generation
  """
  def __init__(self, api_key):
    self.client = Groq(api_key=api_key)

  def generate_response(self, text: str) -> str:
    try:
      completion = self.client.chat.completions.create(
        model = 'llama-3.1-70b-versatile', # "llama3-70b-8192" - "mixtral-8x7b-32768" = other options 
        messages=[
          {
            "role": "system",
            "content": "do exactly as directed."
          },
          {
            "role": "user",
            "content": text

          }
        ],
        temperature = 0.5,
        max_tokens=8192,
        top_p=1,
        stream=False,
        stop=None,
      )
      message: str = str(completion.choices[0].message.content)
      return message
    except Exception as e:
      # Log any exceptions that occur
      logging.error(e)
      return "Sorry, an error occurred while generating the response."
    
  def main(self):
    message = self.generate_response(text="Hello World")
    return message
#================================================================================================================================
