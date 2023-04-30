import os
from shorten_paper.file_operations_utils import (shorten_text, read_textual_file)

from colorama import Fore
from shorten_paper.logs import Logger
from shorten_paper.config import Config

logger = Logger()
CFG = Config()


def main() -> None:
    logger.typewriter_log(
        "-* Start Shorten Paper *- by. Han DongHeun",
        Fore.LIGHTRED_EX
    )

    logger.typewriter_log(
        "File input path:",
        Fore.LIGHTYELLOW_EX,
        CFG.papers_input_dir
    )
    logger.typewriter_log(
        "File output path:",
        Fore.LIGHTYELLOW_EX,
        CFG.papers_output_dir
    )
    files = os.listdir(CFG.papers_input_dir)

    logger.typewriter_log(
        "Target files",
        Fore.LIGHTCYAN_EX
    )
    for num, document_name in enumerate(files):
        logger.typewriter_log(f"| {num+1} - {document_name}")

    print()
    shorten_result_info = []
    for num, document_name in enumerate(files):
        logger.typewriter_log(
            "File num:",
            Fore.CYAN,
            f"{num+1}/{len(files)}"
        )
        shorten_result_info.append(("ERROR!", "ERROR!"))
        document_output_name = "Error: Didn't saved."
        try:
            document_text = read_textual_file(os.path.join(CFG.papers_input_dir, document_name))
            shorten_result_info[-1] = (len(document_text), "ERROR!", document_output_name)
            shortened_text = shorten_text(document_text, document_name)
            shorten_result_info[-1] = (len(document_text), len(shortened_text), document_output_name)
        except ValueError as e:
            logger.error(f"ValueError with file {document_name}:", f"{e}")
            continue

        if not os.path.exists(CFG.papers_output_dir):
            os.mkdir(CFG.papers_output_dir)
        document_name_pure = os.path.splitext(document_name)[0]
        attempt = 10000
        counter = 0
        while attempt > 0:
            attempt -= 1

            document_output_name = "".join([CFG.output_prefix, document_name_pure,
                                            f"_{len(shortened_text) / len(document_text):.2f}%",
                                            "" if counter == 0 else f"_({counter})", "_.txt"])
            document_output_full_path = os.path.join(CFG.papers_output_dir, document_output_name)
            if os.path.exists(document_output_full_path):
                counter += 1
                continue

            with open(document_output_full_path, "w") as f:
                f.write(shortened_text)
            shorten_result_info[-1] = (len(document_text), len(shortened_text), document_output_name)
            logger.typewriter_log(
                "Save shortened text to file",
                Fore.BLUE
            )
            logger.typewriter_log(
                f"| File name: {document_output_name}"
            )
            logger.typewriter_log(
                f"File num {num+1} done!",
                Fore.CYAN,
            )
            print()
            break
        if attempt <= 0:
            logger.error(f"File Save Error: {document_name} did not saved until 10,000 attempts in certain reason.")

    logger.typewriter_log(
        f"Shortening {len(files)} files done!",
        Fore.CYAN
    )
    for num, document_name in enumerate(files):
        current_doc_text_len = shorten_result_info[num][0]
        current_shorten_text_len = shorten_result_info[num][1]
        logger.typewriter_log(f"File {num+1}:",
                              Fore.CYAN,
                              f"{document_name}")
        if isinstance(current_doc_text_len, int) and isinstance(current_shorten_text_len, int):
            logger.typewriter_log(f"| Output file name: {shorten_result_info[num][2]}")
            logger.typewriter_log(f"| Shorten characters: {current_doc_text_len} -> {current_shorten_text_len}")
            logger.typewriter_log(
                f"| Shortened to {current_shorten_text_len / current_doc_text_len * 100:.2f} %"
            )
        else:
            logger.typewriter_log("| ERROR! Not shortened.")


if __name__ == "__main__":
    main()
