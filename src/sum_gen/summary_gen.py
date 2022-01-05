import re
import torch
import os
import random
import keras
import numpy as np
import pandas as pd
from rouge import Rouge
nlp = spacy.load('en_core_web_sm')
from keras.models import Model, Input
from sentence_transformers import SentenceTransformer
from keras.callbacks import EarlyStopping, ModelCheckpoint
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from keras.layers import Dense, Input, LayerNormalization, LSTM, Dropout, Bidirectional
from keras import initializers, regularizers, constraints, optimizers, layers, models, losses

transformerSource = 'paraphrase-distilroberta-base-v1' 


def gen_abs_summary(text):

    model = PegasusForConditionalGeneration.from_pretrained('akshara23/Pegasus_for_Here')
    tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-cnn_dailymail')
    ARTICLE_TO_SUMMARIZE = str(text)
    inputs = tokenizer([ARTICLE_TO_SUMMARIZE], max_length=1024, return_tensors='pt')
    summary_ids = model.generate(inputs['input_ids'])
    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    summary = "".join(summary)
    summary = summary.replace("<n>","")
    summary = summary.replace("</n>","")
    return summary


def embedding_text(report_text):

    embedder = SentenceTransformer(transformerSource)
    text_sentences = nlp(report_text)
    array=[]
    for sentence in text_sentences.sents:
      array.append(sentence.text)
    sentences = np.array(array)
    df = pd.DataFrame(sentences,columns=['text'])

    df['embedded_data'] = (df['text']
                 .apply(lambda x: np.array(embedder.encode(x, convert_to_tensor=True), dtype="float"))
                 .values)
    return df

def gen_ext_sum(report):

    reconstructed_model = keras.models.load_model("final_model_h5") 
    dataframe = embedding_text(report)  
    dat_ = np.array([x for x in dataframe["embedded_data"]],dtype="float")
    dat_ = dat_.reshape(len(dat_),1,768)
    pred = reconstructed_model.predict(dat_)
    pred_result_list = []
    dataframe["Pred"] = pred
    pred_w_hgen_sen = (dataframe.sort_values("Pred", ascending=False).head(4)["text"].values) 

    return ".".join(pred_w_hgen_sen)



