import unittest
from gcp_cis import gcp_client


class MyTestCase(unittest.TestCase):
    def test_authentication(self):
        sa = {}
        pid = ''

        try:
            client = gcp_client(service_account_info=sa, project_id=pid)
            status = True
        except Exception as e:
            status = False

        self.assertEqual(status, True)  # add assertion here

    def test_get_project_number(self):
        sa = {}
        pid = ''

        client = gcp_client(service_account_info=sa, project_id=pid)
        project_number = client.get_project_number()

        self.assertEqual('509676931471', project_number)


if __name__ == '__main__':
    unittest.main()
