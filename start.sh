#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export dbcred='dbms/dbms1234@localhost:1521'
pip3 install -r requirements.txt
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:LD_LIBRARY_PATH
source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000
