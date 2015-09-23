#/bin/bash

source ../ENV/bin/activate
./serve.py &
./user.py &
./hose.py &
