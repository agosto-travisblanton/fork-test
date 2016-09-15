import cloudstorage as gcs
from google.appengine.api import app_identity as identity
from utils.url_sign import sign_cloud_storage_url

default_bucket = "/" + identity.get_default_gcs_bucket_name()


def create_file(file_data, filename, content_type, tenant_code):
    existing_file = read_file(tenant_code, filename)
    # we don't want to overwrite an existing file
    if not existing_file:
        final_filepath = default_bucket + "/" + tenant_code + "/" + filename

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(final_filepath,
                            'w',
                            content_type=content_type,
                            retry_params=write_retry_params)
        gcs_file.write(file_data)
        gcs_file.close()
        # signed cloud storage url with no expiry
        return sign_cloud_storage_url(final_filepath)
    else:
        raise ValueError("This filename already exists in this tenant")


def read_file(tenant_code, filename):
    final_filepath = default_bucket + "/" + tenant_code + "/" + filename
    try:
        gcs_file = gcs.open(final_filepath)
    except gcs.NotFoundError:
        return None
    return gcs_file


def read_bucket(tenant_code):
    final_filepath = default_bucket + "/" + tenant_code
    objects_in_bucket = gcs.listbucket(final_filepath, marker=None, max_keys=None, delimiter=None,
                                       retry_params=None)
    convereted_objects_in_bucket = [e for e in objects_in_bucket]
    return convereted_objects_in_bucket


def delete_file(filepath):
    final_filepath = default_bucket + "/" + filepath
    if final_filepath:
        try:
            gcs.delete(final_filepath)
            return True
        except gcs.errors.NotFoundError:
            return True
    return False
