import openai
import logging
import time
# Set up the OpenAI API client with your API key
openai.api_key = "OPENAI_API_KEY"

# Set the temperature for text generation
temperature = 1 # change it accordingly

# Set up logging
log_file = f"log_{time.strftime('%Y%m%d-%H%M%S')}.log"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO, filename=log_file)


class Ai:
  """
  This class provides a gateway to the OpenAI api for text generation.
  """
  def __init__(self):
    self.prompt = ""
  def get_prompt(self, prompt):
    self.prompt = prompt

  def generate_response(self):
    try:
      # Generate text using the text-davinci-003 model and the specified temperature
      response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=self.prompt,
        temperature=temperature,
        max_tokens=1024,
        n=1,
        stop=None,
      )
      # Parse the response to extract the generated text
      message = response.choices[0].text.strip() # type: ignore
      return message
    except Exception as e:
      # Log any exceptions that occur
      logging.error(e)
      return "Sorry, an error occurred while generating the response."
    
  def main(self):
    self.get_prompt(prompt="Hello World")
    message = self.generate_response()
    return message
#================================================================================================================================
