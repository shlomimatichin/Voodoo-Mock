#you'll probably only ever use multi
export LD_LIBRARY_PATH=../..
mkdir multi-result
python ../../multi.py --input=original --output=multi-result --exclude=Dont --define=IN= --define=OUT= --define=INOUT=
#you might also want to read about multi --concurrent flag, and --only-if-new flag. run multi.py with --help

#you might sometime want a more complicated build process, and create the h files single handedly
mkdir single-result
#the next line will create single-result/original/Header1.h
python ../../single.py --input=original/Header1.h --output=single-result --define=IN= --define=OUT= --define=INOUT=
python ../../single.py --input=original/Header2.h --output=single-result/Header2.h

#but mostly single.py is used to produce external voodoos. more on external in it's tutorial chapter
