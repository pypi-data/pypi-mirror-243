Tryton FileStore Cellar
=======================

Cellar Storage Service for the Tryton application framework.

To use Cellar Storage Service, the trytond configuration must be modify to set
in the `database` section, the `class`  to
`tryton_filestorage_cellar.FileStoreCellar` and the `bucket` to the name of
your bucket.
Here is an example the section::

    [database]
    class = tryton_filestorage_cellar.FileStoreCellar
    bucket = bucket-id-here

The authentication must be set using environment variable as explained in the
`Cellar, a S3-like object storage service
<https://www.clever-cloud.com/doc/deploy/addon/cellar/>`_.
