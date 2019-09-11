[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIS computes **minimal independent support** for a given CNF formula. This means that it gives the user a set of variables that fully determine all the other variables' settings. So for example, if you give it an electronic circuit, it might give you all its input variables. It gives a minimal set, but it may not be the minimum set.

The implementation is based on MIS algorithm by Alexander Ivrii, Sharad Malik, Kuldeep Meel, and Moshe Vardi see [CP'15 paper](http://link.springer.com/article/10.1007/s10601-015-9204-z), which won the Best Student Paper Award. MIS uses [MUSer2](https://bitbucket.org/anton_belov/muser2) by Anton Belov and Joao Marques-Silva, paper [here](https://satassociation.org/jsat/index.php/jsat/article/view/101).

### Docker usage
Run on a file `formula.cnf` that **must** have a correct DIMACS header `p cnf vars clauses`:

```
docker run --rm -v `pwd`/formula.cnf:/in msoos/mis /in
```

### Building

```
apt-get install minisat2 zlib1g-dev g++
git clone https://github.com/meelgroup/mis
cd mis
git submodule update --init
make
```

### Usage
Please beware that you *must* have a correct DIMACS header in your input 'formula.cnf' file, then run:

```
$ ./mis.py formula.cnf
Running togmus: './togmus formula.cnf formula.gcnf False'
togmus executed in 0.01
Running muser2: 'muser2 -v 0 -grp -comp -minisats -order 4 -T 310 formula.gcnf > formula.tcnf'
muser2 executed in 0.25
num independent vars: 19
** Copy-paste the following line in the top of your CNF for ApproxMC **
c ind 3 4 7 8 10 11 14 17 18 26 30 35 36 39 42 47 60 62 67 0
```
The system has found 19 variables to be a minimal independent support. It also prints the exact line you have to copy-paste to the top of your CNF file if you want to use our [ApproxMC](https://github.com/meelgroup/approxmc) approximate model counter. It is *highly* recommended to use MIS before running ApproxMC.

In case the above doesn't terminate, you can push Ctrl+C and it will print the intermediary best independent set. Or you can run the above command with an explicit timeout using the `--timeout` option, giving timeout in seconds:

```
$ ./mis.py --timeout 100 formula.cnf
Running togmus: './togmus formula.cnf formula.gcnf False'
togmus executed in 0.01
Running muser2: 'muser2 -v 0 -grp -comp -minisats -order 4 -T 310 formula.gcnf > formula.tcnf'
muser2 executed in 0.25
num independent vars: 22
** Copy-paste the following line in the top of your CNF for ApproxMC **
c ind 3 4 7 8 10 11 14 17 18 19 26 30 31 35 36 39 42 47 60 62 63 67 0
```

### Better Independent Sets

You can try your luck and ask the system to try to find different minimal independent sets. It will then print only the smallest:

```
$ ./mis.py formula.cnf --maxiter 50
[...]
num independent vars: 17
** Copy-paste the following line in the top of your CNF for ApproxMC **
c ind 3 4 7 8 10 11 14 17 18 30 35 39 42 47 60 62 67 0
```


### Minimising an independent support
In case you already have a set that you know is independent, and you want to minimise that, then you can give that set to the sytem by putting in your CNF a line that lists these variables (variable numbers start with 1), ending the line with a 0. For example, if variables 1, 5, 22 and 124 are independent you need to put at the top in the CNF:

```
c ind 1 5 22 124 0
```

Now you can run the tool with the option `--useind`:
```
$ ./mis.py formula.cnf --useind
[...]
num independent vars: 2
** Copy-paste the following line in the top of your CNF for ApproxMC **
c ind 1 22 0
```

The system then will find a minimal independent support that is a subset of the variables given.

### Issues, questions, bugs, etc.
Please click on "issues" at the top and [create a new issue](https://github.com/meelgroup/mis/issues/new). All issues are responded to promptly.
