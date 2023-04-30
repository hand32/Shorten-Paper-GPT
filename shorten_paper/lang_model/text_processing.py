import math
import tiktoken
from shorten_paper.logs import Logger

logger = Logger()


def string_to_tokens(
        string: str, lang_model: str = "gpt-3.5-turbo"
) -> list[int]:
    try:
        encoding = tiktoken.encoding_for_model(lang_model)
    except ValueError:
        logger.warn("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    string = string.replace("\n", " ")
    return encoding.encode(string)


def count_string_tokens(
        string: str, lang_model: str = "gpt-3.5-turbo"
) -> int:
    return len(string_to_tokens(string, lang_model))


def tokens_to_string(
        tokens: list[int], lang_model: str = "gpt-3.5-turbo",
        token_start_idx: int = None, token_end_idx: int = None, from_back: bool = True
) -> (str, int):
    """
    Converts a list of token IDs to a string using the specified language model's encoding in a safe way.

    Args:
        tokens (list[int]): A list of token IDs.
        lang_model (str): The name of the language model to use for encoding.
        token_start_idx (int): The index of the starting token to convert. Defaults to None, the start of the list.
        token_end_idx (int): The index of the ending token to convert. Defaults to None, the end of the list.
        from_back (bool): If True, to truncate the string from the end of the token list. If False, from the start.

    Returns:
        str: The decoded string.
        int: The token count of decoded string.
    """
    try:
        encoding = tiktoken.encoding_for_model(lang_model)
    except ValueError:
        logger.warn("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    if from_back:
        tmp_token_end_idx = token_end_idx if token_end_idx else len(tokens)
        while True:
            if tmp_token_end_idx < 1:
                result_tokens = tokens[token_start_idx:token_end_idx]
                return encoding.decode(result_tokens), len(result_tokens)
            try:
                result_tokens = tokens[token_start_idx:tmp_token_end_idx]
                return encoding.decode_bytes(result_tokens).decode(), len(result_tokens)
            except UnicodeDecodeError:
                tmp_token_end_idx -= 1
    else:
        tmp_token_start_idx = token_start_idx if token_start_idx else 0
        while True:
            if tmp_token_start_idx >= len(tokens):
                result_tokens = tokens[token_start_idx:token_end_idx]
                return encoding.decode(result_tokens), len(result_tokens)
            try:
                result_tokens = tokens[tmp_token_start_idx:token_end_idx]
                return encoding.decode(result_tokens), len(result_tokens)
            except UnicodeDecodeError:
                tmp_token_start_idx += 1


def truncate_by_token_cnt(
        string: str, lang_model: str = "gpt-3.5-turbo", token_cnt: int = None, from_back: bool = True
) -> (str, int):
    tokens = string_to_tokens(string, lang_model)
    if from_back:
        return tokens_to_string(tokens, lang_model, None, token_cnt, True)
    return tokens_to_string(tokens, lang_model, max(0, len(tokens) - token_cnt), None, False)


def split_with_next_text(
        text: str, lang_model: str, max_token_len: int, next_text_ratio: float
) -> list[dict]:
    """
    Splits a given input text into smaller chunks
    compose of current text and next text
    based on max_token_len and next_text_ratio.

    Args:
        text (str): Text to be split.
        lang_model (str): OpenAI language model name for the token calculation.
        max_token_len (int): The maximum number of tokens allowed per chunk.
        next_text_ratio (float): The ratio of the length of the next text to the max_token_len.

    Returns:
    A list of dictionaries where each dictionary contains two keys:
    'current_text' and 'next_text'.
    The value of 'current_text' is a dict
    containing the truncated current text and the number of tokens in it,
    and the value of 'next_text' is a dict
    containing the truncated next text and the number of tokens in it.
    """
    if next_text_ratio < 0 or next_text_ratio >= 1:
        raise ValueError(f"next_text_ratio must be [0, 1).")
    current_text_max_token_len = math.ceil((1 - next_text_ratio) * max_token_len)
    next_text_max_token_len = max_token_len - current_text_max_token_len

    result_split_list = []

    while len(text) > 0:
        current_text, current_token_cnt = truncate_by_token_cnt(text, lang_model, current_text_max_token_len)
        text = text[len(current_text):]
        next_text, next_token_cnt = truncate_by_token_cnt(text, lang_model, next_text_max_token_len)
        result_split_list.append({"current_text": {"text": current_text, "token_cnt": current_token_cnt},
                                  "next_text": {"text": next_text, "token_cnt": next_token_cnt}})

    return result_split_list


def split_with_previous_text(
        text: str, lang_model: str, max_token_len: int, previous_text_ratio: float
) -> list[dict]:
    """
    Splits a given input text into smaller chunks
    compose of current text and previous text
    based on max_token_len and previous_text_ratio.

    Args:
        text (str): Text to be split.
        lang_model (str): OpenAI language model name for the token calculation.
        max_token_len (int): The maximum number of tokens allowed per chunk.
        previous_text_ratio (float): The ratio of the length of the previous text to the max_token_len.

    Returns:
    A list of dictionaries where each dictionary contains two keys:
    'current_text' and 'previous_text'.
    The value of 'current_text' is a dict
    containing the truncated current text and the number of tokens in it,
    and the value of 'previous_text' is a dict
    containing the truncated previous text and the number of tokens in it.
    """
    if previous_text_ratio < 0 or previous_text_ratio >= 1:
        raise ValueError(f"previous_text_ratio must be [0, 1).")
    current_text_max_token_len = math.ceil((1 - previous_text_ratio) * max_token_len)
    previous_text_max_token_len = max_token_len - current_text_max_token_len

    result_split_list = []

    previous_text = ""
    while len(text) > 0:
        current_text, current_token_cnt = truncate_by_token_cnt(text, lang_model, current_text_max_token_len)
        previous_text, previous_token_cnt = \
            truncate_by_token_cnt(previous_text, lang_model, previous_text_max_token_len, from_back=True)

        result_split_list.append({"previous_text": {"text": previous_text, "token_cnt": previous_token_cnt},
                                  "current_text": {"text": current_text, "token_cnt": current_token_cnt}})

        text = text[len(current_text):]
        previous_text = "".join([previous_text, current_text])

    return result_split_list


if __name__ == "__main__":
    _text = input("text: ")
    _max_token_len = int(input("max_token_len: "))
    _lang_model = input("lang_model: ")
    _previous_text_ratio = float(input("previous_text_ratio: "))
    _next_text_ratio = float(input("next_text_ratio"))
    print("Previous Split")
    print(split_with_previous_text(_text, _lang_model, _max_token_len, _previous_text_ratio))
    print()
    print("Next Split")
    print(split_with_next_text(_text, _lang_model, _max_token_len, _next_text_ratio))
