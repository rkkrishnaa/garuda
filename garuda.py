#!/usr/bin/python
import os
import logging
import ConfigParser
import json
import datetime
import boto3

class garuda:
    # app configuration
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('garuda.cfg')
        self.execution_mode = self.config.get('DEFAULT', 'execution_mode')
        self.debug = (self.config.getboolean('DEFAULT', 'debug'))
        self.log_dir = self.config.get('DEFAULT', 'log_dir')
        self.access_key = self.config.get('credentials', 'access_key')
        self.secret_access_key = self.config.get('credentials', 'secret_access_key')
        os.environ["AWS_ACCESS_KEY_ID"] = self.access_key
        os.environ["AWS_SECRET_ACCESS_KEY"] = self.secret_access_key

    # logger definition
    def logger(self, debug):
        '''This method requires a boolean value to enable or disable logging to the console
        Log files will be stored in the configured log directory
        '''

        log_path = self.log_dir + '/s3explorer.log'
        if debug == True:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
        else:
            logging.basicConfig(filename=log_path, level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
            print('logging on ' + log_path)

    def create_session(self, type):
        '''This method creates a connection to aws s3 service by using client or resource class returns
        connection object which is used by other methods.
        '''

        if type == 'client':
            connection = boto3.client('s3')
            return connection
        elif type == 'resource':
            connection = boto3.resource('s3')
            return connection
        else:
            print('Invalid Connection')

    def list_bucket(self, connection):
        '''This method returns the information about list of s3 buckets and creation date.
        It is used by other methods to get more information about s3 bucket available in the aws account
        '''

        buckets = connection.list_buckets()
        bucket_name = []
        bucket_creation_date = []
        for i in buckets['Buckets']:
            bucket_name.append(i['Name'])
            bucket_creation_date.append(i['CreationDate'])

        return bucket_name, bucket_creation_date

    def count_objects(self, bucket, creation_time):
        '''This method returns the information about s3 bucket such as
        bucket name, bucket size in mega bytes rounded to four decimal points, creation time, last updated time,
        number of objects stored in the bucket.
        '''

        count = 0
        s3data = []
        s3info = {}
        bucket_size = []
        total_objects = []
        total_size_in_mb = []
        total_cost_in_usd = []
        for j in range(len(bucket)):
            conn = self.create_session(type='client')
            total_obj = conn.list_objects(Bucket=bucket[j])
            # print (total_obj.items())
            size = 0
            for key, value in total_obj.items():
                if key == 'Contents':
                    for i in range(len(value)):
                        logging.info('iteration: ' + str(i))
                        logging.info('size in bytes before iteration: ' + str(size))
                        size = size + value[i]['Size']
                        logging.info('size after iteration: ' + str(size))
                        logging.info('object size in bytes: ' + str(value[i]['Size']))
                        logging.info('bucket size in bytes: ' + str(size))
                        logging.info('last_updated' + str(value[i]['LastModified']))
                        bsize = size
                    value[i]['Size'] = 0
                    size = 0

            if value != False:
                bucket_size.append(bsize)
                s3info['bucket_name'] = bucket[j]
                s3info['creation_time'] = str(creation_time[j])
                s3info['number_of_objects'] = str(len(value))
                bucket_size_in_mb_per_bucket = round((float(bucket_size[j]) / (1024 * 1024)), 4)
                s3info['bucket_size_in_mb'] = str(bucket_size_in_mb_per_bucket)
                s3info['last_updated'] = str(value[i]['LastModified'])
                current_time = datetime.datetime.utcnow()
                current_time = str(current_time)
                day = int(current_time.split(" ")[0].split("-")[2])
                bucket_size_in_gb = round((bucket_size_in_mb_per_bucket / 1024), 4)
                # s3 standard storage cost for first 50TB / Month in us-east-1 is $0.023 per GB
                storage_cost_per_bucket = round(float(0.023 * ((bucket_size_in_gb / 30) * day)), 4)
                s3info['storage_cost'] = str(storage_cost_per_bucket)
                total_objects.append(len(value))
                total_size_in_mb.append(bucket_size_in_mb_per_bucket)
                total_cost_in_usd.append(storage_cost_per_bucket)
                s3data.append(s3info.copy())
            else:
                bucket_size.append('0')
                s3info['bucket_name'] = bucket[j]
                s3info['creation_time'] = str(creation_time[j])
                s3info['number_of_objects'] = '0'
                s3info['bucket_size_in_mb'] = bucket_size[j]
                s3info['last_updated'] = str(creation_time[j])
                s3info['storage_cost'] = '0.0'
                s3data.append(s3info.copy())

        s3data = json.dumps(s3data, sort_keys=True, indent=2)
        total_count = {"total_buckets": str(len(bucket)), "total_objects": str(sum(total_objects)),
                       "total_size_in_mb": str(sum(total_size_in_mb)), "total_cost_in_usd": str(sum(total_cost_in_usd))}
        total_count = json.dumps(total_count, sort_keys=True, indent=2)

        return s3data, total_count

    def get_total_objects(self, connection):
        '''This method return the total count of the objects in your aws account'''

        count = 0
        for bucket in connection.buckets.all():
            for key in bucket.objects.all():
                count = count + 1

        count = {"total_objects": str(count)}
        count = json.dumps(count, sort_keys=True, indent=2)
        return count

    def main(self):
        # logger based on execution mode
        try:
            if self.execution_mode == 'cli':
                self.logger(self.debug)
            else:
                self.logger(debug=False)
        except Exception as e:
            print('Failed to execute program due to exeception: ' + str(e))
            exit(1)
