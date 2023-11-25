from NifiLibrary.NifiLibrary import NifiLibrary
import unittest
from unittest.mock import MagicMock, patch
import requests


class NifiProcessGroupTest(unittest.TestCase):

    def setUp(self) -> None:
        self.nifi = NifiLibrary()
        self.base_url = "https://localhost:8443"
        self.username = "test"
        self.password = "test"
        self.verify = False
        self.processor_group_id = "Af0110f6c-ba7f-3ac0-00fc-677aa1a4054c"
        self.token = "1234"

    def test_start_process_group_success(self):
        # Arrange
        self.mock_response = MagicMock()
        expected_result = {"revision": {"version": 35}, "id": self.processor_group_id}
        requests.put = MagicMock(status_code=200, return_value=expected_result)
        # Act
        result = self.nifi.start_process_group(self.base_url, self.token, self.processor_group_id,
                                               self.verify)
        # Assert
        self.assertEqual(result, expected_result)
        requests.put.assert_called_once_with(f'{self.base_url}/nifi-api/flow/process-groups/{self.processor_group_id}',
                                             data={'id': self.processor_group_id, 'state': 'RUNNING'},
                                             headers={'Content-Type': 'application/json',
                                                      'Authorization': f'Bearer {self.token}'}, verify=False)

    def test_start_process_group_when_base_url_is_none(self):
        raised = False
        try:
            self.nifi.start_process_group(None, self.token, self.processor_group_id,
                                          self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_start_process_group_when_token_is_none(self):
        raised = False
        try:
            self.nifi.start_process_group(self.base_url, None, self.processor_group_id,
                                          self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_start_process_group_when_processor_group_id_is_none(self):
        raised = False
        try:
            self.nifi.start_process_group(self.base_url, self.token, None,
                                          self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_start_process_group_when_verify_is_none(self):
        raised = False
        try:
            self.nifi.start_process_group(self.base_url, self.token, self.processor_group_id,
                                          self.verify)
        except:
            raised = True
        self.assertFalse(raised)

    def test_start_process_group_exception(self):
        # Arrange
        mock_request_exception = MagicMock()
        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        original_put = requests.put
        requests.put = mock_request_exception
        # Act
        try:
            self.nifi.start_process_group(self.base_url, self.token, self.processor_group_id,
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

    def test_stop_process_group_success(self):
        # Arrange
        expected_result = {"revision": {"version": 35}, "id": "f0110f6c-ba9f-3ac3-00fc-577aa1a4054c"}
        requests.put = MagicMock(status_code=200, return_value=expected_result)
        # Act
        print("######1#####")
        result = self.nifi.stop_process_group(self.base_url, self.token, self.processor_group_id,
                                              self.verify)
        print("######result#####")
        print(result)
        # Assert
        self.assertEqual(result, expected_result)
        requests.put.assert_called_once_with(f'{self.base_url}/nifi-api/flow/process-groups/{self.processor_group_id}',
                                             data={'id': self.processor_group_id, 'state': 'STOPPED'},
                                             headers={'Content-Type': 'application/json',
                                                      'Authorization': f'Bearer {self.token}'}, verify=False)

    def test_stop_process_group_when_base_url_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(None, self.token, self.processor_group_id,
                                         self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_stop_process_group_when_token_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(self.base_url, None, self.processor_group_id,
                                         self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_stop_process_group_when_processor_group_id_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(self.base_url, self.token, None,
                                         self.verify)
        except:
            raised = True
        self.assertFalse(raised)

    def test_stop_process_group_when_verify_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(self.base_url, self.token, self.processor_group_id,
                                         None)
        except:
            raised = True
        self.assertFalse(raised)

    def test_stop_process_group_exception(self):
        # Arrange
        mock_request_exception = MagicMock()
        # Set the side effect to simulate an Exception
        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        # Replace requests.post with the MagicMock instance
        original_put = requests.put
        requests.put = mock_request_exception

        try:
            self.nifi.stop_process_group(self.base_url, self.token, self.processor_group_id,
                                         self.verify)
            raised = True
        except Exception as ex:
            # Here, ex will be the simulated RequestException
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            # Restore the original requests.put
            requests.put = original_put
        self.assertFalse(raised)

    def test_get_process_group_success(self):
        # Arrange
        expected_result = {"revision": {"version": 35}, "id": self.processor_group_id}
        self.mock_response = expected_result
        requests.get = MagicMock(return_value=self.mock_response)

        # Act
        result = self.nifi.get_process_group(self.base_url, self.token, self.processor_group_id,
                                             self.verify)
        # Assert
        self.assertEqual(result, expected_result)
        requests.get.assert_called_once_with(
            f"{self.base_url}/nifi-api/process-groups/{self.processor_group_id}",
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {self.token}'},
            verify=self.verify
        )
        requests.get = MagicMock()

    def test_get_process_group_when_base_url_is_none(self):
        raised = False
        try:
            self.nifi.get_process_group(None, self.token, self.processor_group_id,
                                        self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_process_group_when_token_is_none(self):
        raised = False
        try:
            self.nifi.get_process_group(self.base_url, None, self.processor_group_id,
                                        self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_process_group_when_processor_group_id_is_none(self):
        raised = False
        try:
            self.nifi.get_process_group(self.base_url, self.token, None,
                                        self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_get_process_group_when_verify_is_none(self):
        raised = False
        try:
            self.nifi.get_process_group(self.base_url, self.token, self.processor_group_id,
                                        None)
        except:
            raised = True
        self.assertFalse(raised)

    def test_get_process_group_exception(self):
        # Arrange
        mock_request_exception = MagicMock()
        # Set the side effect to simulate an Exception
        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        # Replace requests.post with the MagicMock instance
        original_get = requests.get
        requests.get = mock_request_exception

        try:
            self.nifi.get_process_group(self.base_url, self.token, self.processor_group_id,
                                        self.verify)
            raised = True
        except Exception as ex:
            # Here, ex will be the simulated RequestException
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            # Restore the original requests.get
            requests.get = original_get
        self.assertFalse(raised)

    def test_stop_process_group_success(self):
        # Arrange
        expected_result = {"revision": {"version": 35}, "id": "f0110f6c-ba9f-3ac3-00fc-577aa1a4054c"}
        requests.put = MagicMock(status_code=200, return_value=expected_result)
        # Act
        result = self.nifi.stop_process_group(self.base_url, self.token, self.processor_group_id,
                                              self.verify)
        # Assert
        self.assertEqual(result, expected_result)
        requests.put.assert_called_once_with(f'{self.base_url}/nifi-api/flow/process-groups/{self.processor_group_id}',
                                             data={'id': self.processor_group_id, 'state': 'STOPPED'},
                                             headers={'Content-Type': 'application/json',
                                                      'Authorization': f'Bearer {self.token}'}, verify=False)

    def test_stop_process_group_when_base_url_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(None, self.token, self.processor_group_id,
                                         self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_stop_process_group_when_token_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(self.base_url, None, self.processor_group_id,
                                         self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_stop_process_group_when_processor_group_id_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(self.base_url, self.token, None,
                                         self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_stop_process_group_when_verify_is_none(self):
        raised = False
        try:
            self.nifi.stop_process_group(self.base_url, self.token, self.processor_group_id,
                                         self.verify)
        except:
            raised = True
        self.assertFalse(raised)

    def test_stop_process_group_exception(self):
        # Arrange
        mock_request_exception = MagicMock()
        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        original_put = requests.put
        requests.put = mock_request_exception
        # Act
        try:
            self.nifi.stop_process_group(self.base_url, self.token, self.processor_group_id,
                                         self.verify)
            raised = True
        except Exception as ex:
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            requests.put = original_put
        self.assertFalse(raised)

    if __name__ == '__main__':
        unittest.main()
