#!/bin/bash
mkfifo turbinepipe
python TurbineListener.py < turbinepipe&
python tester.py > turbinepipe
