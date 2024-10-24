from helper_funtions import *
import argparse
import os
from helper_funtions import *

parser = argparse.ArgumentParser(prog='File Organizor', description='A CLI app that helps you to organize your files.')
parser.add_argument('dirname', 
                    help='The directory to be organized.')
parser.add_argument('-c', '--custom-mapping', 
                    metavar='mapping_file', 
                    help='The map to follow in order to organize the directory. ')
parser.add_argument('-o', '--overwrite', 
                    action='store_true',
                    help='Overwrite default mappings with custom ones completely.')
parser.add_argument('-v', '--verbose', 
                    action='store_true',
                    help='Wether to display the full process or just a progress bar.')
args = parser.parse_args()

def main():
    organize(os.path.abspath(args.dirname),args.custom_mapping,args.overwrite,args.verbose)
if __name__ == '__main__':
    main()
