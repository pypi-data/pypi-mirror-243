#!/bin/bash

conda install -y -c ifilot pyqint>=0.9.3.0 pylebedev>=0.1.1.1
nosetests tests/*.py
