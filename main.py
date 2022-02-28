from ContractNoteParser import *
from os import listdir
from os.path import isfile, join
from shutil import copyfile
from os.path import exists



def parse_files(folderName):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {folderName}')  # Press ⌘F8 to toggle the breakpoint.
    filesname = list_files(folderName);

    for p in filesname:
        print ("First File"+p)
        # check if file has already been processed
        if (exists('processed/' + p)):
            print ("File Already Processed - Ignoring")
        else:
            parse_file(p,folderName);
            # copy file to processed folder
            copyfile(folderName + p, 'processed/' + p)


def list_files(input_path):
    onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    print ("List of files identified are...")
    for p in onlyfiles:
        print (p)
    return onlyfiles

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_files('inputfiles/')

