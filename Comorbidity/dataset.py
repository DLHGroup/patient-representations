#!/usr/bin/env python

import sys, os
sys.dont_write_bytecode = True
#sys.path.append('/content/drive/MyDrive/DLH_Final_Project/test1/Comorbidity/')

#import utils, 
import i2b2
import pickle
#import numpy
#import configparser, os, nltk, pandas
#import glob, string, operator
import collections

# can be used to turn this into a binary task
LABEL2INT = {'Y':0, 'N':1, 'Q':2, 'U':3}
# file to log alphabet entries for debugging
ALPHABET_FILE = os.path.dirname(sys.path[0])+"/Comorbidity/Model/alphabet.txt"

class DatasetProvider:
  """Comorboditiy data loader"""

  def __init__(self,
               corpus_path,
               annot_xml,
               disease,
               judgement,
               use_pickled_alphabet=False, 
               alphabet_pickle=None,
               min_token_freq=0):
    """Index words by frequency in a file"""

    self.corpus_path = corpus_path
    self.annot_xml = annot_xml
    self.min_token_freq = min_token_freq
    self.disease = disease
    self.judgement = judgement
    self.alphabet_pickle = alphabet_pickle

    self.token2int = {}

    # when training, make alphabet and pickle it
    # when testing, load it from pickle
    if use_pickled_alphabet:
      print ('reading alphabet from', alphabet_pickle)
      pkl = open(alphabet_pickle, 'rb')
      self.token2int = pickle.load(pkl)
    else:
      self.make_token_alphabet()

  def make_token_alphabet(self):
    """Map tokens (CUIs) to integers"""

    # count tokens in the entire corpus
    token_counts = collections.Counter()

    for f in os.listdir(self.corpus_path):
      file_path = os.path.join(self.corpus_path, f)
      #file_feat_list = utils.read_cuis(file_path)
      text = open(file_path).read()
      file_feat_list = text.split()
      token_counts.update(file_feat_list)

    # now make alphabet (high freq tokens first)
    index = 1
    self.token2int['oov_word'] = 0
    outfile = open(ALPHABET_FILE, 'w')
    for token, count in token_counts.most_common():
      if count > self.min_token_freq:
        outfile.write('%s|%s\n' % (token, count))
        self.token2int[token] = index
        index = index + 1

    # pickle alphabet
    print("Alphabet pickle: " + self.alphabet_pickle)
    pickle_file = open(self.alphabet_pickle, 'wb')
    pickle.dump(self.token2int, pickle_file)

  def load(self, maxlen=float('inf')):
    """Convert examples into lists of indices for keras"""

    labels = []    # int labels
    examples = []  # examples as int sequences
    no_labels = [] # docs with no labels

    # document id -> label mapping
    doc2label = i2b2.parse_standoff(
      self.annot_xml,
      self.disease,
      self.judgement)

    # load examples and labels
    for f in os.listdir(self.corpus_path):
      doc_id = f.split('.')[0]
      file_path = os.path.join(self.corpus_path, f)
      #file_feat_list = utils.read_cuis(file_path)
      text = open(file_path).read()
      file_feat_list = text.split()

      example = []
      for token in set(file_feat_list):
        if token in self.token2int:
          example.append(self.token2int[token])
        else:
          example.append(self.token2int['oov_word'])

      if len(example) > maxlen:
        example = example[0:maxlen]

      # no labels found for some documents
      if doc_id in doc2label:
        string_label = doc2label[doc_id]
        int_label = LABEL2INT[string_label]
        labels.append(int_label)
        examples.append(example)
      else:
        no_labels.append(doc_id)

    print ('%d documents with no labels for %s/%s in %s' \
      % (len(no_labels), self.disease,
         self.judgement, self.annot_xml.split('/')[-1]))
    return examples, labels  

  def load_vectorized(self, exclude, maxlen=float('inf')):
    """Same as above but labels are vectors"""

    labels = []    # int labels
    examples = []  # examples as int sequences
    no_labels = [] # docs with no labels

    # document id -> vector of labels
    doc2labels = i2b2.parse_standoff_vectorized(
      self.annot_xml,
      self.judgement,
      exclude)
    
    # load examples and labels
    for f in os.listdir(self.corpus_path):
      doc_id = f.split('.')[0]
      file_path = os.path.join(self.corpus_path, f)
      #file_feat_list = utils.read_cuis(file_path)
      #file_feat_list = self.read_cuis(file_path)
      text = open(file_path).read()
      ignore_negation = False
      if ignore_negation:
        tokens = []
        for token in text.split():
          if token.startswith('n'):
            tokens.append(token[1:])
          else:
            tokens.append(token)   
      else:
        file_feat_list = text.split()   

      example = []
      for token in set(file_feat_list):

        if token in self.token2int:
          example.append(self.token2int[token])
        else:
          example.append(self.token2int['oov_word'])
      
      if len(example) > maxlen:
        example = example[0:maxlen]
      
      # no labels found for some documents
      if doc_id in doc2labels:
        label_vector = doc2labels[doc_id]
        labels.append(label_vector)
        examples.append(example)
      else:
        no_labels.append(doc_id)

    print ('%d documents with no labels for %s/%s in %s' \
      % (len(no_labels), self.disease,
         self.judgement, self.annot_xml.split('/')[-1]))
    return examples, labels

  def load_raw(self):
    """Load for sklearn training"""
    print('inside load_raw')
    labels = []    # string labels
    examples = []  # examples as strings
    no_labels = [] # docs with no labels

    # document id -> label mapping
    doc2label = i2b2.parse_standoff(
      self.annot_xml,
      self.disease,
      self.judgement)
    
    print('do2label after i2b2 parse_standoff and parse_standoff_file',doc2label)
    
    for f in os.listdir(self.corpus_path):
      if not f.startswith('.'):
        doc_id = f.split('.')[0]
        file_path = os.path.join(self.corpus_path, f)
        #file_feat_list = utils.read_cuis(file_path)
        text = open(file_path).read()
        file_feat_list = text.split()


        # no labels found for some documents
        if doc_id in doc2label:
          string_label = doc2label[doc_id]
          int_label = LABEL2INT[string_label]
          labels.append(int_label)
          examples.append(' '.join(file_feat_list))
        else:
          no_labels.append(doc_id)

    print ('%d documents with no labels for %s/%s in %s' \
      % (len(no_labels), self.disease,
         self.judgement, self.annot_xml.split('/')[-1]))
    return examples, labels

if __name__ == "__main__":

  cfg = configparser.ConfigParser()
  base = os.path.dirname(sys.path[0])
  base_conf = sys.path[0]

  #If no config file passed, use sparce.cfg by default
  if len(sys.argv)>1:
    cfg_file = str(os.path.join(base_conf, sys.argv[1]))
  else:
    cfg_file = os.path.dirname(sys.path[0]) + '/Comorbidity/sparse.cfg'
  cfg.read(cfg_file)
    
  data_dir = os.path.join(base, cfg.get('data', 'train_data'))
  #data_dir = '/content/drive/MyDrive/DLH_Final_Project/test1/Comorbidity/Cuis/Train1+2/'
  annot_xml = os.path.join(base, cfg.get('data', 'train_annot'))  
  judgement = cfg.get('data', 'judgement')
  #judgement = 'intuitive'
  test_annot = os.path.join(base, cfg.get('data', 'test_annot')) 
  alphabet_pickle = os.path.join(base, cfg.get('data', 'alphabet_pickle'))
  print('inside main of dataset.py',alphabet_pickle)
  #alphabet_pickle = '/content/drive/MyDrive/DLH_Final_Project/test1/Comorbidity/Model/alphabet.p'
  exclude = set(['GERD', 'Venous Insufficiency', 'CHF'])
  
  for disease in i2b2.get_disease_names(test_annot, exclude):
    print("Disease: " + str(disease))
    dataset = DatasetProvider(
        data_dir, annot_xml, disease, judgement, alphabet_pickle=alphabet_pickle)
    x, y = dataset.load_vectorized(exclude)
    #print (x)
    #print (y)
  # print(cfg_file)
