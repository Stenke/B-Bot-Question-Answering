  <img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/Screen%20Shot%202021-03-02%20at%204.39.38%20PM.png" width="500"   length="700" />

## BERT-Based QA Model with Curated Datasets and ElasticSearch in Mind

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

<img src="this is model arch" width="900" length="700"/>

After Ada is done learning, we look at the loss and validate the model on the test set. Below are the results after one epoch.

##### Loading model and looking at the architecture
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/training-arch.png" width="900" length="700"/>

##### Looking at the loss (log loss on the softmax layer)
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/training-loss-2.png" width="900" length="700"/>

##### And finally, the results.
<img src="https://github.com/Stenke/B-Bot-Question-Answering/blob/main/Images/train-score.png" width="900" length="700"/>


