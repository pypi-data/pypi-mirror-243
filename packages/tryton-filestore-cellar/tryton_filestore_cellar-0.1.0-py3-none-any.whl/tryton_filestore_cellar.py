# This file is part of filestore-cellar. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import os
import uuid

from boto.s3.connection import OrdinaryCallingFormat, S3Connection
from boto.s3.key import Key

from trytond.config import config
from trytond.filestore import FileStore


class FileStoreCellar(FileStore):

    def __init__(self):
        self.__bucket = None

    @property
    def bucket(self):
        if not self.__bucket:
            conn = S3Connection(
                aws_access_key_id=os.getenv('CELLAR_ADDON_KEY_ID'),
                aws_secret_access_key=os.getenv('CELLAR_ADDON_KEY_SECRET'),
                host=os.getenv('CELLAR_ADDON_HOST'),
                calling_format=OrdinaryCallingFormat())
            self.__bucket = conn.get_bucket(config.get('database', 'bucket'))
        return self.__bucket

    def get(self, id, prefix=''):
        key = self.bucket.get_key(name(id, prefix))
        return key.get_contents_as_string()

    def size(self, id, prefix=''):
        key = self.bucket.get_key(name(id, prefix))
        return key.size

    def set(self, data, prefix=''):
        id = uuid.uuid4().hex
        key = Key(self.bucket, name(id, prefix))
        key.set_contents_from_string(data)
        return id


def name(id, prefix=''):
    return '/'.join(filter(None, [prefix, id]))
