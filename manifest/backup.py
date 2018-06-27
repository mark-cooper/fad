import boto3
import datetime
import json
import logging
import os

CLIENT = boto3.client('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    backup = False
    backup_status = 'fail'
    table = os.getenv('FAD_TABLE_NAME')

    try:
        backup = create_backup(table)
        backup_status = 'ok'
    except Exception as e:
        logger.error("Failed backup for {table}.\n. Error: {err}".format(
            table=table, err=str(e)))

    status = {
        'backup': backup,
        'message': backup_status,
    }
    logger.info(json.dumps(status))

    return status


def create_backup(table):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup = table + "_" + timestamp
    CLIENT.create_backup(
        TableName=table,
        BackupName=backup
    )
    return backup


if __name__ == '__main__':
    handler('', '')
