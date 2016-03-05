Installing MIS
--------------
MIS must be built using GCC 4.8.x or higher and requires libz.

To build MIS:

1) First compile MUser2  (refer to MUser2's README for further details):
   

```
#!shell

   cd Muser2-Source/src/tools/muser2/
   make allclean
   make
   Put the muser2 binary to the top directory. 

```
   
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



Running MIS
---------------
You can run MIS using the 'MIS.py' Python script in this directory.
For example, the command


```
#!shell

   python MIS.py -output=formula.out -logging=1 -log=log.txt -timeout=300 formula.cnf 

```

runs MIS on the DIMACS CNF file 'formula.cnf', writing the generated minimal independent support to a file called 'formula.out' with logfile log.txt and a timeout of 300 seconds.
Run with '-h' option to print detailed usage.

---
Contact
---
Kuldeep Meel (kuldeep@rice.edu)