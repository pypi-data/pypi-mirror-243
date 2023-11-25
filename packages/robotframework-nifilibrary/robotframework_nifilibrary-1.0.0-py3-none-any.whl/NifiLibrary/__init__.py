from .NifiLibrary import NifiLibrary
from .version import VERSION

__version__ = VERSION

__author__ = 'Weeraporn.pai'
__email__ = 'poopae1322@gmail.com'

class NifiLibrary(NifiLibrary):
    """NifiLibrary is a robotframework library for calling jenkins api

    == Example Test Cases ==
    | *** Settings ***       |
    | Library                | NifiLibrary   |
    |                        |
    | *** Test Cases ***     |
    | create nifi session | ${protocol}      | ${host}          | ${username}      | ${password}      | ${verify} |
    | ${job_details}=        | Get Jenkins Job  | ${job_full_name} |
    | ${job_build_details}=  | Get Jenkins Job Build | ${job_full_name} | ${build_number}  |
    | ${build_number}=       | Build Jenkins With Parameters | ${job_full_name} | ${parameters_string} |
    | ${job_build_details}=  | Build Jenkins With Parameters And Wait Until Job Done | ${job_full_name} | ${parameters_string} | 10 | 2 |

    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
    ROBOT_LIBRARY_VERSION = VERSION
