#!/bin/bash
export DISPLAY=:0
export LD_LIBRARY_PATH=.
./chrome --no-sandbox --disable-xss-auditor --disable-improved-download-protection --js-flags='--noblock_tainted' --enable-logging=stderr --v=1 > no_display_log_file 2>&1 &


