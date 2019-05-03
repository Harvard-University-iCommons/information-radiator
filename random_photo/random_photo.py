import json
import os
import boto3
import random

page_html_prefix = '''<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body, html {
  height: 100%;
  margin: 0;
}

.bg {
  /* The image used */
  background-image: url("'''

page_html_suffix = '''");

  /* Full height */
  height: 100%;

  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
</head>
<body>

<div class="bg"></div>

</body>
</html>
'''


def lambda_handler(event, context):
    # TODO implement
    bucket = os.environ['photo_bucket']
    folder = os.environ['photo_folder']
    
    client = boto3.client('s3')
    
    # list the contents of the folder in the S3 bucket
    
    bucket_list = client.list_objects_v2(Bucket=bucket, Prefix='{}/'.format(folder))
    
    photos = bucket_list['Contents']
    
    # remove any items from photos that have a size of 0
    for p in photos:
        if p['Size'] == 0:
            photos.remove(p)
    
    p = random.choice(photos)

    url = 'https://s3.amazonaws.com/{}/{}'.format(bucket, p['Key'])

    return {
        'statusCode': 302,
        'headers': {
            'Location': url,
        },
    }
