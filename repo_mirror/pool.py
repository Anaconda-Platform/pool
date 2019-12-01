
from boto3.s3 import transfer


import boto3
import logging


_logger = logging.getLogger(__name__)


def upload_files(aws_bucket, all_tarballs, monthly_directory):
    upload_config = transfer.TransferConfig(
        max_concurrency=10,
        use_threads=True
    )
    s3 = boto3.client('s3')
    #monthly_directory = time.strftime("%Y_%m")
    for file_name in all_tarballs:
        print(f'Uploading {file_name} to S3')
        s3.upload_file(
            file_name,
            aws_bucket,
            f'{monthly_directory}/{file_name}',
            ExtraArgs={'ACL': 'public-read'},
            Config=upload_config
        )
        _logger.info(f'uploaded {file_name} to {aws_bucket}')
