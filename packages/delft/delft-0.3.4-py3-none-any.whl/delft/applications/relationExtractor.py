# -*- coding: utf-8 -*-

import argparse
import json
import time

from sklearn.model_selection import train_test_split

from delft.sequenceLabelling import Sequence
from delft.sequenceLabelling.reader import load_biored_relations

'''
Relation extraction task is expressed as a sentence classification, similar to approach like 
SciBERT relation extraction. Input is a text with entities pre-annotated and identified with
special tokens, one for head entity and one for tail entity. 

Optionally the marked entities can be associated to an entity type. 

The prediction is a class corresponding to a relation or no relation, relatively to these 2
entities. 
'''

def configure(architecture):
    batch_size = 256
    maxlen = 300
    patience = 5
    early_stop = True
    max_epoch = 60

    # default bert model parameters
    if architecture == "bert":
        batch_size = 16
        early_stop = False
        max_epoch = 6
        maxlen = 200

    return batch_size, maxlen, patience, early_stop, max_epoch


def get_input_path(corpus):
    if corpus == 'biored':
        input_path = "data/sequenceLabelling/biored"
    elif corpus == 'chemprot':
        input_path = "data/sequenceLabelling/chemprot"
    elif corpus == 'bel':
        input_path = "data/sequenceLabelling/BEL"
    return input_path


# train a model with all available data
def train(corpus=None, embeddings_name=None, architecture="gru", transformer=None, input_path=None, 
        output_path=None, features_indices=None, max_sequence_length=-1, batch_size=-1, max_epoch=-1, 
        use_ELMo=False, incremental=False, input_model_path=None, patience=-1, learning_rate=None):
    
    if input_path == None:
        input_path = get_input_path(corpus)

    print('Loading data...')
    x_train, y_train, x_valid, y_valid, x_test, y_test = load_biored_relations(input_path)

    x_all = concatenate_or_none([x_train, x_valid, x_test])
    y_all = concatenate_or_none([y_train, y_valid, y_test])

    print(len(x_all), 'total sequences')

    print("\nmax train sequence length:", str(longest_row(x_all)))

    batch_size, maxlen, patience, early_stop, max_epoch, learning_rate = configure(architecture)

    model_name = "relation_"+corpus+"_"+architecture
    class_weights = None

    model = Classifier(model_name, 
                       architecture=architecture, 
                       list_classes=list_classes, 
                       max_epoch=max_epoch, 
                       fold_number=fold_count, 
                       patience=patience,
                       use_roc_auc=True, 
                       embeddings_name=embeddings_name, 
                       batch_size=batch_size, 
                       maxlen=maxlen, 
                       early_stop=early_stop,
                       class_weights=class_weights, 
                       transformer_name=transformer,
                       learning_rate=learning_rate)

    start_time = time.time()

    if fold_count == 1:
        model.train(x_all, y_all)
    else:
        model.train_nfold(x_all, y_all)

    runtime = round(time.time() - start_time, 3)
    print("training runtime: %s seconds " % (runtime))

    # saving the model
    if output_path:
        model.save(output_path)
    else:
        model.save()


# split data, train a relation extraction model and evaluate it
def train_eval(corpus=None, embeddings_name=None, architecture='gru', transformer=None,
               input_path=None, output_path=None, fold_count=1,
               features_indices=None, max_sequence_length=-1, batch_size=-1, max_epoch=-1, 
               use_ELMo=False, incremental=False, input_model_path=None, patience=-1, learning_rate=None):
    
    if input_path == None:
        input_path = get_input_path(corpus)

    print('Loading data...')
    x_train, y_train, x_valid, y_valid, x_eval, y_eval = load_biored_relations(input_path)

    print(len(x_train), 'train sequences')
    print(len(x_valid), 'validation sequences')
    print(len(x_eval), 'evaluation sequences')

    print("\nmax train sequence length:", str(longest_row(x_train)))
    print("max validation sequence length:", str(longest_row(x_valid)))
    print("max evaluation sequence length:", str(longest_row(x_eval)))

    print(x_train)
    print(y_train)

    batch_size, maxlen, patience, early_stop, max_epoch, learning_rate = configure(architecture)

    model_name = "relation_"+corpus+"_"+architecture
    class_weights = None

    # if we want to train with validation set too when no early stop
    if not early_stop:
        x_train = concatenate_or_none([x_train, x_valid])
        y_train = concatenate_or_none([y_train, y_valid])

    model = Classifier(model_name, 
                       architecture=architecture, 
                       list_classes=list_classes, 
                       max_epoch=max_epoch, 
                       fold_number=fold_count, 
                       patience=patience,
                       use_roc_auc=True, 
                       embeddings_name=embeddings_name, 
                       batch_size=batch_size, 
                       maxlen=maxlen, 
                       early_stop=early_stop,
                       class_weights=class_weights, 
                       transformer_name=transformer,
                       learning_rate=learning_rate)

    start_time = time.time()

    if fold_count == 1:
        model.train(x_train, y_train)
    else:
        model.train_nfold(x_train, y_train)

    runtime = round(time.time() - start_time, 3)
    print("training runtime: %s seconds " % runtime)

    # evaluation
    print("\nEvaluation:")
    model.eval(x_eval, y_eval)

    # saving the model (must be called after eval for multiple fold training)
    if output_path:
        model.save(output_path)
    else:
        model.save()


# split data, train a relation extraction model and evaluate it
def eval_(corpus=None, input_path=None, architecture="gru", use_ELMo=False):
    
    if input_path == None:
        input_path = get_input_path(corpus)

    print('Loading data...')
    x_train, y_train, x_valid, y_valid, x_eval, y_eval = load_biored_relations(input_path)

    print(len(x_eval), 'evaluation sequences')

    model_name = "relation_"+corpus+"_"+architecture
    class_weights = None

    start_time = time.time()

    # load the model
    model = Sequence(model_name)
    model.load()

    # evaluation
    print("\nEvaluation:")
    model.eval(x_eval, y_eval)

    runtime = round(time.time() - start_time, 3)
    print("Evaluation runtime: %s seconds " % (runtime))


# classify a list of texts
def classify_text(texts, corpus=None, output_format="json", architecture='BidLSTM_CRF', use_ELMo=False):

    # load model
    model = Classifier(model_name = "relation_"+corpus+"_"+architecture)
    model.load()
    start_time = time.time()
    result = model.predict(texts, output_format)
    runtime = round(time.time() - start_time, 3)
    if output_format == 'json':
        result["runtime"] = runtime
    else:
        print("runtime: %s seconds " % (runtime))
    return result

class Tasks:
    TRAIN = 'train'
    TRAIN_EVAL = 'train_eval'
    EVAL = 'eval'
    CLASSIFY = 'classify'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Trainer for relation extraction models using the DeLFT library")

    actions = [Tasks.TRAIN, Tasks.TRAIN_EVAL, Tasks.EVAL, Tasks.CLASSIFY]

    word_embeddings_examples = ['glove-840B', 'fasttext-crawl', 'word2vec']
    pretrained_transformers_examples = [ 'bert-base-cased', 'bert-large-cased', 'allenai/scibert_scivocab_cased' ]
    architectures = [ 'bert', 'gru' ]
    corpus = [ 'biored', 'chemprot', 'bel' ]

    parser.add_argument("corpus", help="Name of the corpus.", choices=corpus)
    parser.add_argument("action", choices=actions)
    parser.add_argument("--fold-count", type=int, default=1, help="Number of fold to use when evaluating with n-fold "
                                                                  "cross validation.")
    parser.add_argument("--architecture", help="Type of model architecture to be used, one of "+str(architectures))
    parser.add_argument("--use-ELMo", action="store_true", help="Use ELMo contextual embeddings") 

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
    parser.add_argument("--output", help="Directory where to save a trained model.")
    parser.add_argument("--input", help="When no predefined corpus is indicated, indicates the relation extraction data file to be used " + 
                                        "for training (train action), for training and " +
                                        "evaluation (train_eval action) or just for evaluation (eval action).")
    #parser.add_argument("--incremental", action="store_true", help="training is incremental, starting from existing model if present") 
    #parser.add_argument("--input-model", help="In case of incremental training, path to an existing model to be used " +
    #                                    "to start the training, instead of the default one.")
    parser.add_argument("--max-sequence-length", type=int, default=-1, help="max-sequence-length parameter to be used.")
    parser.add_argument("--batch-size", type=int, default=-1, help="batch-size parameter to be used.")
    parser.add_argument("--patience", type=int, default=-1, help="patience, number of extra epochs to perform after "
                                                                 "the best epoch before stopping a training.")
    parser.add_argument("--learning-rate", type=float, default=None, help="Initial learning rate")

    args = parser.parse_args()

    corpus = args.corpus
    action = args.action
    architecture = args.architecture
    output = args.output
    input_path = args.input
    #input_model_path = args.input_model
    embeddings_name = args.embedding
    max_sequence_length = args.max_sequence_length
    batch_size = args.batch_size
    transformer = args.transformer
    use_ELMo = args.use_ELMo
    #incremental = args.incremental
    patience = args.patience
    learning_rate = args.learning_rate

    if architecture is None:
        raise ValueError("A model architecture has to be specified: " + str(architectures))

    if transformer is None and embeddings_name is None:
        # default word embeddings
        embeddings_name = "glove-840B"

    if action == Tasks.TRAIN:
            train(corpus=corpus, 
            embeddings_name=embeddings_name, 
            architecture=architecture, 
            transformer=transformer,
            input_path=input_path, 
            output_path=output,
            max_sequence_length=max_sequence_length,
            batch_size=batch_size,
            use_ELMo=use_ELMo,
            #incremental=incremental,
            #input_model_path=input_model_path,
            patience=patience,
            learning_rate=learning_rate)

    if action == Tasks.EVAL:
        if args.fold_count is not None and args.fold_count > 1:
            print("The argument fold-count argument will be ignored. For n-fold cross-validation, please use "
                  "it in combination with " + str(Tasks.TRAIN_EVAL))
        if input_path is None:
            raise ValueError("A relation extraction evaluation data file must be specified to evaluate such a model with the parameter --input")
        eval_(corpus=corpus, input_path=input_path, architecture=architecture, use_ELMo=use_ELMo)

    if action == Tasks.TRAIN_EVAL:
        if args.fold_count < 1:
            raise ValueError("fold-count should be equal or more than 1")
        train_eval(corpus=corpus, 
                embeddings_name=embeddings_name, 
                architecture=architecture, 
                transformer=transformer,
                input_path=input_path, 
                output_path=output, 
                fold_count=args.fold_count,
                max_sequence_length=max_sequence_length,
                batch_size=batch_size,
                use_ELMo=use_ELMo, 
                #incremental=incremental,
                #input_model_path=input_model_path,
                learning_rate=learning_rate)

    if action == Tasks.CLASSIFY:
        someTexts = []

        someTexts.append("The column scores (the fraction of entirely correct columns) were  reported  in  addition  to Q-scores  for  BAliBASE 3.0. Wilcoxon  signed-ranks  tests  were  performed  to  calculate statistical  significance  of  comparisons  between  alignment programs,   which   include   ProbCons   (version   1.10)   (23), MAFFT (version 5.667) (11) with several options, MUSCLE (version 3.52) (10) and ClustalW (version 1.83) (7).")
        someTexts.append("Wilcoxon signed-ranks tests were performed to calculate statistical significance of comparisons between  alignment programs, which include ProbCons (version 1.10) (23), MAFFT (version 5.667) (11) with several options, MUSCLE (version 3.52) (10) and ClustalW (version 1.83) (7).")
        someTexts.append("All statistical analyses were done using computer software Prism 6 for Windows (version 6.02; GraphPad Software, San Diego, CA, USA). One-Way ANOVA was used to detect differences amongst the groups. To account for the non-normal distribution of the data, all data were sorted by rank status prior to ANOVA statistical analysis. ")
        someTexts.append("The statistical analysis was performed using IBM SPSS Statistics v. 20 (SPSS Inc, 2003, Chicago, USA).")

        result = annotate_text(someTexts, corpus=corpus, output_path="json", architecture=architecture, use_ELMo=use_ELMo)
        print(json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False))

