# NifiLibrary
`NifiLibrary` is a [Robot Framework](http://www.robotframework.org) test library which provides keywords to work with Apache Nifi api

# Usage
Install `robotframework-nifilibrary` via `pip` command

```bash
pip install -U robotframework-nifilibrary
```

# Example Test Case
| *** Settings ***      |                                  |                       |             |                              |                                         |                     |
|-----------------------|----------------------------------|-----------------------|-------------|------------------------------|-----------------------------------------|---------------------|
| Library               | NifiLibrary                      |                       |             |                              |                                         |                     |
| *** Test Cases ***    |                                  |                       |             |                              |                                         |                     |
| Rename File - Success |                                  |                       |             |                              |                                         |                     |
|                       | ${token}                         | Get Nifi Token        | ${base_url} | ${username}                  | ${password}                             |                     |
|                       | Stop Process Group               | ${base_url}           | ${token}    | ${rename_processor_group_id} |                                         |
|                       | Update Parameter Value           | ${base_url}           | ${token}    | ${parameter_context_id}      | ${file_filter_param}                    | ${file_filter_name} |
|                       | Start Processor                  | {base_url}            | ${token}    | ${get_file_processor_id}     |                                         |                     |
|                       | Stop Processor                   | {base_url}            | ${token}    | ${get_file_processor_id}     |                                         |                     |
|                       | List Directory                   | ${local_folder_path}/ |             |                              |                                         |                     |
|                       | Wait Until Keyword Succeeds      | 3x                    | 5s          | File Should Exist            | ${local_folder_path}/${file_name_value} |                     |

# Documentation