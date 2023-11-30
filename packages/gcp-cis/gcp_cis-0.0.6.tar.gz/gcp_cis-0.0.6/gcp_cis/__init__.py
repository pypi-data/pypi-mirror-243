__author__ = 'Klera DevOps'
__version__ = '0.0.6'

import json

from google.cloud import compute_v1
from google.oauth2 import service_account
from google.cloud import resourcemanager_v3
from gcp_cis.gcp_cis_checks_iam import iam_controls
from gcp_cis.gcp_cis_checks_logging_and_monitoring import logging_monitoring_controls
from gcp_cis.gcp_cis_checks_networking import networking_controls
from gcp_cis.gcp_cis_checks_storage import storage_controls
from gcp_cis.gcp_cis_checks_vms import vms_controls


class gcp_client(iam_controls, logging_monitoring_controls, networking_controls, storage_controls, vms_controls):
    def __init__(self, org_id=None, **kwargs):
        """
        :param service_account_path:
        :param org_id:
        """
        self.scopes = ['https://www.googleapis.com/auth/cloud-platform']
        if 'service_account_path' in kwargs.keys():
            self.credentials = service_account.Credentials.from_service_account_file(
                kwargs['service_account_path'], scopes=self.scopes
            )
        elif 'service_account_info' in kwargs.keys():
            self.credentials = service_account.Credentials.from_service_account_info(
                kwargs['service_account_info'], scopes=self.scopes
            )
        self.organization_id = org_id

        # sa_file = open(service_account_path)
        # sa = json.load(sa_file)

        self.project_id = kwargs['project_id']

        region_client = compute_v1.RegionsClient(credentials=self.credentials)
        region_list = region_client.list(project=self.project_id)
        self.locations = [region.name for region in region_list]

        project_number = self.get_project_number()

        super().__init__(self.scopes, self.credentials, self.organization_id,
                         self.project_id, self.locations, project_number)

    def getCompliance(self) -> list:
        """
        :return: list of GCP CIS Benchmarks
        """
        compliance_data = []

        compliance_data.extend(self.get_iam_compliance())
        compliance_data.extend(self.get_logging_monitoring_compliance())
        compliance_data.extend(self.get_networking_compliance())
        compliance_data.extend(self.get_vms_compliance())
        compliance_data.extend(self.get_storage_compliance())

        return compliance_data

    # returns the project number associated with GCP project id
    def get_project_number(self) -> str:
        """
        :return: project number associated with GCP project id
        """
        client = resourcemanager_v3.ProjectsClient(credentials=self.credentials)
        # Initialize request argument(s)
        request = resourcemanager_v3.SearchProjectsRequest(query=f"id:{self.project_id}")

        # # Make the request
        page_result = client.search_projects(request=request)
        # # Handle the response
        for response in page_result:
            if response.project_id == self.project_id:
                project = response.name
                return project.replace('projects/', '')

