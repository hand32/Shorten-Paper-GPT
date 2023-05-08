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

Now, you can input the instruction to each file!
![image](https://user-images.githubusercontent.com/38789681/236756791-08e56536-ce04-4ad5-8462-6bcbca417b02.png)

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

I recommend to repeat the shortening process (`SHORTEN_REPEAT`)
rather than adjust extremely small shorten ratio (`SHORTEN_RATIO`)
for the extremely long document. However, it will cost more accordingly.💸

## Text Settings (.env)
The following are the available text settings that can be adjusted in the `.env` file:

#### SHORTEN_REPEAT (int): bigger than 0
Shorten provided document in `SHORTEN_RATIO` ratio of token length 
and repeat it `SHORTEN_REPEAT` times.
In conclusion, the document will be
shortened in (`SHORTEN_RATIO` ** `SHORTEN_REPEAT`) ratio of token length.\
Usually, I use 3-5 for the academic papers.\
The default value is 3.\
❗ However, it will cost more accordingly.💸

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
* `TEXT_TOKEN_LEN` (int) : [Max Token List](https://platform.openai.com/docs/models/gpt-3-5)
* `MODEL_TEMPERATURE` (float) : `[0, 2]`
* `MODEL_TOP_P` (float) : `[0, 1]`
* `MODEL_PRESENCE_PENALTY` (float) : `[-2, 2]`
* `MODEL_FREQUENCY_PENALTY` (float) : `[-2, 2]`

## Result Comparison Sample
#### Target Paper
* [VR-HandNet: A Visually and Physically Plausible Hand Manipulation System in Virtual Reality](https://doi.org/10.1109/TVCG.2023.3255991)
#### Shortened Full Paper .pdf (`SHORTEN_REPEAT=5`, `SHORTEN_RATIO=0.4`)
This study introduces a new method for manipulating virtual objects using VR-HandNet.
It maps the VR controller to the virtual hand and uses a deep neural network
to determine desired joint orientations of the virtual hand model at each frame
based on information about the virtual hand, VR controller input, 
and hand-object spatial relations. The proposed approach combines 
reinforcement learning-based training with imitation learning paradigm that increases 
visual plausibility by mimicking reference motion datasets. To evaluate this approach,
424 training datasets having 50,100 frames and 247 test datasets having 30,332 frames
were collected using Oculus Quest HMDs/controllers under Unity engine implementation
with Nvidia PhysX4.1 simulated physical skeletal models having capsule/box colliders 
detecting collision between hands/objects were used. The evaluation section classified 
test datasets into primitive-level objects (PL), scaled-primitive-level objects (SPL), 
and complex level objects (CL) further classified into reference pose (RP) 
and reference object (RO). This paper provides valuable insights into collecting
reference motion data for virtual reality applications while introducing a promising 
approach to dexterous manipulation using physics-based approaches and deep reinforcement learning algorithms.
#### Paper's Original Abstract
This study aims to allow users to perform dexterous hand manipulation of objects in virtual environments with hand-held VR
controllers. To this end, the VR controller is mapped to the virtual hand and the hand motions are dynamically synthesized when the
virtual hand approaches an object. At each frame, given the information about the virtual hand, VR controller input, and hand-object
spatial relations, the deep neural network determines the desired joint orientations of the virtual hand model in the next frame. The
desired orientations are then converted into a set of torques acting on hand joints and applied to a physics simulation to determine the
hand pose at the next frame. The deep neural network, named VR-HandNet, is trained with a reinforcement learning-based approach.
Therefore, it can produce physically plausible hand motion since the trial-and-error training process can learn how the interaction
between hand and object is performed under the environment that is simulated by a physics engine. Furthermore, we adopted an
imitation learning paradigm to increase visual plausibility by mimicking the reference motion datasets. Through the ablation studies, we
validated the proposed method is effectively constructed and successfully serves our design goal. A live demo is demonstrated in the
supplementary video.

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