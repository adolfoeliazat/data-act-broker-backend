import logging

from dataactcore.config import CONFIG_BROKER
from dataactvalidator.filestreaming.csvLocalWriter import CsvLocalWriter
from dataactvalidator.filestreaming.csvS3Writer import CsvS3Writer


logger = logging.getLogger(__name__)


def write_csv(file_name, upload_name, is_local, header, body):
    """Derive the relevant location and write a CSV to it.
    :return: the final file name (complete with prefix)"""
    with get_write_csv_writer(file_name, upload_name, is_local, header) as writer:
        for line in body:
            writer.write(line)
        writer.finish_batch()


def write_d_file_csv(sess, agency_code, file_utils, file_name, upload_name, is_local, start, end, file_type):
    headers, columns = [key for key in file_utils.mapping], file_utils.db_columns
    page_size, page_idx = 10000, 0
    with get_write_csv_writer(file_name, upload_name, is_local, headers) as writer:
        # stream to file
        while True:
            page_start = page_size * page_idx
            # rows = file_utils.\
            #     query_data(sess, agency_code, start, end, page_start, (page_size * (page_idx + 1))).all()
            rows = file_utils.\
                temp_query_data(sess, agency_code, start, end, page_start, (page_size * (page_idx + 1))).all()
            if rows is None:
                break

            logger.debug('Writing rows {}-{} to file {} CSV'.format(page_start, page_start+len(rows), file_type))
            for row in rows:
                writer.write([dict(zip(columns, row))[value] for value in columns])

            if len(rows) < page_size:
                break
            page_idx += 1
        writer.finish_batch()


def get_write_csv_writer(file_name, upload_name, is_local, header):
    """Derive the relevant location.
    :return: the writer object"""
    if is_local:
        file_name = CONFIG_BROKER['broker_files'] + file_name
        csv_writer = CsvLocalWriter(file_name, header)
        message = 'Writing file locally...'
    else:
        bucket = CONFIG_BROKER['aws_bucket']
        region = CONFIG_BROKER['aws_region']
        csv_writer = CsvS3Writer(region, bucket, upload_name, header)
        message = 'Writing file to S3...'

    logger.debug(message)

    return csv_writer
