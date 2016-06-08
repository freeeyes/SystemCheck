#!/bin/sh

#$HOME/.bash_profile

source $HOME/.bash_profile

cd $HOME/python_shell/src

#export export MYSCONS=/m2myw/schang/scons-2.1.0
#export SCONS_LIB_DIR=$MYSCONS/engine
#export ORACLE_BASE=/oracle
#export ORACLE_HOME=$ORACLE_BASE/app
#export ORACLE_SID=m2mdb
#export PATH=$PATH:$ORACLE_HOME/bin
#LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib:/usr/local/lib:$ACE_ROOT/lib
#export LD_LIBRARY_PATH

/usr/local/python27/bin/python $HOME/python_shell/src/check_main.py >> $HOME/python_shell/src/2.log 2>&1
