#!/bin/bash

sudo apt-get -y install python3-pip virtualenv
rm -Rf env activate
virtualenv -p python3 env 
ln -s env/bin/activate .
source activate
pip3 install requests pyblake2 pycurve25519 base58 pysha3

