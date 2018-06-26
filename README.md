TVM/NNVM environment setup
==========================

This document describes the working process regarding TVM/NNVM project arranged
in Moscow Research center.

The main machine is a Linux workstation with [NixOS](www.nixos.org) operating
system installed. This operating system has a notion of build environments
where users may define the exact set of packages and versions they use. This
definitions are stored as 'expressions' in Nix language. By using this feature,
developers may be sure they use exactly the same versions of environment which
make collaborative development easier.

This repository expects the NixOS [packages](www.github.com/nixos/nixpkgs) tree
to be derived from the following commit:

    commit 08d245eb31a3de0ad73719372190ce84c1bf3aee (HEAD -> nixos-18.03)
    Author: Benjamin Hipple <bhipple@protonmail.com>
    Date:   Sat Jun 9 19:08:59 2018 -0400

Server used in Moscow office has been already set up accordingly.


Overall procedure
-----------------

  1. Login to `ws` machine (contact Sergey Mironov mWX579795 in order to get user
     account)

        $ ssh 10.122.85.37

  2. Clone the current repository recursively

        $ git clone --recursive https://http://code.huawei.com/mrc-cbg-opensource/nixtvm
        $ cd nixtvm

  3. Enter the development environment

     The build hook (see `tvm.nix`) will set up environment and change directory to
     `nixtvm/tvm`.

        $ nix-shell tvm-llvm.nix -A shell

     Important tasks such as `make`, `clean` and `test` are wrapped with shell
     functions. See `shell` expression defined in `tvm.nix` for details.

  4. Build the project using either docker, or directly using `cmake` build
     system, as described in [Official manual](https://docs.tvm.ai/install/index.html).

  5. Use TVM as a library to build and test solutions


Building the TVM/NNVM
=====================


Build TVM/NNVM using docker
---------------------------

TVM/NNVM project includes scripts specifying the automated build and test
procedures to be used by [Jenkins](https://jenkins.io/) facilities.
This scripts were examined and the minimal build procedure was extracted in
order to be able to reproduce various build conditions.

General procedure is encoded in `Jenkinsfile` and `test/ci_build/ci_build.sh`
files. In order to run the docker software, one have to execute the following
command:

    $ sh ./tests/ci_build/ci_build.sh cpu ./tests/scripts/task_build.sh build

As a result, the Docker image should be generated, the current source folder
should be loop-mounted inside and the build procedure should be completed. Note
that Docker doesn't fix the dependencies like NixOS does, so one should prefer
native builds in day-to-day development.

`nixtvm` environment defines `dmake` and `dtest` commands to simplify the docker
execution:


    $ type dmake  # Review the build algorithm
    $ dmake

    $ type dtest  # Review the test algorithm
    $ dtest

More test commands may be extracted using `cat Jenkinsfile | grep docker`


Native build of TVM/NNVM
------------------------

Direct build assumes we are building TVM from source without any virtualisation
employed. [Official manual](https://docs.tvm.ai/install/index.html) describes
the following process:

  * Creating `build` folder in TVM tree for storing temporary files
  * Copying the config from template folder to `build/config.cmake` file
  * Editing the configuration to enable/disable components
  * Running `cmake ..` to generate the Makefile
  * Running `make` to perform actual make

In order to simplify this proceess, the current working environment includes
`nmake` shell function. After entering the nix-shell, developers may execute the
following commands to perform basic LLVM build:

    $ type nmake  # Review the build algorithm
    $ nmake

After the build is complete, `build-native` folder will contain `*.so` libraries
to link with C++ applications.

`nclean` command is also defined

    $ type nclean  # Review the algorithm
    $ nclean

Running executables using TVM/NNVM
==================================

General information
-------------------

We expect that native build procedure described above has been completed.

Inside `nix-shell tvm-llvm.nix -A shell`, users are able to run development
tools such as python, g++, gdb, etc. `LD_LIBRARY_PATH` and `PYTHONPATH` include
build directory. After running `nmake` shell function, just-built libraries
should appear in `build-native` directory.

In order to run examples, the following shell environment variables should be
changed:

    export TVM=$CWD/tvm
    export PYTHONPATH="$CWD/src/tutorials:$TVM/python:$TVM/topi/python:$TVM/nnvm/python:$PYTHONPATH"
    export LD_LIBRARY_PATH="$TVM/build-native:$LD_LIBRARY_PATH"
    export C_INCLUDE_PATH="$TVM/include:$TVM/dmlc-core/include:$TVM/HalideIR/src:$TVM/dlpack/include:$TVM/topi/include:$TVM/nnvm/include"
    export CPLUS_INCLUDE_PATH="$C_INCLUDE_PATH"
    export LIBRARY_PATH=$TVM/build-native

`nixtvm/src` folder contains tutorials used as a playground for studying the TVM. For
example, to test the reduction code in Python, one should run:


Running Python programs using TVM/NNVM
--------------------------------------

In order to run Python programs, the `PYTHONPATH` variable should point to build
directories. The environment does it automatically. For example, to run code
from `nixtvm/src/reduction.py` one may run:

    $ ipython
    >> from reduction import *
    >> lesson1()


Running C++ programs using TVM/NNVM
-----------------------------------

C++ programs should know paths to `tvm/include` and `tvm/build-native`
directories to include and link the runtime. The `nixtvm` scripts set the
related `C_INCLUDE_PATH`, `CPLUS_INCLUDE_PATH` and `LD_LIBRARY_PATH` variables.

    [nix-shell:~/proj/nixtvm/tvm]$ g++ -ltvm ../src/tutorials/tvm0.cpp
    [nix-shell:~/proj/nixtvm/tvm]$ ./a.out


