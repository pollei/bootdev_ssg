#! /usr/sbin/bash
/usr/sbin/python3 src/main.py
 
cd docs && /usr/sbin/python3 -m http.server 8888
