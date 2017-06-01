# DjangoZipS3

S3 has no built-in functionality to download a directory as a zip, so I had to whip this up for one of my projects myself.

Maybe you have users uploading files to a specific media directory which happens to be S3 in deployment. You want the user to be able to download all of the files under a certain folder as a single zip, rather than having them download files individually. This module aims to fix that issue.

In this Python module, given the path to a folder in S3, a zip file will be created with a matching directory structure, then uploaded to S3 under a folder called 'zips3'. 

The zip will be given an expiration of 1 day so that it auto removes itself ASAP. A URL is generated for the zip file and returned, so that in your Django view, you can redirect the user to that link to instantly download the files.

## Install
This package is not pip installable (yet!)

```sh
cd django_zips3
sudo python setup.py install
```

## Example usage
```py
from django_zips3 import generate_url
from django.shortcuts import redirect

def my_view(request):
    # Make sure the path begins with a '/' and does not end in one
    download_url = generate_url('/path/to/a/bucket/folder')

    return redirect(download_url)
```

In settings.py, add your AWS access keys and the bucket name you have your files stored in.

```py
AWS_STORAGE_BUCKET_NAME = 'bucket_name'
AWS_ACCESS_KEY_ID = 'your_aws_key_id'
AWS_SECRET_ACCESS_KEY = 'your_aws_secret_key'
```

Check out the example django project for more information :) (It is currently very empty)
