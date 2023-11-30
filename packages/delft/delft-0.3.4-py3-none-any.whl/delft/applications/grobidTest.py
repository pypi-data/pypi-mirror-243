"""
    grobidTest.py
    ======================

    This modest python script will evaluate the runtime of the grobid models.
    
    To call the script for evaluation the text processing service:

    > python3 grobidTest.py --xml-repo /the/path/to/the/xml/directory/ model_name

    All the xml files under the indicated directory will be parsed and the text content 
    will be processed by the indicated model.

    For instance:

    > python3 grobidTest.py --xml-repo ~/tmp/dataset/software/corpus/ software-scibert

    The default value is 1, so there is no parallelization in the call to the service by default.  

    Tested with python 3.*

"""

import sys
import os
import xml.etree.ElementTree as ET
import re
import subprocess
import argparse
import json
import requests
import time

import numpy as np
from delft.utilities.Embeddings import Embeddings
import delft.sequenceLabelling
from delft.sequenceLabelling import Sequence
from delft.utilities.Tokenizer import tokenizeAndFilter
from sklearn.model_selection import train_test_split
from delft.sequenceLabelling.reader import load_data_and_labels_crf_file
from delft.sequenceLabelling.reader import load_data_and_labels_crf_string
from delft.sequenceLabelling.reader import load_data_crf_string

# for making console output less boring
green = '\x1b[32m'
red = '\x1b[31m'
bold_red = '\x1b[1;31m'
orange = '\x1b[33m'
white = '\x1b[37m'
blue = '\x1b[34m'
score = '\x1b[7m'
bright = '\x1b[1m'
bold_yellow = '\x1b[1;33m'
reset = '\x1b[0m'

delimiters = "\n\r\t\f\u00A0([ •*,:;?.!/)-−–‐\"“”‘’'`$]*\u2666\u2665\u2663\u2660\u00A0"
regex = '|'.join(map(re.escape, delimiters))
pattern = re.compile('('+regex+')') 

models = ['affiliation-address', 'citation', 'date', 'header', 'name-citation', 'name-header', 'software']

def run_eval_txt(xml_repo_path, model, architecture, transformer=None):

    # load the model
    # load model
    model_name = 'grobid-'+model
        
    model = Sequence(model_name)
    model.load()

    model.model_config.batch_size = 200 

    if architecture.find('BERT') != -1:
        model.model_config.max_sequence_length = 512

    start_time = time.time()

    # acquisition of texts
    texts = [] 
    nb_texts = 0
    nb_tokens = 0
    nb_files = 0
    for (dirpath, dirnames, filenames) in os.walk(xml_repo_path):
        for filename in filenames:
            if filename.endswith('.xml') or filename.endswith('.tei'): 
                #try:
                tree = ET.parse(os.path.join(dirpath,filename))
                #except:
                #    print("XML parsing error with", filename)
                for paragraph in tree.findall(".//{http://www.tei-c.org/ns/1.0}p"):
                    #texts.append(paragraph.text)
                    text = ET.tostring(paragraph, encoding='utf-8', method='text').decode('utf-8')
                    text = text.replace("\n", " ")
                    text = text.replace("\t", " ")
                    text = re.sub(r'( )+', ' ', text.strip())
                    text = text.strip()
                    texts.append(text)
                    nb_texts += 1
                    nb_local_tokens = len(pattern.split(text))
                    if 'bert' in model_name:
                        # if we have a BERT architecture model (fine-tuned), strict sequence length limit is 512
                        # we should at some point introduce a splitting of paragraph to manage that correctly
                        nb_tokens += min(nb_local_tokens,512)
                    else:
                        nb_tokens += nb_local_tokens
                    #print(str(nb_local_tokens))
                    if len(texts) == model.model_config.batch_size:
                        process_batch_txt(texts, model)
                        texts = []
                nb_files += 1
                if nb_files > 50:
                    break
    # last batch
    if len(texts) > 0:
        process_batch_txt(texts, model)

    print("-----------------------------")
    print("nb xml files:", nb_files)
    print("nb texts:", nb_texts)
    print("nb tokens:", nb_tokens)

    runtime = round(time.time() - start_time, 4)
    print("-----------------------------")
    print("total runtime: %s seconds " % (runtime))
    print("-----------------------------")
    print("xml files/s:\t {:.4f}".format(nb_files/runtime))
    print("    texts/s:\t {:.4f}".format(nb_texts/runtime))
    print("   tokens/s:\t {:.4f}".format(nb_tokens/runtime)) 

def process_batch_txt(texts, model):
    print(len(texts), "texts to process")
    max_length = 0
    for text in texts:
        nb_text_tokens = len(pattern.split(text))
        if nb_text_tokens>max_length:
            max_length = nb_text_tokens
    print("max sequence length of batch:", max_length)
    model.tag(texts, "json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Compute some runtime statistics for the grobid models")
    parser.add_argument("model")
    parser.add_argument("--xml-repo", type=str, help="path to a directory of XML files containing text to be used for benchmarking")

    args = parser.parse_args()
    model = args.model
    xml_repo_path = args.xml_repo
    threads = args.thread
    architecture = args.architecture
    transformer = args.transformer

    nb_threads = 1
    if threads is not None:
        try:
            nb_threads = int(threads)
        except ValueError:
            print("Invalid concurrency parameter thread:", threads, "thread = 1 will be used by default")
            pass

    # check xml path
    if xml_repo_path is None or not os.path.isdir(xml_repo_path):
        print("the path to the XML directory is not valid: ", xml_repo_path)
    else:
        run_eval_txt(xml_repo_path, model, nb_threads, use_ELMo)
