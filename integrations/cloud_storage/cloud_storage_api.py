import cloudstorage as gcs


def create_file(file_data, filename, content_type, tenant_code):
    """Create a file.

    The retry_params specified in the open call will override the default
    retry params for this particular file handle.

    Args:
      filename: filename.
    """
    existing_file = read_file(tenant_code, filename)
    # we don't want to overwrite an existing file
    if not existing_file:
        final_filepath = "/" + tenant_code + "/" + filename

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(final_filepath,
                            'w',
                            content_type=content_type,
                            retry_params=write_retry_params)
        gcs_file.write(file_data)
        gcs_file.close()
        return final_filepath
    else:
        raise ValueError("This filename already exists in this tenant")

def read_file(tenant_code, filename):
    final_filepath = "/" + tenant_code + "/" + filename
    try:
        gcs_file = gcs.open(final_filepath)
    except gcs.NotFoundError:
        return None
    return gcs_file

def read_bucket(tenant_code):
    objects_in_bucket =  gcs.listbucket(tenant_code, marker=None, max_keys=None, delimiter=None, retry_params=None)
    convereted_objects_in_bucket = [e for e in objects_in_bucket]
    return convereted_objects_in_bucket
