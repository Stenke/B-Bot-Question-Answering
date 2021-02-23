from transformers import (WEIGHTS_NAME, DistilBertConfig,DistilBertForQuestionAnswering, DistilBertTokenizer)
from prediction_utils import (read_squad_examples, convert_examples_to_features, to_list, write_predictions)
from torch.utils.data import (DataLoader, SequentialSampler, TensorDataset)
from download import download_model
from pathlib import Path
import numpy as np
import collections
import requests
import logging
import torch
import math
import os

RawResult = collections.namedtuple("RawResult",
                                   ["unique_id", "start_logits", "end_logits"])


class Model:

    def __init__(self, path: str):
        self.max_seq_length = 384
        self.doc_stride = 128
        self.max_query_length = 64
        self.do_lower_case = True
        self.n_best_size = 20
        self.max_answer_length = 30
        self.eval_batch_size = 1
        self.model, self.tokenizer = self.model_load(path)
        self.model.eval()

    def model_load(self, path):

        s3_model_url = 'https://distilbert-finetuned-model.s3.eu-west-2.amazonaws.com/pytorch_model.bin'
        path_to_model = download_model(s3_model_url, model_name="pytorch_model.bin")

        config = DistilBertConfig.from_pretrained(path + "/config.json")
        tokenizer = DistilBertTokenizer.from_pretrained(path, do_lower_case=self.do_lower_case)
        model = DistilBertForQuestionAnswering.from_pretrained(path_to_model, from_tf=False, config=config)

        return model, tokenizer

    def answer_question(question, answer_text):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.
    input_ids = tokenizer.encode(question, answer_text)

    # Report how long the input sequence is.
    print('Query has {:,} tokens.\n'.format(len(input_ids)))

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    # ======== Evaluate ========
    # Run our example question through the model.
    start_scores, end_scores = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                    token_type_ids=torch.tensor([segment_ids])) # The segment IDs to differentiate question from answer_text

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):
        
        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        
        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]

    print('Answer: "' + answer + '"')

model = Model('model')
