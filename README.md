# Applied Deep Learning
Teodor Chakarov - 12141198

## Assignment 1
### Topic and Project Type
For this course, I have decided to do: **project type** - Bring your own method and **topic** - Natural Language Processing and more specific, Text Generation.

### Project summary
#### Introduciton
I am interested in the NLP field of deep learning since ChatGPT made a complete breakthrough in the IT sector. With its capabilities, people are using it for almost anything from code generation to saving time with template generation, math, text summarization, text classification, text manipulation, and more.

The problem comes when companies want to use the model, but since it is open source and in the cloud. There is no on-premise solution for big companies to use it locally for their everyday jobs (to accelerate their work and be helpful) without sending secret and sensitive information to the cloud (due to GDPR regulations). 

July, 18 2023, Meta released a model named LLAMA 2. They released several models 7B, 13B and 70B parameters as the 70B one has capabilities almost like GPT3.5. The advantage for this model is that people can donwload the weights of the model and use it locally. That means that organisations can use a private ChatGPT which can accelerate the work for the empolyees without sending sensitive data to the cloud. 

#### My approach
I will use this model and train it for text generation, to see how can this model be further fine-tuned, how much computer resource I will need in order to do that and to evaluate if the model can be easily adaptive to new data and task.

#### My Data
I tested the model for its capabilities on generating text other than English and the result was far from the expected.(https://www.llama2.ai/)

For my project, I want to try fine-tuning LLAMA 2 model using Bulgarian text data (as I am Bulgarian) and try to make the model generate bulgarian text (gramatically correct, with well-put sentances and guides). The data itself is recepies which were being collected from a [recepies website](https://receptite.com/) as well as the [Kaggle Dataset](https://www.kaggle.com/datasets/auhide/bulgarian-recipes-dataset/)


#### Expected work-breakdown 
I expect the the most time-consuming part to be text preparation and making it in a style of LLAMA 2 fine-tuning guidlines. How should the input text be structured and formulated and in what kind of taks should the model be learned?

Then I need to download the LLAMA 2 weights from the offical [Meta website](https://ai.meta.com/llama/) and with help of [Hugginface Framework](https://huggingface.co/docs/transformers/main/model_doc/llama2), try to fine-tune the model with the proivded data. The time for the trianig will be unknowed as no so much information exists at the time.

As the last steps, the model should be tested with given data as well as new data for generation general Bulgarian text as well as cooking-specific topicss. 

### Papers for this project
 - [Attention is All You Need](https://arxiv.org/abs/1202.4347)
 - [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288)
 - [LoRa: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
 - [GPGPU Processing in CUDA Architecture](https://arxiv.org/abs/1202.4347)


## Assignment 2
Note: For assignment 2 I tried using the specified model on Colab but the training and using it couldn't run on the GPU memory. That's why I am using AWS infrastructure with GPU 25GB RAM and CUDA availability.

From 00_English_LLAMA.ipynb I saw how bad the original LLAMA model is at text generation is different than the English language (Lack of knowledge of the Bulgarian language and lack of text generation when I write in Bulgarian). 

In that sense, as a metric I want to evaluate, as a native speaker, if the trained model will:
Be forced to generate grammatically correct sentences that make sense.
Check if the model can specialize in recipe generation (since the picked dataset is focused on that aspect).
If the model can generate text on other general topics than cocking.

As an achievable metric, I want to aim for at least text generation in Bulgarian (no matter how grammatically correct will be) because based on the first notebook we see a lack of proper Bulgarian generation whatsoever.

In notebook 03_Load_using_model.ipynb we can see the result of fine-tuning the model which positively surprised me. It not only achieved grammatically correct text generation in Bulgarian language but also generated cooking recipes that are different from the expected ones BUT the ingredients make sense based on the dish, which shows not high over-fitting but actually understanding the ingredients and the meals themselves.
Example:
From the given instruction they propose to cook chocolate candies with cherry syrup  (Пияни вишни) but the generated text proposes to make Biscuit cake with cherry syrup (Бисквитена торта с вишни).

As a problem I see some generations at the end I have one sentence repeating itself again and again but you can concur the problem with maximum words for the generation parameter.

Another problem is for funny recipes generated for example:
Real recipe: Spanish sauce with veggies which is cooked with bacon
Generated recipe: Soup with bacon and wine. 
Interesting in this situation is the accuracy of using the same ingredients.

The amount of time spent on this project is:
 - Data pre-processing = 2h.
 - Creating python env running successfully the environment = 4h.
 - Reading documentation and code implementation = 5h.
 - Training the model = 12h.
 - Testing and evaluation of the model = 3h.