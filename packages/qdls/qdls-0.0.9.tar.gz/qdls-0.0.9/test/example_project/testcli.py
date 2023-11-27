import os,sys 
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
 
PROJ_DIR = FILE_DIR[:FILE_DIR.index('qdls')+len('qdls')]
sys.path.append(PROJ_DIR)

from src.qdls.cli import main

main()