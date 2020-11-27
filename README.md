# Don't Trust The Locals: Investigating the Prevalence of Persistent Client-Side Cross-Site Scripting in the Wild
This repository contains our code base used to automatically generate exploit candidates for 
Reflected Client-Side XSS and Persistent Client-Side XSS.
It is a product of our [work](https://swag.cispa.saarland/papers/steffens2019locals.pdf) published at NDSS 2019.
  
## Taint Engine
The generation is based on the flows collected by the tainted Chromium engine presented by
 [Lekies et al.](https://publications.cispa.saarland/3/1/domxss.pdf). 

**Update 2019/09/26**: we are releasing the (very old!!!) Chromium engine. Please find it in the `taintchrome` folder. This is a prototype we developed after our [USENIX 2014 paper](https://swag.cispa.saarland/papers/stock2014precise.pdf) and therefore has partial ability to block tainted flows. To start the engine, you therefore have to use specific command line flags to ensure that tainted flows are just recorded and not blocked. We have recently run this in an Ubuntu 16.04 LTS VM (you may need to put libgcrypt.so.11 (md5 `bb6c4e40803d0e59e2cc03e23c9861cd`) in your library folder for it to work).

```
./chrome --no-sandbox --disable-xss-auditor --disable-improved-download-protection --js-flags='--noblock_tainted'
```

**Note that this browser is outdated and Chromium has had known-exploitable bugs in this version. We take absolutely no responsibility for this prototype, neither in terms of functionality nor security. You run this at your own risk**

Whenever a tainted data flow is detected in a sink, the engine tries to locate the function `___DOMXSSFinderReport` in the current window's global scope. We used an extension to inject this code into each page we visited. To get you started, we have put a minimal JavaScript example of the function which can be used to log tainted data flows to the console in the `taintchrome/minimal_extension` folder. 

If you choose to not use the taint engine, check out our examples of such flows, which can be found in the `examples` directory, with EXAMPLE1 being annotated and each other example providing different 
combinations of sources and sinks.

# Flows
In general we consider *findings* and *sources* as provided to us by the tainted chromium engine.  
A finding in this case consists of all the different parts(sources) of one string which ended up in one of our sinks.

document.write('<script src="//ad.com/url='+ location.href + '></ script>')  

In the above example the finding consists of the complete string, whereas we have three sources, 
that is the beginning and end of the string which are hardcoded(SOURCE_BENIGN) and the middle part which 
originates from the URL of the frame(SOURCE_LOCATION_HREF).

For an annotated example of the structure which is expected by the Exploit generation refer to EXAMPLE1.
# Setup
You can setup a Docker container to test the project making use of the the following two commands in the project root.
```bash
docker build -t exploit_generator .
docker run -it exploit_generator:latest
```
If you want to setup the environment natively you need to install the required dependencies as follows:
```bash
pip install -r requirements.txt
```
# Usage
Generating exploits for a specific finding can be performed as follows:
```python 
from generator import generate_exploit_for_finding

finding = # fetch finding from somewhere
exploits = generate_exploit_for_finding(finding)
```

The return value of `generate_exploit_for_finding` is a list of exploit candidates which will then need to be validated
 in order to ensure the presence of the same flow given the altered values.

You can run the tests on 6 examples provided in the examples subdirectory, with ```tests.py``` currently 
running the first example.
```bash
python tests.py
```

Optional commandline arguments can be ```--payload alert(1)``` or ```--debug```, with the former allowing to change 
the payload which is used when generating exploit candidates and the latter activating log output.  
There is one small caveat to changing the payload, which should be easy to find but prevents copycatting.

# Script Source Exploits
When we observe a flow into the src property of a script which happens before the path of the url start, we can redirect the hostname to one under our own control. In ```config.py``` it can be configured which hostname should be used and in ```configs/``` you can find the NGINX server block which we used to always host the attacker file no matter which subdomains/path where intended by the developers.

# License
This project is licensed under the terms of the AGPL3 license which you can find in ```LICENSE```.

# Modifications by Zifeng Kang
## Append value to logs
Append a 'TAINTFINDING' string to the extension outputs so that they can be easily distinguished from other chrome outputs. 

## Add auto scraping scripts
In taintchrome/chrome/scrape-auto.sh, bash scripts do web crawling and website scanning automatically. They will also record the outputs by chrome into log_files, and each distinguished domain will be recorded in a distinguished log_file. 

Usage: 

```
cd taintchrome/chrome
./scrape-auto.sh <# of start line - 1> <# of end line> <flushing parameter> <max_num_window>
```

The sh script takes 4 parameters. It reads from a csv recording all of the websites to be crawled. Choose # of the start line and end line of what you want to crawl.

The third parameter controls whether or not to flush the logs. If you don't want flushing, just type 2 there. 

The fourth parameter is how many windows you want the chrome to open simultaneously in a single iteration. In one iteration, the script opens as many as <max_num_window> windows, sleeps for a while to wait all windows loading, and then closes these windows to start a new interation (opening new bunch of windows). You may adjust the source code for your own needs. 

The following example means the script will crawl all of the websites from line 1 to line 1000, no flushing, and open 30 windows simultaneously in a single iteration: 

```
cd taintchrome/chrome
./scrape-auto.sh 0 1000 2 30
```

If you just want to crawl one particular website, you can put it into one csv file, change the file name in the last line of the scrape-auto.sh to your file name, and run: 

```
cd taintchrome/chrome
./scrape-auto.sh 0 1 2 1
```

The crawling scripts don't support crawling sub-pages, though. (Perhaps done by adding a self-made chrome extension. ) This is in the TODO-list of this project. 

## Auto-processing outputs in test.py
In test.py, the python codes can read and distinguish the desired information. Afterwards, the program tries to generate an exploit according to such info. 

Note: However, for simplicity if there are errors e.g. UnicodeDecodeError, the log_file will be skipped. More precise error-handling is in the TODO-list. 
