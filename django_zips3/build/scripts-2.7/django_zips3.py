from __future__ import print_function
from django.conf import settings
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.s3.lifecycle import (
    Lifecycle,
    Expiration,
)
import os, uuid, boto, zipfile, shutil

def zip(src, dst):
    """
    Zips a src directory, saved to the destination
    """
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname))
            zf.write(absname, arcname)
    zf.close()

def generate_url(path):
    """
    Given the path to bucket directory, each file under that prefix is
    downloaded to a temporary directory of the same name. The folder is then
    zipped, and uploaded to a folder in the bucket called "s3zip". Everything in this
    folder is set to expire in 1 day. The URL to the zip is returned for the user to
    redirect to, to download.
    """

    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

    # Name the zip file (and store it) as the innermost directory that
    # we are zipping everything from
    temp_directory = path[path.rfind('/')+1:]

    # Create the directory that will house all of the files we are
    # downloading from S3
    try:
        os.makedirs(temp_directory)
    except OSError as err:
        print("OS error: {0}".format(err))

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                           AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(bucket_name)

    # Get every key with the 'path' prefix
    # We need to determine the directory structure and recreate it
    for key in bucket.list(prefix=path[1:]):
        # If my key was located in /dir1/dir12/key.txt
        # and my path was dir1, then subdirectory_string would be
        # dir12/key.txt
        key_name = str(key.name)
        subdirectory_string = key_name[key_name.find(path)+len(path):]

        if subdirectory_string.endswith('/'):
            try:
                os.makedirs(temp_directory + subdirectory_string)
            except OSError as err:
                print("OS error: {0}".format(err))
        else:
            key.get_contents_to_filename(key_name[key_name.find(temp_directory):])

    zip(temp_directory, temp_directory)

    lifecycle = Lifecycle()
    lifecycle.add_rule(
        'rulename',
        prefix='s3zip',
        status='Enabled',
        expiration=Expiration(days=1)
    )

    bucket.configure_lifecycle(lifecycle)

    k = Key(bucket)
    k.key = 'zips3/' + temp_directory + '.zip'
    k.set_contents_from_file(open(temp_directory+'.zip'))
    s3 = S3Connection(settings.AWS_ACCESS_KEY_ID,
                      settings.AWS_SECRET_ACCESS_KEY,
                      is_secure=True)
    url = s3.generate_url(60, 'GET',
                          bucket=settings.AWS_STORAGE_BUCKET_NAME,
                          key=k.key,
                          force_http=True)

    shutil.rmtree(temp_directory)
    os.remove(temp_directory+'.zip')

    return url
