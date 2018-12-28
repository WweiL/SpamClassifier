import os

TESTFILE = 'TestSet_phase1.txt'
TESTFOLDER = 'TestSet_phase1'
DATASETFOLDER = 'emaildata'

def get_filename(t):
    i = 0
    while t[i] == 61:
        i += 1
    j = i
    while t[j] != 61:
        j += 1
    return t[i:j]

def process_test_data(testfile, testfolder):
    if testfolder not in os.listdir(DATASETFOLDER):
        os.mkdir(DATASETFOLDER + '/' + testfolder)

    file_name = ''
    curr_file = open(DATASETFOLDER + '/' + testfolder + '/0.txt', 'wb+')

    with open(DATASETFOLDER + '/' + testfile, 'rb') as file:
        for line_content in file:
            if line_content[:10] == b'==========':
                file_name = get_filename(line_content).decode('utf-8')
                curr_file.close()
                curr_file = open(DATASETFOLDER + '/' + testfolder + '/' + file_name, 'wb+')
            else:
                curr_file.write(line_content)

if __name__ == '__main__':
    process_test_data(TESTFILE, TESTFOLDER)
