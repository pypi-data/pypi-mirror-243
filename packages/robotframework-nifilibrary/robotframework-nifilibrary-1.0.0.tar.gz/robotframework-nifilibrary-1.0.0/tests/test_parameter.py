from NifiLibrary.NifiLibrary import NifiLibrary
import unittest
from unittest.mock import MagicMock
import requests


class NifiParameterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.nifi = NifiLibrary()
        self.base_url = "https://localhost:8443"
        self.username = "test"
        self.password = "test"
        self.verify = False
        self.processor_group_id = "Af0110f6c-ba7f-3ac0-00fc-677aa1a4054c"
        self.processor_group_name = "A_group"
        self.token = "1234"
        self.param_context_id = "f0110f6c-ba7f-3ac0-00fc-677aa1a4054c"
        self.param_context_name = "test_param_context"
        self.parameter_name = "name"
        self.parameter_value = "Mr.AAA"
        self.id = "f0110f6c-ba9f-3ac3-00fc-577aa1a4054c"

    def test_update_process_group_parameter_context_success(self):
        # Arrange
        expected_put_result = MagicMock()
        expected_put_result.json.return_value = {"revision": {"version": 35}, "id": self.id}
        data = {
            "revision": {"clientId": self.param_context_id, "version": 35},
            "component": {"id": self.processor_group_id, "name": self.processor_group_name,
                          "parameterContext": {"id": self.param_context_id,
                                               "component": {
                                                   "id": self.param_context_id,
                                                   "name": self.param_context_name}}}}

        expected_get_result = {"revision": {"version": 35}, "id": "f0110f6c-ba9f-3ac3-00fc-577aa1a4054c"}
        requests.get = MagicMock(status_code=200, return_value=expected_get_result)
        requests.put = MagicMock(status_code=200, return_value=expected_put_result)

        # Act
        result = self.nifi.update_process_group_parameter_context(self.base_url, self.token, self.processor_group_id,
                                                                  self.processor_group_name,
                                                                  self.param_context_id,
                                                                  self.param_context_name,
                                                                  self.verify)
        #Assert
        self.assertEqual(result, expected_put_result)
        requests.put.assert_called_once_with(
            f"{self.base_url}/nifi-api/process-groups/{self.processor_group_id}",
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {self.token}'},
            json=data,
            verify=self.verify
        )
        requests.put = MagicMock()

    def test_update_process_group_parameter_context_when_base_url_is_none(self):
        raised = False
        try:
            self.nifi.update_process_group_parameter_context(None, self.token, self.processor_group_id,
                                                             self.processor_group_name, self.param_context_id,
                                                             self.param_context_name,
                                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_process_group_parameter_context_when_token_is_none(self):
        raised = False
        try:
            self.nifi.update_process_group_parameter_context(self.base_url, None, self.processor_group_id,
                                                             self.processor_group_name, self.param_context_id,
                                                             self.param_context_name,
                                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_process_group_parameter_context_when_processor_group_id_is_none(self):
        raised = False
        try:
            self.nifi.update_process_group_parameter_context(self.base_url, self.token, None,
                                                             self.processor_group_name, self.param_context_id,
                                                             self.param_context_name,
                                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_process_group_parameter_context_when_processor_group_name_is_none(self):
        raised = False
        try:
            self.nifi.update_process_group_parameter_context(self.base_url, self.token, self.processor_group_id,
                                                             None, self.param_context_id,
                                                             self.param_context_name,
                                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_process_group_parameter_context_when_param_context_id_is_none(self):
        raised = False
        try:
            self.nifi.update_process_group_parameter_context(self.base_url, self.token, self.processor_group_id,
                                                             self.processor_group_name, None,
                                                             self.param_context_name,
                                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_process_group_parameter_context_when_param_context_name_is_none(self):
        raised = False
        try:
            self.nifi.update_process_group_parameter_context(self.base_url, self.token, self.processor_group_id,
                                                             self.processor_group_name, self.param_context_id,
                                                             None,
                                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_process_group_parameter_context_when_verify_is_none(self):
        raised = False
        try:
            self.nifi.update_process_group_parameter_context(self.base_url, self.token, self.processor_group_id,
                                                             self.processor_group_name,
                                                             self.param_context_id,
                                                             self.param_context_name,
                                                             self.verify)
        except:
            raised = True
        self.assertFalse(raised)

    def test_update_process_group_parameter_context_exception(self):
        # Arrange
        mock_request_exception = MagicMock()
        expected_get_result = {"revision": {"version": 35}, "id": "f0110f6c-ba9f-3ac3-00fc-577aa1a4054c"}
        requests.get = MagicMock(status_code=200, return_value=expected_get_result)

        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        original_put = requests.put
        requests.put = mock_request_exception
        # Act
        try:
            self.nifi.update_process_group_parameter_context(self.base_url, self.token, self.processor_group_id,
                                                             self.processor_group_name,
                                                             self.param_context_id,
                                                             self.param_context_name,
                                                             self.verify)
            raised = True
        except Exception as ex:
            # Here, ex will be the simulated RequestException
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            # Restore the original requests.put
            requests.put = original_put
        # Assert
        self.assertFalse(raised)

    def test_get_parameter_contexts_success(self):
        # Arrange
        expected_get_result = {"revision": {"version": 35}, "id": "f0110f6c-ba9f-3ac3-00fc-577aa1a4054c"}
        requests.get = MagicMock(status_code=200, return_value=expected_get_result)

        # Act
        result = self.nifi.get_parameter_contexts(self.base_url, self.token,
                                                  self.param_context_id,
                                                  self.verify)
        # Assert
        self.assertEqual(result, expected_get_result)
        requests.get.assert_called_once_with(f"{self.base_url}/nifi-api/parameter-contexts/{self.param_context_id}",
                                             headers={'Content-Type': 'application/json',
                                                      'Authorization': f'Bearer {self.token}'},
                                             verify=self.verify)
        requests.get = MagicMock()

    def test_get_parameter_contexts_when_base_url_is_none(self):
        raised = False
        try:
            self.nifi.get_parameter_contexts(None, self.token,
                                             self.param_context_id,
                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_parameter_contexts_when_token_is_none(self):
        raised = False
        try:
            self.nifi.get_parameter_contexts(self.base_url, None,
                                             self.param_context_id,
                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_parameter_contexts_when_param_context_id_is_None(self):
        raised = False
        try:
            self.nifi.get_parameter_contexts(self.base_url, self.token,
                                             None,
                                             self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_parameter_contexts_when_verify_is_none(self):
        raised = False
        try:
            self.nifi.get_parameter_contexts(self.base_url, self.token,
                                             self.param_context_id,
                                             None)
        except:
            raised = True
        self.assertFalse(raised)

    def test_stop_process_group_exception(self):
        # Arrange
        mock_request_exception = MagicMock()
        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        original_get = requests.get
        requests.get = mock_request_exception
        # Act
        try:
            self.nifi.get_parameter_contexts(self.base_url, self.token,
                                             self.param_context_id,
                                             self.verify)
            raised = True
        except Exception as ex:
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            requests.put = original_get
        self.assertFalse(raised)

    def test_update_parameter_value_success(self):
        # Arrange
        expected_get_result = MagicMock()
        expected_put_result = MagicMock()
        expected_get_result.json.return_value = {"revision": {"version": 35},
                                                 "id": self.id,
                                                 "component": {"id": self.param_context_id}}
        expected_put_result.json.return_value = {"revision": {"version": 35},
                                                 "id": self.param_context_id}
        expected_response = {"revision": {"version": 35},
                             "id": self.param_context_id}
        param = [{"parameter": {"name": self.parameter_name, "value": self.parameter_value}}]
        data = {"id": self.id,
                "revision": {"version": 35}, "component": {"id": self.param_context_id, "parameters": param}}

        requests.get = MagicMock(status_code=200, return_value=expected_get_result)
        requests.put = MagicMock(status_code=200, return_value=expected_put_result)
        # Act
        result = self.nifi.update_parameter_value(self.base_url, self.token, self.param_context_id, self.parameter_name,
                                                  self.parameter_value, self.verify)
        # Assert
        self.assertEqual(result.json(), expected_response)
        requests.put.assert_called_once_with(f"{self.base_url}/nifi-api/parameter-contexts/{self.param_context_id}",
                                             headers={'Content-Type': 'application/json',
                                                      'Authorization': f'Bearer {self.token}'},
                                             json=data,
                                             verify=self.verify)
        requests.put = MagicMock()
        requests.get = MagicMock()

    def test_update_parameter_value_when_base_url_is_none(self):
        raised = False
        try:
            self.nifi.update_parameter_value(None, self.token, self.param_context_id,
                                             self.parameter_name,
                                             self.parameter_value, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_parameter_value_when_token_is_none(self):
        raised = False
        try:
            self.nifi.update_parameter_value(self.base_url, None, self.param_context_id,
                                             self.parameter_name,
                                             self.parameter_value, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_parameter_value_when_param_context_id_is_None(self):
        raised = False
        try:
            self.nifi.update_parameter_value(self.base_url, self.token, None,
                                             self.parameter_name,
                                             self.parameter_value, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_parameter_value_when_parameter_name_is_none(self):
        raised = False
        try:
            self.nifi.update_parameter_value(self.base_url, self.token, self.param_context_id,
                                             None,
                                             self.parameter_value, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_parameter_value_when_parameter_value_is_none(self):
        raised = False
        try:
            self.nifi.update_parameter_value(self.base_url, self.token, self.param_context_id,
                                             self.parameter_name,
                                             None, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_update_parameter_value_when_verify_is_none(self):
        raised = False
        expected_get_result = MagicMock()
        expected_put_result = MagicMock()
        expected_get_result.json.return_value = {"revision": {"version": 35},
                                                 "id": self.id,
                                                 "component": {"id": self.param_context_id}}
        expected_put_result.json.return_value = {"revision": {"version": 35},
                                                 "id": self.param_context_id}
        requests.get = MagicMock(status_code=200, return_value=expected_get_result)
        requests.put = MagicMock(status_code=200, return_value=expected_put_result)
        try:
            self.nifi.update_parameter_value(self.base_url, self.token, self.param_context_id,
                                             self.parameter_name,
                                             self.parameter_value, None)
        except:
            raised = True

        self.assertFalse(raised)

    def test_update_parameter_value_exception(self):
        # Arrange
        expected_get_result = MagicMock()
        expected_get_result.json.return_value = {"revision": {"version": 35},
                                                 "id": self.id,
                                                 "component": {"id": self.param_context_id}}
        requests.get = MagicMock(status_code=200, return_value=expected_get_result)
        mock_request_exception = MagicMock()
        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        original_put = requests.put
        requests.put = mock_request_exception
        # Act
        try:
            self.nifi.update_parameter_value(self.base_url, self.token, self.param_context_id, self.parameter_name,
                                             self.parameter_value, self.verify)
            raised = True
        except Exception as ex:
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            requests.put = original_put
        self.assertFalse(raised)

    if __name__ == '__main__':
        unittest.main()
