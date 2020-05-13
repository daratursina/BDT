# -*- coding: utf-8 -*-

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
import numpy as np
import unicodedata as ud
from pyarabic.araby import strip_tashkeel
import string

def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("\[", "", text)
    text = re.sub("\]", "", text)
    return(text)
    
print("START READ AND PREPROCESSING")
#sentence_clear = []

""" 
directory = '/content/drive/My Drive/TA/dataset/'
kitab=[]
datakitab = 1;
for filename in os.listdir(directory):
    print(filename)
    for filecsv in os.listdir(directory+'/'+filename):
        print(filecsv)
        print(datakitab)
        datakitab = datakitab + 1
        with open(directory+'/'+filename+'/'+filecsv, encoding='cp1256') as csvFile:
            next(csvFile)
            reader = csvFile.readlines()
            # get number of columns
            count = 1
            for i in range(len(reader)):
            #for i in range(1000):
                r = reader[i]
                if count % 100 == 0:
                    print(count)
                
                token = word_tokenize(r)
                
                token_clear = []
                for t in token:
                    norm = normalizeArabic(t)
                    
                    token_clear.append(norm)
                
                sentence_clear.append(token_clear)
                
                count += 1
            print("==========DONE==========")
        kitab.append(reader)
 
"""

kitab = np.load('dataset/numpy/kitabsave.npy')
kitab = kitab.tolist()

sentence_clear = np.load('dataset/numpy/sentence_clearsave.npy')
sentence_clear = sentence_clear.tolist()

kategori = np.load('dataset/numpy/kategori.npy')
kategori = kategori.tolist()

namakitab = np.load('dataset/numpy/namakitab.npy')
namakitab = namakitab.tolist()


# processing FastText in Gensim
#print("START PROCESSING EMBEDDING")
#from gensim.models import FastText

#modelFT = FastText(sentence_clear, size=100, window=5, min_count=2, sg=1)

# save model
#modelFT.save('/content/drive/My Drive/TA/Model/modelFT.model')



# load model
modelFT = ft.load('Model/modelFT.model')

# MOST SIMILAR WE
hasilQE = modelFT.wv.most_similar("ولد")

hasilQE = [(strip_tashkeel(''.join(c for c in hasilQE[i][0] if not ud.category(c).startswith('P'))), hasilQE[i][1]) for i in range(len(hasilQE))]
print(hasilQE)

#TF-IDF
tfidf_vectorizer = TfidfVectorizer()


isikitab=''
ktb=[]
for i in range(len(kitab)):
    for j in kitab[i] :
        isikitab = ''.join(kitab[i])
    ktb.append(isikitab)
    
norm_tf=[]
for i in range(len(ktb)):
    norm_tfidf = normalizeArabic(ktb[i])
    norm_tf.append(norm_tfidf)

tfidf_doc = tfidf_vectorizer.fit_transform(norm_tf)

tfidf_word=tfidf_vectorizer.get_feature_names()

PIFQvectorizer = CountVectorizer()
vectoreTF = PIFQvectorizer.fit_transform(norm_tf)
featureTf = PIFQvectorizer.get_feature_names()

cosim = []
hasilpifq = []
hasilgabungan = []
nilaihasilgabungan = []
nilaihasilpifq = []
nilaicosim = []
for i in hasilQE:
  #DOKUMEN PALING RELEVAN
  # print(i[0])
  #QUERY
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
  if len(countTF) < 1 :
    for j in range(vectoreTF.shape[0]):
      countTF.append(0.0)

  # print('count ' + str(len(countTF)))

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
  
print("====== hasil pifq ==========")
angka = 0
for i in nilaihasilpifq:
  print(hasilQE[angka][0])
  if hasilpifq[angka] > 1:
    for j in range(len(i)):
      if i[j] == hasilpifq[angka]:
        print(kategori[0], '-', namakitab[j], '-', i[j])
        # if j < 21:
        #   print(kategori[0], '-', namakitab[j], '-', i[j])
        # else:
        #   print(kategori[1], '-', namakitab[j], '-', i[j])
  angka += 1
  
print("======= hasil Cosim ===========")
angka = 0
for i in nilaicosim:
  print(hasilQE[angka][0])
  for j in range(len(i)):
    if i[j] == cosim[angka]:
      print(kategori[0], '-', namakitab[j], '-', i[j])
      # if j < 21:
      #   print(kategori[0], '-', namakitab[j], '-', i[j])
      # else:
      #   print(kategori[1], '-', namakitab[j], '-', i[j])
  angka += 1
  
print("============== Hasil Gabungan ===============")
angka = 0
for i in nilaihasilgabungan:
  print(hasilQE[angka][0])

  if hasilgabungan[angka] > 0:
    for j in range(len(i)):
      if i[j] == hasilgabungan[angka]:
        print(kategori[0], '-', namakitab[j], '-', i[j])
        # if j < 21:
        #   print(kategori[0], '-', namakitab[j], '-', i[j])
        # else:
        #   print(kategori[1], '-', namakitab[j], '-', i[j])
  angka += 1