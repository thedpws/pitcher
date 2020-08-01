#!/bin/sh


patch "env/lib/python3.8/site-packages/timidity/player.py" < patches/player.patch
patch "env/lib/python3.8/site-packages/timidity/parser.py" < patches/parser.patch
patch "env/lib/python3.8/site-packages/timidity/__main__.py" < patches/main.patch
