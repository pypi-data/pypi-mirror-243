import json
from delft.utilities.Embeddings import Embeddings
from delft.utilities.Utilities import split_data_and_labels
from delft.utilities.Tokenizer import tokenizeAndFilterSimple
from delft.utilities.numpy import shuffle_arrays
from delft.textClassification.reader import load_citation_sentiment_corpus
import delft.textClassification
from delft.textClassification import Classifier
import argparse
import time
from delft.textClassification.models import architectures

import numpy as np
import pandas as pd
import re
from lxml import etree, objectify
import xml.sax.saxutils as saxutils
import html

from blingfire import text_to_sentences

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=RuntimeWarning) 


list_classes = ["contradicting", "mentioning", "supporting"]

"""
class_weights = {
                    0: 1.2,
                    1: 0.9,
                    2: 0.9
                }
"""
class_weights = {
                    0: 1.0,
                    1: 1.0,
                    2: 1.0
                }

def configure(architecture):
    batch_size = 256
    maxlen = 150
    patience = 5
    early_stop = True
    max_epoch = 60

    # default bert model parameters
    if architecture == "bert":
        batch_size = 32
        early_stop = False
        max_epoch = 5

    return batch_size, maxlen, patience, early_stop, max_epoch

def train(embeddings_name, fold_count, architecture="gru", transformer=None, with_holdout=True):
    use_sections = False
    batch_size, maxlen, patience, early_stop, max_epoch = configure(architecture)

    model = Classifier('veracity-'+architecture, architecture=architecture, list_classes=list_classes, max_epoch=max_epoch, fold_number=fold_count, 
        use_roc_auc=True, embeddings_name=embeddings_name, batch_size=batch_size, maxlen=maxlen, patience=patience, early_stop=early_stop,
        class_weights=class_weights, transformer_name=transformer)

    print('loading citation function train corpus...')
    x_train, y_train, _ = load_training_corpus_rebuild_csv("data/textClassification/veracity/training/scite-verified-corpus-052818-rebuild.csv",
                                                     filepath_additions=["data/textClassification/veracity/training/291-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-1-2-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-3-4-5-6-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-7-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-8-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-9-10-new.csv",
                                                                        "data/textClassification/veracity/training/expert_classification_081219_training.csv",
                                                                        "data/textClassification/veracity/training/set_01_01_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_02_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_03_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_04_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_05_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_01_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_02_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_03_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_04_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_05_verified.csv"
                                                                        ],
                                                                        add_section_info=use_sections)

    # for a final full training (model to be shipped in production), we can use all resources available, including the holdout set
    if with_holdout:
        x_holdout, y_holdout, _ = load_holdout_corpus_rebuild_csv("data/textClassification/veracity/holdout/holdout-022619-rebuild.csv",
                                                            add_section_info=use_sections)
        x_train = np.concatenate((x_train, x_holdout), axis=0)
        y_train = np.concatenate((y_train, y_holdout), axis=0)

        # additional shuffle to take into account the holdout set entries, this is an in-place shuffle
        shuffle_arrays([x_train,y_train])

    if fold_count == 1:
        model.train(x_train, y_train)
    else:
        model.train_nfold(x_train, y_train)
    # saving the model
    model.save()

def train_and_eval(embeddings_name, fold_count, architecture="gru", transformer=None): 
    use_sections = False
    batch_size, maxlen, patience, early_stop, max_epoch = configure(architecture)

    model = Classifier('veracity-'+architecture, architecture=architecture, list_classes=list_classes, max_epoch=max_epoch, fold_number=fold_count, 
        use_roc_auc=True, embeddings_name=embeddings_name, batch_size=batch_size, maxlen=maxlen, patience=patience, early_stop=early_stop,
        class_weights=class_weights, transformer_name=transformer)

    # segment train and eval sets
    print('loading citation function train corpus...')
    x_train, y_train, _ = load_training_corpus_rebuild_csv("data/textClassification/veracity/training/scite-verified-corpus-052818-rebuild.csv",
                                                     filepath_additions=["data/textClassification/veracity/training/291-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-1-2-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-3-4-5-6-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-7-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-8-verified.csv",
                                                                        "data/textClassification/veracity/training/5000-9-10-new.csv",
                                                                        "data/textClassification/veracity/training/expert_classification_081219_training.csv",
                                                                        "data/textClassification/veracity/training/set_01_01_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_02_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_03_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_04_verified.csv",
                                                                        "data/textClassification/veracity/training/set_01_05_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_01_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_02_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_03_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_04_verified.csv",
                                                                        "data/textClassification/veracity/training/set_02_05_verified.csv"
                                                                        ],
                                                                        add_section_info=use_sections)

    print('loading citation function holdout corpus...')
    x_test, y_test, _ = load_holdout_corpus_rebuild_csv("data/textClassification/veracity/holdout/holdout-022619-rebuild.csv",
                                                            add_section_info=use_sections)

    if fold_count == 1:
        model.train(x_train, y_train)
    else:
        model.train_nfold(x_train, y_train)
    
    # saving the model
    model.save()

    model.eval(x_test, y_test)

def holdout(output_format, architecture="gru", embeddings_name=None, transformer=None):
    use_sections = False

    batch_size, maxlen, patience, early_stop, max_epoch = configure(architecture)
    model = Classifier('veracity-'+architecture, architecture=architecture, list_classes=list_classes, embeddings_name=embeddings_name, transformer_name=transformer)
    model.load()

    print('loading citation function holdout corpus...')
    x_test, y_test, _ = load_holdout_corpus_rebuild_csv("data/textClassification/veracity/holdout/holdout-022619-rebuild.csv", add_section_info=use_sections)
    model.eval(x_test, y_test)

# classify a list of texts
def classify(texts, output_format, architecture="gru", embeddings_name=None, transformer=None):
    # load model
    model = Classifier('veracity-'+architecture, architecture=architecture, list_classes=list_classes, embeddings_name=embeddings_name, transformer_name=transformer)
    model.load()
    start_time = time.time()
    result = model.predict(texts, output_format, batch_size=256)
    runtime = round(time.time() - start_time, 3)
    if output_format == 'json':
        result["runtime"] = runtime
    else:
        print("runtime: %s seconds " % (runtime))
    return result

def load_model(class_weights=None):
    model = Classifier('veracity-'+architecture, architecture=architecture, list_classes=list_classes, embeddings_name=embeddings_name, transformer_name=transformer)
    model.load()

    return model

def load_training_corpus_rebuild_csv(
        filepath, filepath_additions=None, add_section_info=False):
    """
    Load texts from the training citation corpus in csv and in the rebuild format with Pandas

    Returns:
        tuple(numpy array, numpy array, numpy array): texts, polarity, full snippets

    """

    texts = []
    polarities = []
    snippets = []

    df = pd.read_csv(
        filepath,
        usecols=[
            'id',
            'class',
            'target_sentence',
            'section',
            'sections',
            'target_doi',
            'full_snippet'])

    print(df.shape)

    # remove rows with class NAN
    # df.dropna(inplace=True)
    # for safety, remove rows with class 4 (no call), but this should not
    # appear in the training data
    df = df[df['class'] != 4]
    df = df.astype({"class": int})

    def rewrite_class(x):
        # in the current csv, 1 is supporting (positive), 2 is refuting
        # (negative) and 3 neutral
        if x == 1:
            return 1, 0, 0
        elif x == 2:
            return 0, 1, 0
        elif x == 3:
            return 0, 0, 1
        else:
            print("invalid class:", x)
            return 0, 0, 0
    df["supporting"], df["contradicting"], df["mentioning"] = zip(
        *df["class"].map(rewrite_class))
    df = df.drop(columns=['class'])

    # shuffle in case the rows are sorted by class
    df = df.sample(frac=1)
    df.reset_index(drop=True, inplace=True)

    # print(df.shape)

    # rename full_snippet into markup_context for consistency with the other
    # format
    df.rename(columns={'full_snippet': 'markup_context'}, inplace=True)
    df = df.astype({"markup_context": str})
    df = df.astype({"target_doi": str})

    df = df.apply(clean_row, axis=1)
    df.rename(columns={'target_sentence': 'text'}, inplace=True)
    df = df.astype({"text": str})
    df = df.astype({"section": str})
    df = df.astype({"sections": str})

    # for snippet without extracted sentence, we can use the manual one as
    # fall back
    '''
    def fill_text_field(row):
        if row["text"] is None or row["text"].lower() == "nan" or len(row["text"]) < 10:
            row["text"] = row["target_sentence"]
        return row


    df = df.apply(fill_text_field, axis=1)
    df = df.astype({"text": str})
    print(df.shape)
    #df.dropna(inplace=True)
    #print(df.shape)
    '''

    def text_field_section(row):
        if row["section"] is not None and row["section"].lower() != "nan":
            row['text'] = " ".join([row["section"], row['text']])
        return row

    def text_field_sections(row):
        if row["sections"] is not None and len(row["sections"]) > 0:
            sections = " ".join(row["sections"])
            row['text'] = " ".join([sections, row['text']])
        return row

    if add_section_info:
        df = df.apply(text_field_section, axis=1)

    df = df.apply(preprocess_row, axis=1)

    df = df.apply(preprocess_row, axis=1)

    df = df[df["text"].map(count_token) > 5]
    if add_section_info:
        df = df[df["text"].map(count_token) < 110]
    else:
        df = df[df["text"].map(count_token) < 100]
    df.reset_index(drop=True, inplace=True)

    print(df.shape)

    if filepath_additions is not None:
        for filepath_addition in filepath_additions:
            df_add = pd.read_csv(filepath_addition, encoding="UTF-8")

            df_add = df_add[df_add['class'] != 'no call']
            #df = df.astype({"class": int})
            print(df_add.shape)

            def rewrite_holdout_class(x):
                # in the current csv, 1 is supporting (positive), 2 is refuting
                # (negative) and 3 neutral
                if x == 'supporting':
                    return 1, 0, 0
                elif x == 'contradicting':
                    return 0, 1, 0
                elif x == 'mentioning':
                    return 0, 0, 1
                else:
                    print("invalid class:", x)
                    return 0, 0, 0
            df_add["supporting"], df_add["contradicting"], df_add["mentioning"] = zip(
                *df_add["class"].map(rewrite_holdout_class))
            df_add = df_add.drop(columns=['class'])

            df_add.reset_index(drop=True, inplace=True)

            # rename snippet into markup_context to ensure compatibility with
            # the snippet methods
            df_add.rename(columns={'snippet': 'markup_context'}, inplace=True)

            df_add = df_add.apply(clean_row, axis=1)
            df_add = df_add.apply(target_sentence, axis=1)
            df_add.reset_index(drop=True, inplace=True)

            df_add = df_add.astype({"section": str})
            df_add = df_add.astype({"sections": str})

            if add_section_info:
                df_add = df_add.apply(text_field_section, axis=1)

            df = df.apply(preprocess_row, axis=1)

            df_add = df_add[df_add["text"].map(count_token) > 5]
            if add_section_info:
                df = df[df["text"].map(count_token) < 110]
            else:
                df_add = df_add[df_add["text"].map(count_token) < 100]
            df_add.reset_index(drop=True, inplace=True)

            df = pd.concat([df, df_add])
            df.reset_index(drop=True, inplace=True)
            df = df.sample(frac=1)

    nb_mentioning = 0
    # shuffle in case the rows are sorted by class
    df = df.sample(frac=1)
    df.reset_index(drop=True, inplace=True)
    for i in df.index:
        if df.at[i, "contradicting"] == 0 and df.at[i,
                                                    "mentioning"] == 0 and df.at[i, "supporting"] == 0:
            continue

        # if nb_mentioning > 10000 and df.at[i,"mentioning"] == 1:
        #    continue

        # if df.at[i,"mentioning"] == 1:
        #    nb_mentioning += 1

        # full snippet
        snippet = df.at[i, "markup_context"]
        snippet = remove_markup(str(snippet))
        snippets.append(snippet.strip())

        # polarity
        # order is ["contradicting", "mentioning", "supporting"]
        polarity = []
        polarity.append(df.at[i, "contradicting"])
        polarity.append(df.at[i, "mentioning"])
        polarity.append(df.at[i, "supporting"])
        polarities.append(polarity)

        # text
        text = df.at[i, "text"]
        text = remove_markup(str(text))
        texts.append(text.strip())

    return np.asarray(texts), np.asarray(polarities), np.asarray(snippets)

def load_holdout_corpus_rebuild_csv(filepath, add_section_info=False):
    """
    Load texts from the holdout citation corpus in csv with Pandas

    Returns:
        tuple(numpy array, numpy array, numpy array): texts, polarity, full snippets

    """

    texts = []
    polarities = []
    snippets = []

    # id,source_doi,original_full_snippet,class,target_sentence,section,sections,target_doi,full_snippet
    df = pd.read_csv(filepath, encoding="UTF-8")
    print("total init:", df.shape[0])

    # output row with nan, which have not been classified
    df.drop(['id', 'source_doi'], axis=1, inplace=True)

    # remove rows with class NAN
    # df.dropna(inplace=True)
    # remove rows with class 4 (no call)
    df = df[df['class'] != 'no call']
    #df = df.astype({"class": int})
    print("removing no call:", df.shape[0])

    def rewrite_holdout_class(x):
        # in the current csv, 1 is supporting (positive), 2 is refuting
        # (negative) and 3 neutral
        if x == 'supporting':
            return 1, 0, 0
        elif x == 'contradicting':
            return 0, 1, 0
        elif x == 'mentioning':
            return 0, 0, 1
        else:
            print("invalid class:", x)
            return 0, 0, 0
    df["supporting"], df["contradicting"], df["mentioning"] = zip(
        *df["class"].map(rewrite_holdout_class))
    df = df.drop(columns=['class'])

    # shuffle in case the rows are sorted by class
    df = df.sample(frac=1)

    # check and remove rows with empty text
    # df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # for some mysterious reasons, target_doi are here xml-escaped two times
    def unescape_doi(x):
        x = saxutils.unescape(x)
        return x
    df["target_doi"] = df["target_doi"].map(unescape_doi)

    # rename full_snippet into markup_context to ensure compatibility with the
    # snippet methods
    df.rename(columns={'full_snippet': 'markup_context'}, inplace=True)

    df = df.apply(clean_row, axis=1)
    df = df.apply(target_sentence, axis=1, use_mask=True)

    def text_field_section(row):
        if row["section"] is not None and row["section"].lower(
        ) != "nan" and row['text'] is not None:
            row['text'] = " ".join([row["section"], row['text']])
        return row

    def text_field_sections(row):
        if row["sections"] is not None and len(
                row["sections"]) > 0 and row['text'] is not None:
            sections = " ".join(row["sections"])
            row['text'] = " ".join([sections, row['text']])
        return row

    df = df.astype({"section": str})
    df = df.astype({"sections": str})

    if add_section_info:
        df = df.apply(text_field_section, axis=1)

    df = df.apply(preprocess_row, axis=1)

    df = df.apply(preprocess_row, axis=1)

    df = df[df["text"].map(count_token) > 5]
    if add_section_info:
        df = df[df["text"].map(count_token) < 110]
    else:
        df = df[df["text"].map(count_token) < 100]
    df.reset_index(drop=True, inplace=True)

    print("removing invalid:", df.shape[0])

    for i in df.index:
        # full snippet
        snippet = df.at[i, "markup_context"]
        #print("\n", snippet)
        snippet = remove_markup(str(snippet))
        snippets.append(snippet.strip())

        # polarity
        # order is ["contradicting", "mentioning", "supporting"]
        polarity = []
        polarity.append(df.at[i, "contradicting"])
        polarity.append(df.at[i, "mentioning"])
        polarity.append(df.at[i, "supporting"])
        polarities.append(polarity)

        # text
        text = df.at[i, "text"]
        # print(text)
        text = remove_markup(str(text))
        texts.append(text.strip())

    return np.asarray(texts), np.asarray(polarities), np.asarray(snippets)

def clean_row(row):
    row['markup_context'] = clean_text(row['markup_context'])
    # weird stuff to remove...
    row['markup_context'] = row['markup_context'].replace(
        '<ref target...="></ref>', ' ')
    return row

def clean_text(string):
    if string is None or len(string) == 0:
        return string
    string = re.sub("\"\"", "\"", string)
    string = re.sub("\\n"," ",string)
    string = re.sub("( )+"," ",string)
    string = string.strip()
    return string

def preprocess_row(row):
    #row['text'] = maskSnippetWithMarkup(row['text'], row['target_doi'], mask_target='XX', mask_other='YY')
    row['text'] = preprocess_text(row['text'])
    return row

def preprocess_text(string):
    string = _normalize_num(string)
    #string = string.lower()
    return string

def _normalize_num(sentence):
    if sentence is not None:
        return re.sub(r'[0-9０１２３４５６７８９]', r'0', sentence)
    else:
        return sentence

def count_token(text):    
    if text is None: 
        return 0 
    tokens = tokenizeAndFilterSimple(clean_text(text))
    return len(tokens)

def segmentSnippetWithMarkup(snippet):
    '''
    Sentence segmentation for full snippet produced by kala, including markup. There are
    several cases to cover as compared to "traditional" sentence segmentation:
    * superscript callout after the dot of the sentence where it appears:
      ...bla bla.13 New sentence...
      ...subjects.26, 27, 28, 29, 30, 31 Three trials...
    * lack of space after dot:
      ...years [35].Both ...
      ... ChIPpeakAnno (22).Distr...
      ...(<cite data-doi=""10.1016/j.jtbi.2014.04.027"">Morishita and Suzuki, 2014</cite>).Such morphogenetic...
    * lack of space with <hi>:
      ...and anxiety disorders.<hi rend="superscript"><cite data-doi="10.1016/j.biopsych.2006.05.022">10</cite>...
    * some particular dotted notations ... et al. ...
    In addition some (rare) snippets are not well-formed xml fragments, due to a possible missing closing tag
    which has to be handled preliminarly.
    '''

    if snippet is None or len(snippet) == 0 or snippet.lower() == "nan":
        return None

    # basic, but necessary, cleaning
    snippet = clean_text(str(snippet))

    # missing space around closing <hi>
    # ... of <hi rend="italic">daf-12/NHR</hi>.It seemed possible...
    case0 = r'</hi>\.([A-Z])'
    pattern0 = re.compile(case0)
    snippet = re.sub(pattern0, r'</hi>. \g<1>', snippet)

    # remove all <hi> elements
    snippet = re.sub("<hi[^>]+>", "", snippet)
    snippet = re.sub("</hi>", "", snippet)

    root = None
    try:
        root = objectify.fromstring('<p>' + snippet + '</p>')
    except etree.XMLSyntaxError:
        #print('not parsable:', snippet)
        # apply recovery (usually remove a non-closed <cite> without doi data)
        snippet = snippet.replace("<cite>", "")
        try:
            root = objectify.fromstring('<p>' + snippet + '</p>')
        except etree.XMLSyntaxError:
            print('not parsable and unrecovered:', snippet)
            pass
        pass

    # missing space after callout
    # <cite data-doi=""10.3109/03639045.2014.902465"">66</cite>].In addition
    case1 = r'</cite>([\]\)])\.'
    pattern1 = re.compile(case1)
    snippet = re.sub(pattern1, r'</cite>\g<1>. ', snippet)

    # variant of case 1 (consider that <hi> tags are removed above)
    # medulla <hi rend="superscript"><cite
    # data-doi="10.2198/jelectroph.49.5">27</cite></hi>.These findings
    case1_2 = r'</cite>\.([A-Z])'
    pattern1_2 = re.compile(case1_2)
    snippet = re.sub(pattern1_2, r'</cite>. \g<1>', snippet)

    # we have the same missing space also without <cite> markup:
    # ... [46], [47].The data presented...
    # ... Liebetanz et al., 2002).It has also been speculated...
    case1_3 = r'\]\.([A-Z])'
    pattern1_3 = re.compile(case1_3)
    snippet = re.sub(pattern1_3, r']. \g<1>', snippet)
    # note adding the ) in addition to ] causes a significant loss of accuracy! minus 3 point f-score (might cut doi string?)
    #case1_4 = r'\)\.([A-Z])'
    #pattern1_4 = re.compile(case1_4)
    #snippet = re.sub(pattern1_4, '). \g<1>', snippet)

    # superscript callout after end of sentence
    case2 = r'\.(<cite[^<]+</cite>[, \-–]*)+'
    pattern2 = re.compile(case2)

    new_snippet = ""
    last_index = 0
    for m in pattern2.finditer(snippet):
        new_snippet += snippet[last_index:m.start()] + \
            " " + snippet[m.start() + 1:m.end()] + ". "
        last_index = m.end()
        # m.group()
    new_snippet += snippet[last_index:len(snippet)]
    if len(new_snippet) > 0:
        snippet = new_snippet

    # case et al.
    # ... an fMRI study by Peacock-Lewis et al. <cite data-doi="10.1162/jocn_a_00140">[68] ...
    snippet = snippet.replace("et al.", "et al ")

    # frequent case like Fig. 3, E. coli, ...
    # ... regardless of the strain background (Fig. 6), which is consistent with our earlier...
    snippet = snippet.replace("Fig.", "Fig ")
    # ... similar to the one reported for E. coli in the host intestine...
    snippet = snippet.replace("E. coli ", "E coli")
    # ...in detail in Ref. [11]. ...
    snippet = snippet.replace("Ref.", "Ref ")

    # more or less regular text but missing space at sentence end
    # ... was agreed.Exclusion criteria...
    # but we should not segment in a case like this:
    # ... ATP-binding (GHKL) domain of P.falciparum HSP90...
    case3 = r'([a-z])\.([A-Z])'
    pattern3 = re.compile(case3)
    snippet = re.sub(pattern3, r'\g<1>. \g<2>', snippet)

    # sentence segmentation (in principle robust to inline xml, but to be
    # confirmed)
    sentences = [sent.strip() for sent in text_to_sentences(snippet).split('\n')]

    return sentences


def getTargetSentence(target_doi, snippet, use_mask=False, maxlen=90):
    # identify target sentence
    '''
    root = None
    try:
        root = objectify.fromstring('<p>'+snippet+'</p>')
    except etree.XMLSyntaxError:
        #print('not parsable snippet:', snippet)
        # apply recovery (usually remove a non-closed <cite> without doi data)
        snippet = snippet.replace("<cite>", "")
        try:
            root = objectify.fromstring('<p>'+snippet+'</p>')
        except etree.XMLSyntaxError:
            print('not parsable and unrecovered:', snippet)
            pass
        pass
    '''
    target_doi = target_doi.replace("//", "/")
    sentences = segmentSnippetWithMarkup(snippet)
    # print(sentences)

    sentence = None
    selected_sentences = []

    if sentences is None or len(sentences) == 0:
        return None

    for sent in sentences:
        #print('sent:', sent)
        sent = sent.replace("//", "/")
        pos_start = sent.lower().find(target_doi.lower())
        if pos_start != -1:
            #sentence = sent
            selected_sentences.append(sent)
            # break
        else:
            # try escaping the doi
            escaped_target_doi = saxutils.escape(target_doi)
            pos_start = sent.lower().find(escaped_target_doi.lower())
            if pos_start != -1:
                #sentence = sent
                # break
                selected_sentences.append(sent)

    # if sentence is None or count_token(sentence) <= 5:
        #print("error getting target sentence: ", snippet, target_doi, saxutils.escape(target_doi))
        #sentence = snippet

    if len(selected_sentences) > 0:
        #sentence = " ".join(selected_sentences)
        sentence = selected_sentences[0]

    if sentence is None or count_token(sentence) <= 5:
        sentence = None

    # if masking reference callout
    if use_mask and sentence is not None:
        sentence = maskSnippetWithMarkup(sentence, target_doi)

    if sentence is not None:
        sentence = remove_markup(sentence)

    # better to have bad segmentation than reject a too long target sentence
    # or to just take the start and cut at n tokens
    # here we ensure that the target callout and its previous text are
    # present in a shorter sentence
    if sentence is not None and use_mask and count_token(sentence) >= maxlen:
        #print(count_token(sentence), sentence)
        pos_target = sentence.find("XX")
        if pos_target != -1:
            new_sentence = sentence[0:pos_target + 2]
            #print(count_token(new_sentence), new_sentence)
            if count_token(new_sentence) >= maxlen:
                # still need some triming
                while(count_token(new_sentence) >= maxlen):
                    pos_space = new_sentence.find(" ")
                    if pos_space == -1:
                        break
                    new_sentence = new_sentence[pos_space + 1:]
                #print(count_token(new_sentence), new_sentence)
            sentence = new_sentence

    return sentence

def target_sentence(row, use_mask=False):
    markup_snippet = row['markup_context']
    target_doi = row['target_doi']

    sentence = getTargetSentence(
        target_doi,
        markup_snippet,
        use_mask=use_mask)

    row['text'] = sentence
    #row['target_string'] = target_string
    return row

def remove_markup(string):
    ''' 
    Remove xml and html markup, replace standard html entity encoding
    '''
    string = re.sub("<[^>]+>", "", string)
    string = html.unescape(string)

    return string

def maskSnippetWithMarkup(
        snippet, target_doi, mask_target='XX', mask_other='YY'):
    # first mask all citation callout
    snippet = re.sub("<cite\s*([^\>]+)>([^<]+)</cite>",
                     r"<cite \g<1>>" + mask_other + "</cite>",
                     snippet,
                     flags=re.IGNORECASE)

    # second mask target citation callout
    doi = re.escape(target_doi)
    snippet = re.sub("<cite data\-doi=\"+" + doi + "\"+>" + mask_other + "</cite>",
                     "<cite data-doi=\"" + doi + "\">" + mask_target + "</cite>",
                     snippet,
                     flags=re.IGNORECASE)
    return snippet

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Sentiment classification of citation contexts based on DeLFT")

    word_embeddings_examples = ['glove-840B', 'fasttext-crawl', 'word2vec']
    pretrained_transformers_examples = [ 'bert-base-cased', 'bert-large-cased', 'allenai/scibert_scivocab_cased' ]

    parser.add_argument("action", help="one of [train, train_eval, holdout, classify]")
    parser.add_argument("--fold-count", type=int, default=1)
    parser.add_argument("--architecture",default='gru', help="type of model architecture to be used, one of "+str(architectures))
    parser.add_argument(
        "--embedding", 
        default=None,
        help="The desired pre-trained word embeddings using their descriptions in the file. " + \
            "For local loading, use delft/resources-registry.json. " + \
            "Be sure to use here the same name as in the registry, e.g. " + str(word_embeddings_examples) + \
            " and that the path in the registry to the embedding file is correct on your system."
    )
    parser.add_argument(
        "--transformer", 
        default=None,
        help="The desired pre-trained transformer to be used in the selected architecture. " + \
            "For local loading use, delft/resources-registry.json, and be sure to use here the same name as in the registry, e.g. " + \
            str(pretrained_transformers_examples) + \
            " and that the path in the registry to the model path is correct on your system. " + \
            "HuggingFace transformers hub will be used otherwise to fetch the model, see https://huggingface.co/models " + \
            "for model names"
    )

    args = parser.parse_args()

    if args.action not in ('train', 'train_eval', 'holdout', 'classify'):
        print('action not specifed, must be one of [train,train_eval,holdout,classify]')

    embeddings_name = args.embedding
    transformer = args.transformer
    
    architecture = args.architecture
    if architecture not in architectures:
        print('unknown model architecture, must be one of '+str(architectures))

    if transformer == None and embeddings_name == None:
        # default word embeddings
        embeddings_name = "glove-840B"

    if args.action == 'train':
        if args.fold_count < 1:
            raise ValueError("fold-count should be equal or more than 1")

        train(embeddings_name, args.fold_count, architecture=architecture, transformer=transformer)

    if args.action == 'train_eval':
        if args.fold_count < 1:
            raise ValueError("fold-count should be equal or more than 1")

        y_test = train_and_eval(embeddings_name, args.fold_count, architecture=architecture, transformer=transformer)    

    elif args.action == 'holdout':
        if args.fold_count < 1:
            raise ValueError("fold-count should be equal or more than 1")
        holdout("json", embeddings_name=embeddings_name, architecture=architecture, transformer=transformer)

    elif args.action == 'classify':
        # we test here two times 150 examples, involving several batched and separate predictions (without reload of the model)
        texts = [ 
            'RNA extraction, DNAase treatment [21] and cDNA synthesis [22] were performed as described.',
            'Finally, our model agrees with psychological theories of free recall proposing that repetitions/reactivations of early list items during subsequent ISIs rely on the same retrieval process as recall [49].', 
            'This is in contrast with two studies that reported a normal spine density for L2/3 and L4 pyramidal neurons in fixed slices at early postnatal ages [35], [37].',
            'This is in contrast to previous studies from engineering that have found that women tend to publish in higher-impact journals [14].',
            'It is, however, consistent with a previous studies from mathematics [7]. By contrast, there is no significant correlation ( P Z > | z | = 0.568) between impact factor and P female in computational biology publications.'
        ]
        all_texts = []
        for n in range(0,500):
            all_texts.append(texts[0])
            all_texts.append(texts[1])
            all_texts.append(texts[2])
            all_texts.append(texts[3])
            all_texts.append(texts[4])

        result = classify(all_texts, "json", architecture=architecture, embeddings_name=embeddings_name, transformer=transformer)
        #print(json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False))

