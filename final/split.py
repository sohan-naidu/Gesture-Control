import os
import numpy as np
import shutil

cwd = os.getcwd()
root = cwd + '/final/data'

classes = ['open', 'closed', 'left', 'right']

os.makedirs(root +'/train/')
os.makedirs(root +'/test/')

for i in classes:
    os.makedirs(root +'/train/' + i)
    os.makedirs(root +'/test/' + i)
    source = root + '/' + i
    allFileNames = os.listdir(source)
    np.random.shuffle(allFileNames)
    test_ratio = 0.25
    train_FileNames, test_FileNames = np.split(np.array(allFileNames),[int(len(allFileNames)* (1 - test_ratio))])
    train_FileNames = [source+'/'+ name for name in train_FileNames.tolist()]
    test_FileNames = [source+'/' + name for name in test_FileNames.tolist()]

    #print(test_FileNames)
    for name in train_FileNames:
        shutil.copy(name, root +'/train/' + i)
    for name in test_FileNames:
        shutil.copy(name, root +'/test/' + i)
print("OK")