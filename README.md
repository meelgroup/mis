# MIS #

### What is it? ###
MIS computes minimal Independent Support for a given CNF formula. The implementation is based on MIS algorithm proposed in our [CP'15 paper](http://link.springer.com/article/10.1007/s10601-015-9204-z), which also won the Best Student Paper Award. 

### Download ###
```
#!shell

   git clone git@bitbucket.org:kuldeepmeel/mis.git --recursive

```
### Licensing ###
Please see the file `LICENSE-MIT`.

### Installing MIS ###

MIS must be built using GCC 4.8.x or higher and requires libz.

To build MIS:

1) First compile MUser2  (refer to MUser2's README for further details):
   

```
#!shell

   cd Muser2-Source/src/tools/muser2/
   make allclean
   make

```
   Put the muser2 binary to the top directory. 
   
2) Install libz if required:


```
#!shell

   sudo apt-get install zlib1g-dev

```
   
3) Compile togmus:
  

```
#!shell

   g++  -o togmus togmus.cpp -lz   


```
As described below, we provide the wrapper script 'MIS.py' in this directory as an easy way to invoke MIS.



### Running MIS ###

You can run MIS using the 'MIS.py' Python script in this directory.
For example, the command


```
#!shell

   python MIS.py -output=formula.out -logging=1 -log=log.txt -timeout=300 -useInd=1 formula.cnf 

```

runs MIS on the DIMACS CNF file 'formula.cnf', writing the generated minimal independent support to a file called 'formula.out' with logfile log.txt and a timeout of 300 seconds.
useInd=1 indicates to the program to find a minimal independent support over the user-supplied independent support given in formula.cnf in 'c ind' format.
Run with '-h' option to print detailed usage and other advanced options.


### Contact ###

Kuldeep Meel (kuldeep@rice.edu)