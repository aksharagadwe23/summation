import re
import os
import string
import nltk

nltk.download('words')
words = set(nltk.corpus.words.words())

def sub_words(text):
    text = remove_numbers(text)

    text = re.sub(r'\\n|\\t',' ',text)
    text = re.sub("\s\s+", " ", text)
    text = re.sub(r"[\[0-9]+[\]]","",text)
    text = re.sub("<!--?.*?-->","",text)
    text = re.sub(r"\s+"," ",text)
    text = re.sub(r"\d{7,}","", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s##\w*\s"," ", text)
    text = re.sub(r"(<[^<>]*>)|(&\w+;)"," ",text)
    text = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?','',text)
    text = re.sub(r'(@)[\w_-]+','',text)
    text = re.sub(r"'s"," is",text)
    text = re.sub(r"'ll"," will",text)
    text = re.sub(r"'m"," am",text)
    text = re.sub(r"can't","can not",text)
    text = re.sub(r"don't","do not",text)

    return text


def pre_process(text):
    text_abs = text.lower()
    text_abs = sub_words(text_abs)
    text_ext = sub_words(text)

    for w in nltk.wordpunct_tokenize(text_abs):
      if w not in words or not w.isalnum():
        nltk.wordpunct_tokenize(text_abs).remove(w)

    for w in nltk.wordpunct_tokenize(text_ext):
      if w not in words or not w.isalnum():
        nltk.wordpunct_tokenize(text_ext).remove(w)

    
    return text_abs,text_ext

def remove_numbers(string):
  strings = string.split(" ")
  for word in strings:
    if word.isnumeric():
      if len(word) > 5:
        strings.remove(word)
  return " ".join(strings)