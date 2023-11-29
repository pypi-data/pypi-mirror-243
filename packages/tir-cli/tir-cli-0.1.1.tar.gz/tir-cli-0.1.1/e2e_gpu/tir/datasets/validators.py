
def _creation_is_valid(arguments):
    try:
        if arguments.name:
            return True
        return False
    except:
        return False


def _delete_get_request_is_valid(arguments):
    try:
        if arguments.dataset_id:
            return True
        return False
    except:
        return False


def _download_is_valid(arguments):
    try:
        if arguments.dataset_id and arguments.local_path:
            return True
        return False
    except:
        return False


def _upload_is_valid(arguments):
    try:
        if arguments.dataset_id and arguments.dataset_path:
            return True
        return False
    except:
        return False
