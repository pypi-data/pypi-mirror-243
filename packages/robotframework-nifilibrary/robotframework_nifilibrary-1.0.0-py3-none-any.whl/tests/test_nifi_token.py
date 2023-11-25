from NifiLibrary.NifiLibrary import NifiLibrary
import unittest
from unittest.mock import MagicMock
import requests


class NifiTokenTest(unittest.TestCase):

    def setUp(self) -> None:
        self.nifi = NifiLibrary()
        self.mock_response = MagicMock()
        self.base_url = "https://localhost:8443"
        self.username = "test"
        self.password = "test"
        self.verify = False

    def test_get_nifi_token_success(self):
        # Arrange
        expected_result = "#123456#"
        self.mock_response = expected_result
        requests.post = MagicMock(return_value=self.mock_response)
        # Act
        result = self.nifi.get_nifi_token(self.base_url, self.username, self.password, self.verify)
        # Assert
        try:
            self.assertEqual(result, expected_result)
            requests.post.assert_called_once_with(
                f"{self.base_url}/nifi-api/access/token",
                headers=self.nifi.headers,
                data={'username': self.username, 'password': self.password},
                verify=self.verify
            )
            raised = True
        except Exception as ex:
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            # Restore the original requests.post
            requests.post = MagicMock()
        self.assertTrue(raised)

    def test_nifi_token_when_url_is_none(self):
        raised = False
        try:
            self.nifi.get_nifi_token(None, self.username, self.password, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_nifi_token_when_username_is_none(self):
        raised = False
        try:
            self.nifi.get_nifi_token(self.base_url, None, self.password, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_nifi_token_when_password_is_none(self):
        raised = False
        try:
            self.nifi.get_nifi_token(self.base_url, self.username, None, self.verify)
        except:
            raised = True
        self.assertTrue(raised)

    def test_nifi_token_when_verify_is_none(self):
        raised = False
        try:
            self.nifi.get_nifi_token(self.base_url, self.password, self.password, None)
        except:
            raised = True
        self.assertFalse(raised)

    def test_get_nifi_token_exception(self):
        # Arrange
        mock_request_exception = MagicMock()
        # Set the side effect to simulate an Exception
        mock_request_exception.side_effect = Exception("Error making API request: Simulated error")
        # Replace requests.post with the MagicMock instance
        original_post = requests.post
        requests.post = mock_request_exception

        try:
            result = self.nifi.get_nifi_token(self.base_url, self.username, self.password, self.verify)
            raised = True
        except Exception as ex:
            # Here, ex will be the simulated RequestException
            self.assertEqual(str(ex), "Error making API request: Simulated error")
            raised = False
        finally:
            # Restore the original requests.post
            requests.post = original_post
        self.assertFalse(raised)

    if __name__ == '__main__':
        unittest.main()
