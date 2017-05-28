# DjangoZipS3

S3 has no built-in functionality to download a directory as a zip, so I had to whip this up for one of my projects myself.

In this Python module, given the path to a folder in S3, a zip file will be created with a matching directory structure, then uploaded to S3 under a folder called 'zips3'. 

The zip will be given an expiration of 1 day so that it auto removes itself ASAP. A URL is generated for the zip file and returned, so that in your Django view, you can redirect the user to that link to instantly download the files.

## Example usage
```py
from django_zips3 import generate_url
from django.shortcuts import redirect

def my_view(request):
    # Make sure the path begins with a '/' and does not end in one
    download_url = generate_url('/path/to/a/bucket/folder')

    return redirect(download_url)
```