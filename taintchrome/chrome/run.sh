#!/bin/bash
export DISPLAY=:0
export LD_LIBRARY_PATH=.
./chrome --no-sandbox --disable-xss-auditor --disable-improved-download-protection --js-flags='--noblock_tainted'
