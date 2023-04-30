# Shorten Paper

###### _For convenience, apart of response time has been omitted from the demo. Shortening text is time-consuming due to the language model process. The actual response time will be longer than shown in the demo._

[Demo_Video.mp4](https://user-images.githubusercontent.com/38789681/235345894-9c5c886f-df3d-46cc-a110-1e89ef93beff.mp4)


**Shorten Paper** is a Python project that utilizes language models like GPTs 
to shorten highly lengthy documents while retaining important information.

Language models have a max token length in each call.

Therefore, **Shorten Paper** breaks down the given text into smaller chunks 
to handle lengthy texts with language model, preserving their coherence and flow, 
even after being split into smaller parts.

Also, you can adjust the shorten ratio of the given text length and 
the ratio of previous/next text chunk to be included in an api call.


## Requirements

* Docker-Compose - [Install Guide](https://docs.docker.com/compose/install/)
* OpenAI API Key - [Configure API Key](https://platform.openai.com/account/api-keys)

## Usage
To use **Shorten Paper**, follow these simple steps:
1. Clone this repository to your local machine.
2. Add your OpenAI API key to the `OPENAI_API_KEY` field in the `.env` file.
3. Modify the `PAPERS_INPUT_DIR`, `PAPERS_OUTPUT_DIR`, and `OUTPUT_PREFIX` fields in the `.env` file if necessary.
4. Place the target paper(s) in the `PAPERS_INPUT_DIR`.
5. Run `'run - mac, linux.sh'` for Mac/Linux or `'run - windows.bat'` for Windows to build and run the Docker container at the root project directory.

After building and running the Docker container, 
the program will automatically start running. 
It will read in all the text files in the `PAPERS_INPUT_DIR`,
shorten them using the specified language model, 
and save the shortened versions to the `PAPERS_OUTPUT_DIR`.

The shortening settings can be modified in the `.env` file.

**Shorten Paper** currently supports text files with the following extensions: 
`.txt, .csv, .pdf, .doc, .docx, .json, .xml, .yaml, .html, .md, .tex`.

For optimal results, ensure that your document is well-organized and 
follows a logical structure. A well-ordered document will 
lead to a higher quality of shortening, allowing the program 
to preserve important information while reducing the overall length.

## Text Settings (.env)
The following are the available text settings that can be adjusted in the `.env` file:

#### SHORTEN_RATIO (float): (0, 1]
The shortening ratio of the original text.\
The default value is 0.4.

#### PREVIOUS_TEXT_TOKEN_RATIO (float): [0, 1)
The ratio of the previous text to include when split
the input text for the language model.
0 means to exclude the previous text in the shortening process.\
The default value is 0.4.

#### NEXT_TEXT_TOKEN_RATIO (float): [0, 1)
The ratio of the next text to include when split 
the input text for the language model.
0 means to exclude the next text in the shortening process.\
The default value is 0.2.

Additionally, you can consider to fine-tune the language model parameters
for the better output quality:
* `LANG_MODEL_NAME` (str) : [Models](https://platform.openai.com/docs/models/model-endpoint-compatibility)
* `TEXT_TOKEN_LEN` (int) : [Max token list](https://platform.openai.com/docs/models/gpt-3-5)
* `MODEL_TEMPERATURE` (float) : `[0, 2]`
* `MODEL_TOP_P` (float) : `[0, 1]`
* `MODEL_PRESENCE_PENALTY` (float) : `[-2, 2]`
* `MODEL_FREQUENCY_PENALTY` (float) : `[-2, 2]`

## Credits
**Shorten Paper** was developed by _**Han DongHeun**_ and using the language model 
provided by OpenAI, 
inspired by [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)

This project is my personal project for personal usage. 

As you know, this kind of language agent highly relies on the language model's ability. 
So, I can't guarantee that it will always give you a high quality shortened result.
Though, this project can be useful if you kindly fine-tune the parameters 
and clearly organize your document structure for your certain situation.

Hope this project will be helpful for your research or studies,
or whatever purpose you may have.

_**Thank you for enjoying my work!**_