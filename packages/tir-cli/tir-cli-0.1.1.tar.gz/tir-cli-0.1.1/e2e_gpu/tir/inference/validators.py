
def _creation_is_valid(arguments):
    try:
        if arguments.name and arguments.plan_name and arguments.image_id:
            return True
        return False
    except:
        return False

def _notebook_id_exists(arguments):
    try:
        if arguments.notebook_id :
            return True
        return False
    except:
        return False


def _upgrade_request_is_valid(arguments):
    try:
        if _notebook_id_exists(arguments) and arguments.disk_size:
            return True
        return False
    except:
        return False

