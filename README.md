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
* `cd $GARUDA_HOME`
* `chmod +x garuda-cli`
* Ensure boto3 and prettytable library is installed in your system otherwise install it via pip. Please ignore the step if  these packages are already installed
`pip install -r requirements.txt`
* Edit aws credentials in garuda.cfg file
* `garuda-cli s3`
![garuda](garuda-cli-s3.png?raw=true)

Garuda-app:
-----------
* Garuda-app is an extension of garuda cli. It is a monitoring tool for your hosts running in onpremises environment and in cloud. It is in development state. I have just created the schema and implemented some important api right now(attached api methods and postman schema for testing). I intend to create this tool which should be capable of running in different environments like virtual machine, container and in serverless infrastructre to leverage the capabilty of microservices. 
![garuda](garuda-app.png?raw=true)

The ultimate goal of the application is to monitor the hosts in the cluster without any manual configuration. I am writing agent application in such a way that it should not poll the server continuosly like other monitoring tools. It is a light weight agent it uses amqp and http rest calls for commnications and data exchanging. Users can create their own dashboard with custom metrics. Moreover it will give you an insight to your aws account. I will share the api in the form of swagger schema for portability. 


![garuda](arch.png?raw=true)

Please share your feedback to improve the functionality of this application.
