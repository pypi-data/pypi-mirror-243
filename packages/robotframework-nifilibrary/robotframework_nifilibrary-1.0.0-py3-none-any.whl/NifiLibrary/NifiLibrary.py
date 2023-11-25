from robot.api import logger
from robot.api.deco import keyword
import requests
from .version import VERSION

__version__ = VERSION

class NifiLibrary(object):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def __init__(self):
        self._endpoint = None
        self._accessToken = None

    @keyword('Get Nifi Token')
    def get_nifi_token(self, base_url=None, username=None, password=None, verify=False):
        """ Get NiFi Token

        Arguments:
            - base_url: NiFi domain
            - username: NiFi username to login
            - password: NiFi password to login

        Examples:
        | Get Nifi Token |  https://localhost:8443 | username | password |

        """
        if not base_url or not username or not password:
            raise Exception('Require parameters cannot not be none')
        self._endpoint = f"{base_url}/nifi-api/access/token"
        data = {'username': username, 'password': password}
        try:
            response = requests.post(self._endpoint,
                                     headers=self.headers,
                                     data=data,
                                     verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Start Process Group')
    def start_process_group(self, base_url, token=None, processor_group_id=None, verify=False):
        """ Start Process Group

        Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_group_id: id of processor group

        Examples:
        | Start Process Group |  https://localhost:8443 |{token} | {processor_group_id} |

        """
        if not token or not base_url or not processor_group_id:
            raise Exception('Require parameters cannot be none')
        try:
            response = self.update_process_group_state(base_url, token, processor_group_id, 'RUNNING', verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Stop Process Group')
    def stop_process_group(self, base_url, token=None, processor_group_id=None, verify=False):
        """ Stop Process Group

        Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_group_id: id of processor group

        Examples:
        | Stop Process Group |  https://localhost:8443 | {token} | {processor_id} |

        """
        if not token or not base_url or not processor_group_id:
            raise Exception('Require parameters cannot be none')
        try:
            response = self.update_process_group_state(base_url, token, processor_group_id, 'STOPPED', verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Get Process Group')
    def get_process_group(self, base_url, token=None, processor_group_id=None, verify=False):
        """ To get process group detail

        Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_group_id: id of processor group

        Examples:
        | Get Process Group |  https://localhost:8443 | {token} | {processor_group_id} |

        """
        if not token or not base_url or not processor_group_id:
            raise Exception('Require parameters cannot be none')
        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        try:
            self._endpoint = f"{base_url}/nifi-api/process-groups/{processor_group_id}"
            response = requests.get(self._endpoint,
                                    headers=self.headers,
                                    verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Update Process Group Parameter Context')
    def update_process_group_parameter_context(self, base_url, token=None, processor_group_id=None, processor_name=None,
                                               param_context_id=None,
                                               param_context_name=None,
                                               verify=False):
        """ To update parameter context of process group

        Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_group_id: id of processor group
            - processor_name: The default is None
            - param_context_id: id of parameter context
            - param_context_name: name of parameter context

        Examples: | Update Process Group Parameter Context |  https://localhost:8443 | {token} | {processor_group_id}
        | {processor_name} | {param_context_id} | {param_context_name}

        """
        if not token or not base_url or not processor_group_id or not processor_name or not param_context_id or not param_context_name:
            raise Exception('Require parameters cannot be none')

        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        processor_group_detail = self.get_process_group(base_url, token, processor_group_id)
        data = {
            "revision": {"clientId": param_context_id, "version": int(processor_group_detail['revision']['version'])},
            "component": {"id": processor_group_id, "name": processor_name, "parameterContext": {"id": param_context_id,
                                                                                                 "component": {
                                                                                                     "id": param_context_id,
                                                                                                     "name": param_context_name}}}}

        self._endpoint = f"{base_url}/nifi-api/process-groups/{processor_group_id}"
        try:
            response = requests.put(self._endpoint,
                                    headers=self.headers,
                                    json=data,
                                    verify=verify)
            print("######response#####")
            print(response.json())
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Get Parameter Contexts')
    def get_parameter_contexts(self, base_url, token=None, param_context_id=None, verify=False):
        """
         To get parameter context detail

         Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - param_context_id: parameter context id
            - param_context_name: the default value is none

        Examples:
        | Get Parameter Contexts |  https://localhost:8443 | {token} | {param_context_id}

        """
        if not token or not base_url or not param_context_id:
            raise Exception('Require parameters cannot be none')
        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        self._endpoint = f"{base_url}/nifi-api/parameter-contexts/{param_context_id}"
        try:
            response = requests.get(self._endpoint,
                                    headers=self.headers,
                                    verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Update Parameter Value')
    def update_parameter_value(self, base_url, token=None, param_context_id=None, parameter_name=None,
                               parameter_value=None, verify=False):
        """
         To update parameter value at parameter context

         Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - param_context_id: parameter context id
            - parameter_name: The updated parameter name
            - parameter_value: The updated parameter value

        Examples:
        | Update Parameter Value |  https://localhost:8443 | {token} | {param_context_id} | {parameter_name} | {parameter_value}

        """
        if not token or not base_url or not param_context_id or not parameter_name or not parameter_value:
            raise Exception('Require parameters cannot be none')

        param_response = self.get_parameter_contexts(base_url, token, param_context_id)
        param_response = param_response.json()
        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        self._endpoint = f"{base_url}/nifi-api/parameter-contexts/{param_context_id}"
        param = [{"parameter": {"name": parameter_name, "value": parameter_value}}]
        data = {"id": param_response['id'], "revision": {"version": param_response['revision']['version']},
                "component": {"id": param_response['component']['id'], "parameters": param}}
        try:
            response = requests.put(self._endpoint,
                                    headers=self.headers,
                                    json=data,
                                    verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Get Processor')
    def get_processor(self, base_url, token=None, processor_id=None, verify=False):
        """
         To get processor detail

         Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_id: id of processor

        Examples:
        | Get Processor |  https://localhost:8443 | {token} | {processor_id} |

        """
        if not token or not base_url or not processor_id:
            raise Exception('Require parameters cannot be none')
        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        self._endpoint = f"{base_url}/nifi-api/processors/{processor_id}"
        try:
            response = requests.get(self._endpoint,
                                    headers=self.headers,
                                    verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Stop Processor')
    def stop_processor(self, base_url, token=None, processor_id=None, verify=False):
        """
         To stop processor

         Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_id: id of processor

        Examples:
        | Stop Processor |  https://localhost:8443 | {token} | {processor_id} |
        | Stop Processor |  https://localhost:8443 | {token} | {processor_id} | {name} |

        """
        if not token or not base_url or not processor_id:
            raise Exception('Require parameters cannot be none')
        try:
            response = self.update_process_state(base_url, token, processor_id, "STOPPED", verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Start Processor')
    def start_processor(self, base_url, token=None, processor_id=None, verify=False):
        """
         To start processor

         Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_id: id of processor

        Examples:
        | Start Processor |  https://localhost:8443 | {token} | {processor_id} |

        """
        if not token or not base_url or not processor_id:
            raise Exception('Require parameters cannot be none')
        try:
            response = self.update_process_state(base_url, token, processor_id, "RUNNING", verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Get processor state')
    def get_processor_state(self, base_url, token=None, processor_id=None, verify=False):
        """
         To get state of processor

         Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_id: id of processor

        Examples:
        | Get Processor State |  https://localhost:8443 | {token} | {processor_id} |
        | Get Processor State |  https://localhost:8443 | {token} | {processor_id} | {name} |

        """
        if not token or not base_url or not processor_id:
            raise Exception('Require parameters cannot be none')
        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        self._endpoint = f"{base_url}/nifi-api/processors/{processor_id}/state"
        try:
            response = requests.get(self._endpoint,
                                    headers=self.headers,
                                    verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    @keyword('Clear Processor State')
    def clear_processor_state(self, base_url, token=None, processor_id=None, verify=False):
        """
         To clear state of processor

         Arguments:
            - base_url: NiFi domain
            - token: NiFi token it can be get by using <Get Nifi Token> keywords
            - processor_id: id of processor

        Examples:
        | Clear Processor State |  https://localhost:8443 | {token} | {processor_id} |
        | Clear Processor State |  https://localhost:8443 | {token} | {processor_id} | {name} |

        """
        if not token or not base_url or not processor_id:
            raise Exception('Require parameters cannot be none')
        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        self._endpoint = f"{base_url}/nifi-api/processors/{processor_id}/state/clear-requests"
        try:
            response = requests.post(self._endpoint,
                                     headers=self.headers,
                                     verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    def update_process_group_state(self, base_url, token=None, processor_id=None, state=None, verify=False):

        data = {'id': str(processor_id), 'state': str(state)}
        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        try:
            response = requests.put(f"{base_url}/nifi-api/flow/process-groups/{processor_id}",
                                    json=data,
                                    headers=self.headers,
                                    verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))

    def update_process_state(self, base_url, token=None, processor_id=None, state=None, verify=False):
        processor_res = self.get_processor(base_url, token, processor_id)
        processor_res = processor_res.json()
        print(processor_res)
        data = {"revision": {"clientId": processor_id,
                             "version": processor_res['revision']['version']},
                "component": {"id": processor_res['component']['id'], "state": state}}

        self.headers.update([
            ('Content-Type', 'application/json'),
            ('Authorization', f"Bearer {token}")
        ])
        try:
            response = requests.put(f"{base_url}/nifi-api/processors/{processor_id}",
                                    headers=self.headers,
                                    json=data,
                                    verify=verify)
            return response
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))


