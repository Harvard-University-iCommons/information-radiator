import requests
from bs4 import BeautifulSoup, Comment
import boto3
import os

template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>This Day in Computer History</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Alfa+Slab+One|EB+Garamond:500,500i|Lato" rel="stylesheet">
    <style type="text/css" media="screen">
        {}
    </style>
</head>
<body>

    {}

</body>
</html>
'''
css = '''
        .chm-tdih-entry-date {
            display: block;
            text-transform: capitalize;
            font-family: Lato;
            font-size: 2em;
        }
        .chm-tdih-entry-title {
            display: block;
            font-family: 'Alfa Slab One';
            font-size: 4em;
            line-height: 1em;
            color: crimson;
            margin-top: .5em;
            margin-bottom: .5em;
        }
        .chm-tdih-entry-content {
            font-family: 'EB Garamond';
            font-size: 1.5em;
        }
        .chm-exhibit-container {
            margin-left: 10%;
            margin-right: 10%;
            margin-top: 4em;
        }
        .pull-left {
            float: left;
        }
        .image {
            margin-right: 3em;
        }
'''

def get_content():
    page = requests.get('https://www.computerhistory.org/tdih/');

    soup = BeautifulSoup(page.text, 'html.parser')

    today = soup.find('div', attrs={'class': 'chm-exhibit-container'})
    new_doc = template.format(css, today)

    return new_doc


def fetch_history(event, context):

    bucket = os.environ['history_bucket']
    key = os.environ['history_key']

    body = get_content()
    print('bucket: {} key: {}'.format(bucket, key))
    client = boto3.client('s3')

    client.put_object(
        ACL='public-read',
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType='text/html',
    )

if __name__ == "__main__":
    print(get_content())
