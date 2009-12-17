import os
import boto.s3

import mysociety.config

boto_connection = boto.s3.connection.S3Connection(
    mysociety.config.get('AWS_KEY'), 
    mysociety.config.get('AWS_SECRET')
    )

# This should get the bucket if it exists or create it if not.
bucket = boto_connection.create_bucket(mysociety.config.get('S3_BUCKET'))

    
def store_file(key_name=None, location=None, delete_file=False):
    key = boto.s3.key.Key(bucket)
    key.key = key_name

    key.set_contents_from_filename(location)
        
    if delete_file:
        os.remove(location)

def get_by_key(key_name):
    key = boto.s3.key.Key(bucket)
    key.key = key_name

    key.
