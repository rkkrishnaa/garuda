# garuda
* Garuda is described as the king of birds with eagle-like features. Garuda is generally a protector with power to swiftly go anywhere, ever watchful. Here, Garuda is a cli tool written in python to analyze AWS resources. The ultimate goal of the tool is to get a deep insight to our AWS account. So that we can track our cloud resource usage and avoid unwanted billing charges.
* Currently this tool will give you a detailed information of s3 buckets in your aws account such as total number of s3 buckets, number of objects stored, total storage cost, and details about creation date, last changes made, etc.
* It is a standalone and light weight tool and it does not require extra softwares to be installed.
* It mainly uses boto3(aws sdk for python) to retrive data from AWS and other built-in modules such as os, time, datetime, ConfigParse, logging, json and prettytable for various purposes.

Hardware and Software Requirements:
------------------------------------
1. A physical or virtual machine with minimum RAM 2GB, HDD 10GB, PROCESSOR 1 Cores.
2. Linux/OSX.
3. Internet connection without firewall restictions to access aws service.

Steps to use garuda cli tool:
------------------------------
* `git clone https://github.com/rkkrishnaa/garuda.git`
* set environment path to access garuda-cli
* GARUDA_HOME is a path of the repository in your local system
* `export GARUDA_HOME='/home/rkkrishnaa/garuda'`
* ``export PATH=$PATH:$GARUDA_HOME``
* `garuda-cli s3`
![garuda](garuda-cli-s3.png?raw=true)
