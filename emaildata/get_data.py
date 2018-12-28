import os

TRAINSET_PATH = "TrainSet_phase1"
DATAPATH = "/Users/yui/Documents/Winter2018/hr/emaildata/TrainSet_phase1"
OUTPUT = "/Users/yui/Documents/Winter2018/hr/emaildata/emaildata.dat"
OUTPUT_LABELS = "/Users/yui/Documents/Winter2018/hr/emaildata/emaildata.dat.labels"
OUTPUT_NAMES = "/Users/yui/Documents/Winter2018/hr/emaildata/emaildata.dat.names"
OUTPUT_FULL = "/Users/yui/Documents/Winter2018/hr/emaildata/emaildata-full-corpus.txt"

files = os.listdir(DATAPATH)
output = ''
labels = ''
names  = ''
full_corpus = ''

for file in files:
    with open(DATAPATH + '/' + file, encoding="utf8", errors='ignore') as f:
        content = f.read().replace('\n\n', '\n')
    output += content + ('\n \n' if content[-1] != '\n' else ' \n')
    label = 'spam\n' if file[0] == 's' else 'ham\n'
    name = TRAINSET_PATH + '/' + file + '\n'
    labels += label
    names  += name
    full_corpus += label[:-1] + ' ' + name

with open(OUTPUT, 'w') as f:
    f.write(output)
with open(OUTPUT_LABELS, 'w') as f:
    f.write(labels)
with open(OUTPUT_NAMES, 'w') as f:
    f.write(names)
with open(OUTPUT_FULL, 'w') as f:
    f.write(full_corpus)
