import os
import PyPDF2
import docx
import json
import yaml
from bs4 import BeautifulSoup
import markdown
from pylatexenc.latex2text import LatexNodes2Text

import math
from shorten_paper.lang_model.text_processing import \
    (split_with_next_text, count_string_tokens, truncate_by_token_cnt)
from shorten_paper.lang_model.api_call import create_chat_completion

from colorama import Fore
from shorten_paper.spinner import Spinner
from shorten_paper.logs import Logger
from shorten_paper.config import Config

logger = Logger()
CFG = Config()

ENCODINGS = ['utf_8',
             'ascii',
             'big5',
             'big5hkscs',
             'cp037',
             'cp273',
             'cp424',
             'cp437',
             'cp500',
             'cp720',
             'cp737',
             'cp775',
             'cp850',
             'cp852',
             'cp855',
             'cp856',
             'cp857',
             'cp858',
             'cp860',
             'cp861',
             'cp862',
             'cp863',
             'cp864',
             'cp865',
             'cp866',
             'cp869',
             'cp874',
             'cp875',
             'cp932',
             'cp949',
             'cp950',
             'cp1006',
             'cp1026',
             'cp1125',
             'cp1140',
             'cp1250',
             'cp1251',
             'cp1252',
             'cp1253',
             'cp1254',
             'cp1255',
             'cp1256',
             'cp1257',
             'cp1258',
             'euc_jp',
             'euc_jis_2004',
             'euc_jisx0213',
             'euc_kr',
             'gb2312',
             'gbk',
             'gb18030',
             'hz',
             'iso2022_jp',
             'iso2022_jp_1',
             'iso2022_jp_2',
             'iso2022_jp_2004',
             'iso2022_jp_3',
             'iso2022_jp_ext',
             'iso2022_kr',
             'latin_1',
             'iso8859_2',
             'iso8859_3',
             'iso8859_4',
             'iso8859_5',
             'iso8859_6',
             'iso8859_7',
             'iso8859_8',
             'iso8859_9',
             'iso8859_10',
             'iso8859_11',
             'iso8859_13',
             'iso8859_14',
             'iso8859_15',
             'iso8859_16',
             'johab',
             'koi8_r',
             'koi8_t',
             'koi8_u',
             'kz1048',
             'mac_cyrillic',
             'mac_greek',
             'mac_iceland',
             'mac_latin2',
             'mac_roman',
             'mac_turkish',
             'ptcp154',
             'shift_jis',
             'shift_jis_2004',
             'shift_jisx0213',
             'utf_32',
             'utf_32_be',
             'utf_32_le',
             'utf_16',
             'utf_16_be',
             'utf_16_le',
             'utf_7',
             'utf_8_sig']


class ParserStrategy:
    def read(self, file_path):
        raise NotImplementedError


# Basic text file reading
class TXTParser(ParserStrategy):
    def read(self, file_path):
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    text = f.read()
                    logger.typewriter_log(f"Encoding:", Fore.CYAN, encoding)
                return text
            except UnicodeDecodeError:
                continue
        raise IOError("TXTParser Read Error.")


# Reading text from binary file using pdf parser
class PDFParser(ParserStrategy):
    def read(self, file_path):
        parser = PyPDF2.PdfReader(file_path)
        text = ""
        for page_idx in range(len(parser.pages)):
            text += parser.pages[page_idx].extract_text()
        return text


# Reading text from binary file using docs parser
class DOCXParser(ParserStrategy):
    def read(self, file_path):
        doc_file = docx.Document(file_path)
        text = ""
        for para in doc_file.paragraphs:
            text += para.text
        return text


# Reading as dictionary and returning string format
class JSONParser(ParserStrategy):
    def read(self, file_path):
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    data = json.load(f)
                    text = str(data)
                    logger.typewriter_log(f"Encoding:", Fore.CYAN, encoding)
                return text
            except UnicodeDecodeError:
                continue
        raise IOError("JSONParser Read Error.")


class XMLParser(ParserStrategy):
    def read(self, file_path):
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    soup = BeautifulSoup(f, "xml")
                    text = soup.get_text()
                    logger.typewriter_log(f"Encoding:", Fore.CYAN, encoding)
                return text
            except UnicodeDecodeError:
                continue
        raise IOError("XMLParser Read Error.")


# Reading as dictionary and returning string format
class YAMLParser(ParserStrategy):
    def read(self, file_path):
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    text = str(data)
                    logger.typewriter_log(f"Encoding:", Fore.CYAN, encoding)
                return text
            except UnicodeDecodeError:
                continue
        raise IOError("YAMLParser Read Error.")


class HTMLParser(ParserStrategy):
    def read(self, file_path):
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    soup = BeautifulSoup(f, "html.parser")
                    text = soup.get_text()
                    logger.typewriter_log(f"Encoding:", Fore.CYAN, encoding)
                return text
            except UnicodeDecodeError:
                continue
        raise IOError("HTMLParser Read Error.")


class MarkdownParser(ParserStrategy):
    def read(self, file_path):
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    html = markdown.markdown(f.read())
                    text = "".join(BeautifulSoup(html, "html.parser").findAll(string=True))
                    logger.typewriter_log(f"Encoding:", Fore.CYAN, encoding)
                return text
            except UnicodeDecodeError:
                continue
        raise IOError("MarkdownParser Read Error.")


class LaTeXParser(ParserStrategy):
    def read(self, file_path):
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    latex = f.read()
                    text = LatexNodes2Text().latex_to_text(latex)
                    logger.typewriter_log(f"Encoding:", Fore.CYAN, encoding)
                return text
            except UnicodeDecodeError:
                continue
        raise IOError("LaTeXParser Read Error.")


class FileContext:
    def __init__(self, parser):
        self.parser = parser

    def set_parser(self, parser):
        self.parser = parser

    def read_file(self, file_path):
        return self.parser.read(file_path)


extension_to_parser = {
    ".txt": TXTParser(),
    ".csv": TXTParser(),
    ".pdf": PDFParser(),
    ".doc": DOCXParser(),
    ".docx": DOCXParser(),
    ".json": JSONParser(),
    ".xml": XMLParser(),
    ".yaml": YAMLParser(),
    ".html": HTMLParser(),
    ".md": MarkdownParser(),
    ".tex": LaTeXParser(),
}


def read_textual_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    parser = extension_to_parser.get(file_extension)
    if not parser:
        if not file_extension or file_extension == "":
            file_extension = "Directory"
        raise ValueError(f"Unsupported file format: {file_extension}. Supporting {list(extension_to_parser.keys())}")
    file_context = FileContext(parser)
    return file_context.read_file(file_path)


def shorten_text(
        text: str, filename: str,
        lang_model: str = CFG.lang_model_name,
        shorten_ratio: float = CFG.shorten_ratio,
        previous_text_token_ratio: float = CFG.previous_text_token_ratio,
        next_text_token_ratio: float = CFG.next_text_token_ratio
) -> str:
    """Shorten document's text.

    Args:
        text (str): The text to summarize.
        filename (str): The filename of given text.
        lang_model (str): The name of the language model to use for encoding.
        shorten_ratio (float): Ratio to be shortened (0, 1].
        previous_text_token_ratio (float):  Ratio to be referenced [0, 1).
        next_text_token_ratio (float): Ratio to be referenced [0, 1).

    Returns:
        str: The shortened version of the text.
    """
    if not text:
        raise ValueError("No text to shorten.")
    if shorten_ratio <= 0 or shorten_ratio > 1:
        raise ValueError("shorten_ratio must be (0, 1].")
    if previous_text_token_ratio < 0 or previous_text_token_ratio >= 1:
        raise ValueError("next_text_token_ratio must be (0, 1].")
    if next_text_token_ratio < 0 or next_text_token_ratio >= 1:
        raise ValueError("next_text_token_ratio must be (0, 1].")
    if previous_text_token_ratio + next_text_token_ratio >= 1:
        raise ValueError("Sum of next/previous_text_token_ratio must be under 1.0.")

    logger.typewriter_log(
        "File name:",
        Fore.CYAN,
        filename
    )
    logger.typewriter_log(
        "Text length:",
        Fore.YELLOW,
        f"{len(text)} characters"
    )
    text_token_cnt = count_string_tokens(text, lang_model)
    logger.typewriter_log(
        "Token count:",
        Fore.YELLOW,
        f"{text_token_cnt} tokens"
    )
    logger.typewriter_log(
        "Shorten ratio:",
        Fore.GREEN,
        f"{shorten_ratio}"
    )
    logger.typewriter_log(
        "Try to shorten",
        Fore.BLUE
    )
    logger.typewriter_log(
        f"| {len(text)} -> {math.floor(len(text) * shorten_ratio)} characters."
    )
    logger.typewriter_log(
        f"| {text_token_cnt} -> {math.floor(text_token_cnt * shorten_ratio)} tokens."
    )
    print()

    shorten_text_list = []
    current_text_token_target = math.floor(
        CFG.text_token_len / (1 + shorten_ratio + previous_text_token_ratio + next_text_token_ratio)
    )
    chunks = split_with_next_text(
        text, lang_model=lang_model,
        max_token_len=math.floor(current_text_token_target * (1 + next_text_token_ratio)),
        next_text_ratio=next_text_token_ratio / (1 + next_text_token_ratio)
    )

    previous_shorten_output = ""
    for i, chunk in enumerate(chunks):
        current_text = chunk["current_text"]["text"]
        current_token_cnt = chunk["current_text"]["token_cnt"]
        next_text = chunk["next_text"]["text"]
        next_token_cnt = chunk["next_text"]["token_cnt"]
        previous_text, previous_token_cnt =\
            truncate_by_token_cnt(
                previous_shorten_output, lang_model,
                math.floor(current_text_token_target * previous_text_token_ratio), from_back=False
            )

        logger.typewriter_log(
            f"Shortening chunk {i + 1} / {len(chunks)}",
            Fore.LIGHTYELLOW_EX
        )
        logger.typewriter_log(
            f"| {len(current_text)} -> {math.floor(len(current_text) * shorten_ratio)} characters."
        )
        logger.typewriter_log(
            f"| {current_token_cnt} -> {math.floor(current_token_cnt * shorten_ratio)} tokens."
        )

        logger.typewriter_log(
            "Referencing",
            Fore.YELLOW
        )
        logger.typewriter_log(
            f"| Previous text | Length: {len(previous_text)} characters, Tokens: {previous_token_cnt} tokens"
        )
        logger.typewriter_log(
            f"| Next text | Length: {len(next_text)} characters, Tokens: {next_token_cnt} tokens"
        )

        messages = [
            {
                "role": "system",
                "content": f"You are a text revise assistant. "
                           f"Text chunks are serving sequently and current chunk is "
                           f"number {i+1} of total {len(chunks)} chunks. "
                           f"The \"Previous Text\" will be placed before your output, do not rephrase it. "
                           f"The \"Next Text\" will be placed after your output, do not rephrase it. "
                           f"Consider your output to be smoothly joined with those texts."
            },
            {
                "role": "user",
                "content": f"\"Revise the \"Current Text\" to exact "
                           f"{math.floor(current_token_cnt * shorten_ratio)} "
                           f"words as you can. "
                           f"Meanwhile, retain important key information "
                           f"and the form of the original text as you can.\" "
                           f"\"Current Text\": \"\"\"{current_text}\"\"\" "
                           f"\"Previous Text\": \"\"\"{previous_text}\"\"\" "
                           f"\"Next Text\": \"\"\"{next_text}\"\"\""
            }
        ]

        with Spinner("Shortening..."):
            shorten_current_text = create_chat_completion(
                messages=messages,
                lang_model=lang_model,
                temperature=CFG.model_temperature,
                top_p=CFG.model_top_p,
                presence_penalty=CFG.model_presence_penalty,
                frequency_penalty=CFG.model_frequency_penalty
            )
        shorten_text_list.append(shorten_current_text)
        tokens_for_shorten_text = count_string_tokens(shorten_current_text, lang_model)
        previous_shorten_output = shorten_current_text

        logger.typewriter_log(
            f"Shortened chunk {i + 1} / {len(chunks)}",
            Fore.GREEN,
        )
        logger.typewriter_log(
            f"| Length: {len(shorten_current_text)} characters, Tokens: {tokens_for_shorten_text} tokens"
        )
        print()

    combined_shorten_text = "\n".join(shorten_text_list)
    tokens_for_shorten_text = count_string_tokens(combined_shorten_text, lang_model)

    logger.typewriter_log(
        "Shortened text result",
        Fore.LIGHTGREEN_EX
    )
    logger.typewriter_log(
        f"| {len(text)} -> {len(combined_shorten_text)} characters "
        f"| Shortened to {len(combined_shorten_text) / len(text) * 100:.2f} %"
    )
    logger.typewriter_log(
        f"| {text_token_cnt} -> {tokens_for_shorten_text} tokens "
        f"| Shortened to {tokens_for_shorten_text / text_token_cnt * 100:.2f} %"
    )

    return combined_shorten_text


if __name__ == "__main__":
    _file_path = input("file_path: ")
    _text = read_textual_file(_file_path)
    result = shorten_text(_text, _file_path)
