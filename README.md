  <img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/Screen%20Shot%202021-03-02%20at%204.39.38%20PM.png" width="500"   length="700" />

## BERT-Based QA Model with Curated Datasets and ElasticSearch in Mind
<p align="center">
  <img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/ada.png" width="300"   length="600" />
</p>
Ada.ai aims to reduce human bias by scaling vulnerable questions and honest answers provided by professionals. Using a question-answering model based on the BERT model and fine-tuned on the SQuAD 2.0 dataset. Next steps include domain-specific QA datasets for fine-tuning, long-form context scripts sourced from podcast transcripts and online articles, and an ElasticSearch framework for document retrieval best suited for answering a user's question.

## Current Problem
The first two decades of this century showed us the risks of siloed dialogue.
Countless events surprised some portion of the population - the truth being hidden in plain sight.
Yet, even after we acknowledged the misalignment, words were left unsaid.

##### The problem is we’re afraid to ask the questions that matter.

There are wonderful podcasts, books, and blogs that address some of the most sensitive issues: sex, race, religion, politics, etc.
Though these are great resources, they lack the intimacy of dialogue and the self-reflection inherent in asking a vulnerable question.
Ada.ai intends to promote these conversations at scale.


## The Data
The BERT model was pre-trained on unlabeled data from the BookCorpus and English Wikipedia articles boasting 800M and 2,500M words respectively. Further fine-tuning to add an additional layer and teach Ada the ways of QA was done using Stanford's SQuAD 2.0 dataset. This is composed of 150,000 questions from 500+ Wiki articles that were created by Mechanical Turk users. The version 2.0 included questions with no answers, which is important when performing QA in the wild.
 
 <img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/squad-ex.png" width="1000"   length="1200" />

Additional data was webscraped from Brené Brown's podcast transcripts. The intention of these 41 transcripts is to be used for both creating domain-specific QA dataset for further fine-tuning as well as articles for our document retrieval system.

 <img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/bb-transcript.png" width="600"   length="800" />
 
 ## Methods + Testing
The pre-trained model was sourced using Huggingface's transformer library. For our case, we used the BertForQuestionAnswering import along with its related tokenizers. Additionally, Huggingface provides a library imports for working with the SQuAD datasets. Below is an example of converting strings to tokens and masking certain tokens to add a bit of chaos to the learning process.

<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/Screen%20Shot%202021-03-02%20at%207.20.31%20PM.png" width="900" length="700"/>

Following the data tokenizing, class tagging [CLS] and [SEP], and parameter initialization, we send the model out to study.

<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/Screen%20Shot%202021-03-02%20at%207.20.31%20PM.png" width="900" length="700"/>

After Ada is done learning, we look at the loss and validate the model on the test set. Below are the results after one epoch.

##### Loading model and looking at the architecture
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/training-arch.png" width="800" length="600"/>

##### Looking at the loss (log loss on the softmax layer)
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/training-loss-2.png" width="850" length="600"/>

##### And finally, the results.
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/train-score.png" width="300" length="300"/>

Our main scores here are the exact match and F1. Exact match is where our answer is taken straight from the context and matches word for word in order. Here we ended up with a 68.5% exact match rate after the first epoch. F1-score is a little tricker; we're looking at the number of shared words in our model's prediction and the actual answer as provided in the test set. Recall is the ratio of shared words (between predicted and actual answer) over the total number of words in the true answer. Precision here is the ratio of shared words over the total number of words in the prediction.

# Findings
Here's a quick peak at the at Ada in action. After defining an answer_question function, we feed in context (limited to 512 tokens) and question. After that, Ada assigns most likely start words probabilistically and then the final word. The answer is composed of the most likely tokens in sequential order. Check it out!

##### Context
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/context_ada.png" width="2000" length="1500"/>

##### Answer
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/context_ada.png" width="600" length="400"/>

The results here are pretty good and even more impressive with a nice front-end using Flask or Dash. Since the model is pre-loaded, the QA process is actually quite fast - good when considering using this model in the wild.


## Conclusion
We see Ada.ai as a non-profit that can levarage professionally curated datasets addressing sensitive issues that most of us just aren't talking enough about. Looking forward, we aim to build a pleasant front-end. Additionally, a product like this would rely heavily on a query ability with document retrieval. That way user asks a question, the best document is retrieved, an answer is sourced, and provided to the user.

In AI, we worry about bias. We should. 

But as we work to eliminate biases in AI, we forget how AI can reduce bias in humans.

And in the words of Brene Brown, “we’re not here to get it right - we’re here to be right”.

##### Ada achieves this at scale.

<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/sometimes-I-start.gif" width="600" length="400"/>


