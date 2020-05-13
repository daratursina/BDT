#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import csv
import nltk
from nltk.corpus import stopwords
import pandas as pd
import re
from smart_open import open
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from gensim.models import FastText as ft
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import unicodedata as ud
from pyarabic.araby import strip_tashkeel
import string


# In[2]:


def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("\[", "", text)
    text = re.sub("\]", "", text)
    return(text)
    
print("START READ AND PREPROCESSING")


# In[5]:


kitab = np.load('dataset/numpy/kitabsave.npy', allow_pickle=True)
kitab = kitab.tolist()

sentence_clear = np.load('dataset/numpy/sentence_clearsave.npy', allow_pickle=True)
sentence_clear = sentence_clear.tolist()

kategori = np.load('dataset/numpy/kategori.npy', allow_pickle=True)
kategori = kategori.tolist()

namakitab = np.load('dataset/numpy/namakitab.npy', allow_pickle=True)
namakitab = namakitab.tolist()


# In[6]:


kitab[0][1]


# In[7]:


modelFT = ft.load('Model/modelFT.model')

# MOST SIMILAR WE
hasilQE = modelFT.wv.most_similar("ولد")

hasilQE = [(strip_tashkeel(''.join(c for c in hasilQE[i][0] if not ud.category(c).startswith('P'))), hasilQE[i][1]) for i in range(len(hasilQE))]
print(hasilQE)


# In[10]:


#TF-IDF
tfidf_vectorizer = TfidfVectorizer()

norm_tf=[]
for isikitab in kitab:
    for ktb in isikitab:
        norm_tfidf = normalizeArabic(ktb)
        norm_tf.append(norm_tfidf)


# In[ ]:





# In[11]:


tfidf_doc = tfidf_vectorizer.fit_transform(norm_tf)

tfidf_word=tfidf_vectorizer.get_feature_names()

PIFQvectorizer = CountVectorizer()
vectoreTF = PIFQvectorizer.fit_transform(norm_tf)
featureTf = PIFQvectorizer.get_feature_names()


# In[102]:


cosim = []
hasilpifq = []
hasilgabungan = []
nilaihasilgabungan = []
nilaihasilpifq = []
nilaicosim = []
for i in hasilQE:
    tes=i[0]
    print(tes)

    tfidf_query = tfidf_vectorizer.transform([tes])
    cos=0.0
      #hitung kedekatan query pada masing masing dokumen 
    cos=cosine_similarity(tfidf_doc,tfidf_query)
      # print(type(cos))
    cosim.append(max(cos))
    nilaicosim.append(cos)

      # print('tfidf')
      # ================
    countTF = []
    s = ''.join(c for c in tes if not ud.category(c).startswith('P'))
    s = strip_tashkeel(s)
    for k in range(len(featureTf)):
        if featureTf[k] == s:
          # print(k)
            for j in range(vectoreTF.shape[0]):
                countTF.append(vectoreTF[j,k])
#         if len(countTF) < 1 :
#             for j in range(vectoreTF.shape[0]):
#                 countTF.append(0.0)

      #PIFQ
    nilaipifq = []
    for k in countTF:
        if sum(countTF) == 0:
            nilaipifq.append(0)
        else:
            nilaipifq.append(1 + np.log10(1 + (k / sum(countTF))) + 0.5)
    nilaihasilpifq.append(nilaipifq)
    hasilpifq.append(max(nilaipifq))
      # print('pifq')

      #gabungan
    nilaigabungan = []
    for k in range(vectoreTF.shape[0]):
        nilaigabungan.append(nilaipifq[k] * cos[k][0])
    nilaihasilgabungan.append(nilaigabungan)
    hasilgabungan.append(max(nilaigabungan))
      # print('gabungan')


# In[103]:


print("======= hasil Cosim ===========")
angka = 0
for i in nilaicosim:
    print(hasilQE[angka][0])
    for j in range(len(i)):
        if i[j] == cosim[angka]:
            panjangkitab= 0;
            for iterkitab in range(len(kitab)):
                panjangkitab = panjangkitab + len(kitab[iterkitab])
                if j <= panjangkitab:
                    tessplit = kitab[iterkitab][0].split(',')
                    print('Nama Kitab {} halaman ke {}'.format(namakitab[iterkitab],tessplit[4]))
                    break;
    angka += 1


# In[104]:


print("====== hasil pifq ==========")
angka = 0
for i in nilaihasilpifq:
    print(hasilQE[angka][0])
    for j in range(len(i)):
        if i[j] == hasilpifq[angka]:
            panjangkitab= 0;
            for iterkitab in range(len(kitab)):
                panjangkitab = panjangkitab + len(kitab[iterkitab])
                if j <= panjangkitab:
                    tessplit = kitab[iterkitab][0].split(',')
                    print('Nama Kitab {} halaman ke {}'.format(namakitab[iterkitab],tessplit[4]))
                    break;
    angka += 1


# In[105]:


print("============== Hasil Gabungan ===============")
angka = 0
for i in nilaihasilgabungan:
    print(hasilQE[angka][0])
    for j in range(len(i)):
        if i[j] == hasilgabungan[angka]:
            panjangkitab= 0;
            for iterkitab in range(len(kitab)):
                panjangkitab = panjangkitab + len(kitab[iterkitab])
                if j <= panjangkitab:
                    tessplit = kitab[iterkitab][0].split(',')
                    print('Nama Kitab {} halaman ke {}'.format(namakitab[iterkitab],tessplit[4]))
                    break;
    angka += 1

