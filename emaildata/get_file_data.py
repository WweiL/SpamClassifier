import os

TRAINSET_PATH = "TrainSet_phase1"
LARGE_SET_PATH = "enron"
DATAPATH = "/Users/yui/Documents/Winter2018/hr/emaildata/"
OUTPUT_FULL = "/Users/yui/Documents/Winter2018/hr/emaildata/emaildata-full-corpus.txt"

files = os.listdir(DATAPATH + TRAINSET_PATH)
spam_files = os.listdir(DATAPATH + LARGE_SET_PATH + "/spam")
ham_files = os.listdir(DATAPATH + LARGE_SET_PATH + "/ham")
full_corpus = ''

for file in files:
    label = 'spam\n' if file[0] == 's' else 'ham\n'
    name = TRAINSET_PATH + '/' + file + '\n'
    full_corpus += label[:-1] + ' ' + name

for file in spam_files:
    name = LARGE_SET_PATH + '/spam/' + file + '\n'
    full_corpus += 'spam ' + name

for file in ham_files:
    name = LARGE_SET_PATH + '/ham/' + file + '\n'
    full_corpus += 'ham ' + name

with open(OUTPUT_FULL, 'w') as f:
    f.write(full_corpus)
