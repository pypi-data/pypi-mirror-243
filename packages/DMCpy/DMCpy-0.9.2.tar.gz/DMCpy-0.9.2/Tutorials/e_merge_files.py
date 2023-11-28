import os
# sys.path.append(r'C:\Users\lass_j\Documents\Software\DMCpy')
from Tutorial_Class import Tutorial


def Tester():
    from DMCpy import _tools
    import os
    
    # file numbers that should be merged
    mergeNumbers = ['8540,8553']
    saveFileList = ['merged_file.hdf']
    year = 2022

    folder = 'data/SC'
    path = os.path.join(os.getcwd(),folder)

    for numbers,saveFileName in zip(mergeNumbers,saveFileList):
        print(numbers)
        dataFilesList = _tools.fileListGenerator(numbers,path,year=year)
        print(dataFilesList)
        _tools.merge(dataFilesList, os.path.join(path,saveFileName)) 

    
    
    
title = 'Merge data files'

introText = 'To load two data files that cover the same A3 range is slower than loading one single file. '\
+'Therefore it is recommended to merge datafiles that covers the same A3 range. '\
+'It is not required that the data files are of the same A3 range, but they should overlap.'\
+'The code below is an example of merging of data files '\



outroText = 'The above code takes the data from the A3 scan file dmc2022n008540 and dmc2022n008553, and merge them. '\
+'In this case the files cover the exact same A3 range, but it is not a requirement. '\
+'Here the merging is done in a for loop so more files can easily be added. '\


introText = title+'\n'+'^'*len(title)+'\n'+introText


    
Example = Tutorial('merge_files',introText,outroText,Tester,fileLocation = os.path.join(os.getcwd(),r'docs/Tutorials'))

def test_merge_files():
    Example.test()

if __name__ == '__main__':
    Example.generateTutorial()