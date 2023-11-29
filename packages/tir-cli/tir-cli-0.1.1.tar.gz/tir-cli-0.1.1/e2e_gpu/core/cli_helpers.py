import json
import sys as __sys
import traceback
from types import SimpleNamespace

from e2e_gpu.core.constants import (ERROR_MSG, PACKAGE_INFO, PACKAGE_VERSION,
                                    RESERVES)


# =========================
# e2e pkg/ver-info functions
# =========================
def e2e_version_info():
    print(PACKAGE_VERSION)


def e2e_pakage_info():
    print(PACKAGE_INFO)


# =========================
# get/display/format output
# =========================
def get_output(obj):  # add output types
    if not obj:
        return
    if isinstance(obj, list):
        print_array(obj)
    else:
        print_json_output(obj)


def print_array(array):  # add output types
    for element in array:
        print_json_output(element)


def print_json_output(obj):
    obj = vars(obj)
    covert_namespace_to_json(obj)
    print(json.dumps(obj, sort_keys=True, indent=4))


def covert_namespace_to_json(my_obj):
    for key in my_obj:
        if type(my_obj[key]) == SimpleNamespace:
            my_obj[key] = vars(my_obj[key])
            covert_namespace_to_json(my_obj[key])


# =========================
# commands and error
# =========================
def manage_exception(e, arguments):
    trace = traceback.format_exc()
    if arguments.debug:
        print([arguments, e, trace], sep='\n')
    exit_process(ERROR_MSG)


def exit_process(error=None):
    __sys.exit(error)
