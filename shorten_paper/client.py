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
    instructions = []
    for num, document_name in enumerate(files):
        logger.typewriter_log(f"| {num+1} - {document_name}")
        instructions.append(input("| Enter the instruction (None to just shorten): ").strip())

    print()
    shorten_result_info = []
    for repeat_num in range(CFG.shorten_repeat):
        if CFG.shorten_repeat > 1:
            logger.typewriter_log(
                "Shortening repeat num:",
                Fore.RED,
                f"{repeat_num+1}/{CFG.shorten_repeat}"
            )
        if repeat_num > 0:
            files = [previous_result[2] for previous_result in shorten_result_info]
            shorten_result_info = []
        for num, document_name in enumerate(files):
            logger.typewriter_log(
                "File num:",
                Fore.CYAN,
                f"{num+1}/{len(files)}"
            )
            shorten_result_info.append(("ERROR!", "ERROR!", "ERROR!"))
            document_output_name = "Error: Didn't saved."
            try:
                input_dir = CFG.papers_input_dir if repeat_num == 0 else CFG.papers_output_dir
                document_text = read_textual_file(os.path.join(input_dir, document_name))
                shorten_result_info[-1] = (len(document_text), "ERROR!", document_output_name)
                shortened_text = shorten_text(document_text, document_name, instructions[num])
                shorten_result_info[-1] = (len(document_text), len(shortened_text), document_output_name)
            except ValueError as e:
                logger.error(f"ValueError with file {document_name}:", f"{e}")
                print()
                continue

            if not os.path.exists(CFG.papers_output_dir):
                os.mkdir(CFG.papers_output_dir)
            document_name_pure = os.path.splitext(document_name)[0]
            attempt = 10000
            counter = 0
            while attempt > 0:
                attempt -= 1

                document_output_name = "".join([CFG.output_prefix if repeat_num == 0 else "",
                                                document_name_pure,
                                                f"_{len(shortened_text) / len(document_text) * 100:.2f}%",
                                                "" if counter == 0 else f"_({counter})", ".txt"])
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
        print()

    logger.typewriter_log(
        "Jobs all done. Anything else?",
        Fore.LIGHTBLUE_EX
    )
    logger.typewriter_log(
        "Visit",
        Fore.LIGHTBLUE_EX,
        "https://github.com/hand32/Shorten-Paper"
    )
    logger.typewriter_log(":)")


if __name__ == "__main__":
    main()
