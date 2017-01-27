#!/usr/bin/env python
import time, sys

while True:
   sys.stdout.write("Hello\0")
   #sys.stdout.flush()
   time.sleep(.5) 
