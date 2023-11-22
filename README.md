# Applied Deep Learning
Teodor Chakarov - 12141198

## Topic and Project Type
For this course, I have decided to do: **project type** - Bring your own method and **topic** - Natural Language Processing and more specific, Text Generation.

## Project summary
### Introduciton
I am interested in the NLP field of deep learning since ChatGPT made a complete breakthrough in the IT sector. With its capabilities, people are using it for almost anything from code generation to saving time with template generation, math, text summarization, text classification, text manipulation, and more.

The problem comes when companies want to use the model, but since it is open source and in the cloud. There is no on-premise solution for big companies to use it locally for their everyday jobs (to accelerate their work and be helpful) without sending secret and sensitive information to the cloud (due to GDPR regulations). 

July, 18 2023, Meta released a model named LLAMA 2. They released several models 7B, 13B and 70B parameters as the 70B one has capabilities almost like GPT3.5. The advantage for this model is that people can donwload the weights of the model and use it locally. That means that organisations can use a private ChatGPT which can accelerate the work for the empolyees without sending sensitive data to the cloud. 

### My approach
I will use this model and train it for text generation, to see how can this model be further fine-tuned, how much computer resource I will need in order to do that and to evaluate if the model can be easily adaptive to new data and task.

### My Data
I tested the model for its capabilities on generating text other than English and the result was far from the expected.(https://www.llama2.ai/)

For my project, I want to try fine-tuning LLAMA 2 model using Bulgarian text data (as I am Bulgarian) and try to make the model generate bulgarian text (gramatically correct, with well-put sentances and guides). The data itself is recepies which were being collected from a [recepies website](https://receptite.com/) as well as the [Kaggle Dataset](https://www.kaggle.com/datasets/auhide/bulgarian-recipes-dataset/)


### Expected work-breakdown 
I expect the the most time-consuming part to be text preparation and making it in a style of LLAMA 2 fine-tuning guidlines. How should the input text be structured and formulated and in what kind of taks should the model be learned?

Then I need to download the LLAMA 2 weights from the offical [Meta website](https://ai.meta.com/llama/) and with help of [Hugginface Framework](https://huggingface.co/docs/transformers/main/model_doc/llama2), try to fine-tune the model with the proivded data. The time for the trianig will be unknowed as no so much information exists at the time.

As the last steps, the model should be tested with given data as well as new data for generation general Bulgarian text as well as cooking-specific topics. 

## Papers for this project
 - [Attention is All You Need](https://arxiv.org/abs/1202.4347)
 - [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288)
 - [LoRa: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
 - [GPGPU Processing in CUDA Architecture](https://arxiv.org/abs/1202.4347)