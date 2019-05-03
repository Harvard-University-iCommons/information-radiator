import requests
from bs4 import BeautifulSoup, Comment
import boto3
import os


def remove_all(soup, tag, cssclass):
    for element in soup.find_all(tag, attrs={'class': cssclass}):
        element.decompose()

css = '''
    h1 {
        font-weight: 400;
        margin: 0px;
    }

    a {
        color: black;
        text-decoration: none;
    }

    .article-header-container {
        text-align: center;
        font-family: Lato;
        font-size: 2em;
        color: gray;
    }

    .word-and-pronunciation {
        font-family: Alfa Slab One;
        font-size: 3em;
        text-align: center;
        color: crimson;
    }

    .word-attributes span {
        color: gray;
        padding-left: 1em;
        padding-right: 1em;
    }

    .word-attributes :first-child {
        border-right: 1px solid gray;
    }

    .wod-definition-container {
        margin-left: 15%;
        margin-right: 15%;
        font-family: Lato;
    }

    .wod-definition-container h2 {
        font-size: 2em;
    }
    .wod-definition-container p {
        font-family: 'EB Garamond';
        font-size: 1.5em;
    }
'''

template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Word of the Day</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Alfa+Slab+One|EB+Garamond:500,500i|Lato" rel="stylesheet">
    <style type="text/css" media="screen">
        {}
    </style>
</head>
<body>

    {}

    {}

</body>
</html>
'''

def get_content():
    page = requests.get('https://www.merriam-webster.com/word-of-the-day');

    soup = BeautifulSoup(page.text, 'html.parser')
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    remove_all(soup, 'span', 'scrollDepth')
    remove_all(soup, 'div', 'hidden')
    remove_all(soup, 'div', 'nav-arrow-container')
    remove_all(soup, 'a', 'play-pron')

    word = soup.find('div', attrs={'class': 'article-header-container'})
    definition = soup.find('div', attrs={'class': 'wod-definition-container'})
    new_doc = template.format(css, str(word), str(definition))

    return new_doc


def fetch_wod(event, context):

    bucket = os.environ['wod_bucket']
    key = os.environ['wod_key']

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
