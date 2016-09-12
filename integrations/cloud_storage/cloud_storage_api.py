import cloudstorage as gcs


def create_file(file_data, filename):
    """Create a file.

    The retry_params specified in the open call will override the default
    retry params for this particular file handle.

    Args:
      filename: filename.
    """

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        retry_params=write_retry_params)
    gcs_file.write('abcde\n')
    gcs_file.write('f' * 1024 * 4 + '\n')
    gcs_file.close()
