import math
import metapy
import sys
import time
import os
import functools
import process_test_data as ptd

RATE = 0.75
TESTFILE = "emaildata/TestSet_phase1.txt"
DATASETFOLDER_TEST = 'testdata'
cfg = "config_file.toml"
cfg_test = "config_test.toml"

def make_classifier(training, inv_idx, fwd_idx):
    #options = metapy.learn.SGDModel.Options()
    #options.learning_rate = 0.00001
    #options.l2_regularizer = 0.01
    #return metapy.classify.LogisticRegression(training, options)
    #return metapy.classify.KNN(training, inv_idx, 3, metapy.index.AbsoluteDiscount(0.5))
    #return metapy.classify.NaiveBayes(training)
    return metapy.classify.OneVsAll(training, metapy.classify.SGD, loss_id='hinge')

def cmp(a, b):
    if len(a) < len(b):
        return -1
    elif a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0

def set_corpus(testfolder):
    #TODO: 正确排序
    files = os.listdir(DATASETFOLDER_TEST + '/' + testfolder)
    full_corpus = []
    for file in files:
        label = "1"
        name = testfolder + '/' + file + '\n'
        full_corpus.append(label + ' ' + name)
    full_corpus = sorted(full_corpus, key=functools.cmp_to_key(cmp))
    #full_corpus = sorted(full_corpus)
    with open(DATASETFOLDER_TEST + "/testdata-full-corpus.txt", "w+") as f:
        f.write("".join(sorted(full_corpus)))

def set_corpus_cheat(testfolder):
    files = os.listdir(DATASETFOLDER_TEST + '/' + testfolder)
    max_num = 0
    for file in files:
        max_num = max(max_num, int(file.split('.')[0]))
    full_corpus = ''
    for i in range(max_num+1):
        file = str(i) + ".txt"
        label = "1"
        name = testfolder + '/' + file + '\n'
        full_corpus += label + ' ' + name
    with open(DATASETFOLDER_TEST + "/testdata-full-corpus.txt", "w+") as f:
        f.write(full_corpus)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <TestFile>, normally <TestFile> should be like 'testdata/<filename>'".format(sys.argv[0]))
        sys.exit(1)

    metapy.log_to_stderr()

    print('Building or loading indexes...')
    inv_idx = metapy.index.make_inverted_index(cfg)
    fwd_idx = metapy.index.make_forward_index(cfg)

    dset = metapy.classify.MulticlassDataset(fwd_idx)
    view = metapy.classify.MulticlassDatasetView(dset)
    view.shuffle()
    training = view[:int(RATE*len(view))]
    testing  = view[int(RATE*len(view)):]
    print('training...')
    start_time = time.time()
    #matrix = metapy.classify.cross_validate(lambda fold:
    #        make_classifier(fold, inv_idx, fwd_idx), dset, 5)
    classifier = make_classifier(training, inv_idx, fwd_idx)
    matrix = classifier.test(testing)
    print(matrix)
    matrix.print_stats()
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))

    print('generating prediction result..')
    classifier = make_classifier(view, inv_idx, fwd_idx)
    testfile = sys.argv[1].split('/')[1]
    testfolder = testfile.split('.')[0]
    if testfolder not in os.listdir(DATASETFOLDER_TEST):
        ptd.process_test_data(testfile, testfolder)

    #set_corpus(testfolder)
    set_corpus_cheat(testfolder)

    t_idx = metapy.index.make_forward_index(cfg_test)
    tset = metapy.classify.MulticlassDataset(t_idx)
    tview = metapy.classify.MulticlassDatasetView(tset)

    res = ''
    for v in tview:
        res += "1\n" if classifier.classify(v.weights) == 'spam' else "0\n"
    with open('output.txt', 'w+') as f:
        f.write(res)

    print('done!')
