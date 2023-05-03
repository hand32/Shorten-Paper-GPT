import os
import openai
from shorten_paper.singletone import Singleton
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Config(metaclass=Singleton):
    def __init__(self):
        self.papers_input_dir = os.getenv("PAPERS_INPUT_DIR")
        self.papers_output_dir = os.getenv("PAPERS_OUTPUT_DIR")
        self.output_prefix = os.getenv("OUTPUT_PREFIX")

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        self.lang_model_name = os.getenv("LANG_MODEL_NAME")
        self.text_token_len = int(os.getenv("TEXT_TOKEN_LEN")) - 122  # 122 tokens for pre-defined prompt.
        if self.text_token_len <= 0:
            raise ValueError("text_token_len (int) should be over 0.")

        self.model_temperature = float(os.getenv("MODEL_TEMPERATURE"))
        self.model_top_p = float(os.getenv("MODEL_TOP_P"))
        self.model_presence_penalty = float(os.getenv("MODEL_PRESENCE_PENALTY"))
        self.model_frequency_penalty = float(os.getenv("MODEL_FREQUENCY_PENALTY"))

        self.shorten_repeat = int(os.getenv("SHORTEN_REPEAT"))
        if self.shorten_repeat <= 0:
            raise ValueError("shorten_repeat (int) should be over 0.")
        self.shorten_ratio = float(os.getenv("SHORTEN_RATIO"))
        self.previous_text_token_ratio = float(os.getenv("PREVIOUS_TEXT_TOKEN_RATIO"))
        self.next_text_token_ratio = float(os.getenv("NEXT_TEXT_TOKEN_RATIO"))
