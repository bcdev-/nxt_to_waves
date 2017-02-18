#!/usr/bin/env python3
import sys
from src.gateway import Gateway

if sys.version_info < (3, 0):
    print("This program has to be run with Python 3.")
    print("Try: python3 %s" % sys.argv[0])
    sys.exit(1)

if __name__ == "__main__":
    gateway = Gateway()
    gateway.start()
