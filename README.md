# MIS #

### What is it?
MIS computes minimal Independent Support for a given CNF formula. The implementation is based on MIS algorithm proposed in our [CP'15 paper](http://link.springer.com/article/10.1007/s10601-015-9204-z), which also won the Best Student Paper Award. 

MIS is licensed under the MIT license and built by Kuldeep Meel. It is currently maintined by Mate Soos.

### Building
MIS must be built using GCC 4.8.x or higher and requires libz.

```
apt-get install minisat2 zlib1g-dev
git clone git@bitbucket.org:kuldeepmeel/mis.git --recursive
cd mis
cd muser2-dir/src/tools/muser2
make
cp muser2 ../../../../
cd ../../../../
g++  -o togmus togmus.cpp -lz
```

### Running

```
/.mis.py --out=formula.out --log=log.txt --timeout=300 --useind 1 formula.cnf

```

runs MIS on the DIMACS CNF file 'formula.cnf', writing the generated minimal independent support to a file called 'formula.out' with logfile log.txt and a timeout of 300 seconds.
useInd=1 indicates to the program to find a minimal independent support over the user-supplied independent support given in formula.cnf in 'c ind' format.
Run with '-h' option to print detailed usage and other advanced options.


### Contact ###

Kuldeep S. Meel (meel@comp.nus.edu.sg)
