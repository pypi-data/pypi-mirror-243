import datetime

import googleapiclient.discovery
from google.api_core.exceptions import GoogleAPIError
from google.cloud import api_keys_v2
from google.cloud import dataproc_v1
from google.cloud import essential_contacts_v1
from google.cloud import kms_v1
from googleapiclient.discovery import build


class iam_controls:
    def __init__(self, scopes, credentials, organization_id, project_id, locations, project_number):
        self.scopes = scopes
        self.credentials = credentials
        self.organization_id = organization_id
        self.project_id = project_id
        self.locations = locations
        self.project_number = project_number

    def ensure_corporate_login_credentials_are_used(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "1.1"
        description = "Ensure that Corporate Login Credentials are Used (Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def ensure_mfa_enabled_for_all_non_service_account(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "1.2"
        description = "Ensure that Multi-Factor Authentication is 'Enabled' for All Non-Service Accounts"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def ensure_security_key_enforcement_enabled_for_all_admin_account(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "1.3"
        description = "Ensure that Security Key Enforcement is Enabled for All Admin Accounts "
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def ensure_only_gcp_managed_service_keys_for_each_service_account(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.4"
        description = "User managed service accounts should not have user-managed keys"
        scored = True

        try:

            # Build the IAM API client
            service = build("iam", "v1", credentials=self.credentials)

            # List all service accounts in the project
            request = service.projects().serviceAccounts().list(name=f"projects/{self.project_id}")
            response = request.execute()

            for account in response["accounts"]:
                name = 'projects/-/serviceAccounts/' + account["email"]
                # List all service account keys for the account
                request = service.projects().serviceAccounts().keys().list(name=name)
                response = request.execute()
                # print(response)

                # Check if any non-managed keys exist
                for i in response["keys"]:

                    if i["keyType"] != "SYSTEM_MANAGED":
                        result = "Not Compliant"
                        failReason = "User managed keys exists for some service accounts"
                        offenders.append(i['name'])

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def ensure_service_accounts_have_no_admin_privileges(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.5"
        description = "Ensure that Service Accounts has no Admin privileges"
        scored = True

        try:

            service = googleapiclient.discovery.build(
                'cloudresourcemanager', 'v1', credentials=self.credentials)

            response = service.projects().getIamPolicy(resource=self.project_id, body={}).execute()

            for binding in response['bindings']:
                # print(binding)
                if binding['role'].endswith("admin") or binding['role'].endswith("Admin") or \
                        binding['role'] == "roles/editor" or binding['role'] == "roles/owner":
                    for member in binding['members']:
                        # print(member)
                        if member.startswith('serviceAccount:'):
                            result = "Not Compliant"
                            failReason = "Service Account with Admin Privileges exists"
                            offenders.append(member)

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.6 Ensure That IAM Users Are Not Assigned the Service Account User or Service Account Token Creator Roles at
    # Project Level (Automated)
    def ensure_no_service_account_user_or_service_account_token_creator_role_at_project_level(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.6"
        description = "Ensure That IAM Users Are Not Assigned the Service Account User or Service Account Token " \
                      "Creator Roles at Project Level"
        scored = True

        try:

            service = googleapiclient.discovery.build(
                'cloudresourcemanager', 'v1', credentials=self.credentials)

            response = service.projects().getIamPolicy(resource=self.project_id, body={}).execute()

            for binding in response['bindings']:

                if binding['role'] == "roles/iam.serviceAccountUser" or binding['role'] == \
                        "roles/iam.serviceAccountTokenCreator":
                    if binding['members']:
                        result = "Not Compliant"
                        failReason = "IAM users with the Service Account User or Service Account Token Creator Roles " \
                                     "at Project Level exists"
                        offenders.extend(binding['members'])

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def ensure_service_account_keys_rotated_every_90_days(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.7"
        description = "Ensure User-Managed/External Keys for Service Accounts Are Rotated Every 90 Days or Fewer (" \
                      "Automated)"
        scored = True

        try:

            # Build the IAM API client
            service = build("iam", "v1", credentials=self.credentials)

            # List all service accounts in the project
            request = service.projects().serviceAccounts().list(name=f"projects/{self.project_id}")
            response = request.execute()

            for account in response["accounts"]:
                name = 'projects/-/serviceAccounts/' + account["email"]
                # List all service account keys for the account
                request = service.projects().serviceAccounts().keys().list(name=name)
                response_keys = request.execute()
                # print(response)

                for key in response_keys["keys"]:
                    creation_time = datetime.datetime.strptime(key["validAfterTime"], "%Y-%m-%dT%H:%M:%SZ")
                    # print(creation_time)
                    # print(datetime.datetime.now() - creation_time)
                    if (datetime.datetime.now() - creation_time).days >= 90:
                        result = "Not Compliant"
                        failReason = "User managed/System managed keys for service accounts have not been rotated in " \
                                     "90 days"
                        offenders.append(key['name'])

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def ensure_separation_of_duties_while_assigning_service_account_related_roles(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.8"
        description = "Ensure That Separation of Duties Is Enforced While Assigning Service Account Related Roles to " \
                      "Users"
        scored = True

        try:
            service = googleapiclient.discovery.build(
                'cloudresourcemanager', 'v1', credentials=self.credentials)

            response = service.projects().getIamPolicy(resource=self.project_id, body={}).execute()
            serviceAccountAdmin_members = []
            serviceAccountUser_members = []
            for binding in response['bindings']:
                # print(binding)

                if binding['role'] == "roles/iam.serviceAccountAdmin":
                    serviceAccountAdmin_members.extend(binding["members"])

                if binding['role'] == "roles/iam.serviceAccountUser":
                    serviceAccountUser_members.extend(binding["members"])

            for member in serviceAccountAdmin_members:
                if member in serviceAccountUser_members:
                    result = "Not Compliant"
                    failReason = "Users have been assigned with both the roles/iam.serviceAccountAdmin and " \
                                 "roles/iam.serviceAccountUser roles."
                    offenders.append(member)

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.9	Ensure That Cloud KMS Cryptokeys Are Not Anonymously or Publicly Accessible
    def ensure_cloud_kms_cryptokeys_are_not_publicly_or_anonymously_accessible(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.9"
        description = "Ensure That Cloud KMS Cryptokeys Are Not Anonymously or Publicly Accessible"
        scored = True

        client = kms_v1.KeyManagementServiceClient(credentials=self.credentials)
        for location in self.locations:
            try:
                keyrings = client.list_key_rings(parent=f"projects/{self.project_id}/locations/{location}")
                # print(keyrings)

                for keyring in keyrings:

                    name = keyring.name
                    # print(name)
                    cryptokey_list = client.list_crypto_keys(
                        parent=f"{name}")

                    for cryptokey in cryptokey_list:
                        key_name = cryptokey.name
                        # response = service.projects().getIamPolicy(resource=key_name, body={}).execute()
                        iam_policy = client.get_iam_policy(request={"resource": key_name})
                        bindings = iam_policy.bindings

                        for binding in bindings:
                            members = binding.members
                            if "allUsers" in members or "allAuthenticatedUsers" in members:
                                result = "Not Compliant"
                                failReason = "IAM policy on Cloud KMS cryptokeys is not restricting anonymous and/or " \
                                             "public access"
                                offenders.append(key_name)

            except GoogleAPIError as error:

                # print(f"An error occurred: {}".format(str(error)))
                result = "Not Compliant"
                failReason = "An error occurred: {}".format(str(error))
                offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # Ensure KMS Encryption Keys Are Rotated Within a Period of 90 Days (Automated)
    def ensure_cloud_kms_cryptokeys_are_rotated_within_90_days(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.10"
        description = "Ensure KMS Encryption Keys Are Rotated Within a Period of 90 Days"
        scored = True

        client = kms_v1.KeyManagementServiceClient(credentials=self.credentials)

        for location in self.locations:
            try:
                keyrings = client.list_key_rings(parent=f"projects/{self.project_id}/locations/{location}")
                # print(keyrings)

                for keyring in keyrings:

                    name = keyring.name
                    # print(name)
                    cryptokey_list = client.list_crypto_keys(
                        parent=f"{name}")

                    for cryptokey in cryptokey_list:
                        key_name = cryptokey.name
                        rotation_period = cryptokey.rotation_period.days
                        if rotation_period > 90:
                            result = "Not Compliant"
                            failReason = "KMS encryption keys are not Rotated within a period of 90 days"
                            offenders.append(key_name)
                        # next_rotation_time = cryptokey.next_rotation_time
                    # for cryptokey in cryptokey_list:
                    #     key_name = cryptokey.name
                    #     version_list = client.list_crypto_key_versions(parent=key_name)

                    #     # Get the latest Cryptokey version
                    #     latest_version = max(version_list, key=lambda version: version.create_time)

                    #     # Get the current time
                    #     now = datetime.datetime.now(datetime.timezone.utc)

                    #     # Calculate the time difference
                    #     time_difference = now - latest_version.create_time
                    #     print(time_difference)

                    #     # Check if the key rotation period is greater than 90 days
                    #     if time_difference > datetime.timedelta(days=90):
                    #         print(f"Warning: Cryptokey '{key_name}' has not been rotated within the last 90 days.")

            except GoogleAPIError as error:

                # print(f"An error occurred: {}".format(str(error)))
                result = "Not Compliant"
                failReason = "An error occurred: {}".format(str(error))
                offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.11	Ensure That Separation of Duties Is Enforced While Assigning KMS Related Roles to Users (Automated)

    def ensure_separation_of_duties_is_enforced_while_assigning_kms_related_roles(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.11"
        description = "Ensure That Separation of Duties Is Enforced While Assigning KMS Related Roles to Users"
        scored = True

        try:

            service = googleapiclient.discovery.build(
                'cloudresourcemanager', 'v1', credentials=self.credentials)

            response = service.projects().getIamPolicy(resource=self.project_id, body={}).execute()
            cloudkms_admin_members = []
            cloudkms_encrypter_members = []
            cloudkms_decrypter_members = []
            cloudkms_encrypter_decrypter_members = []
            for binding in response['bindings']:
                # print(binding)

                if binding['role'] == "roles/cloudkms.admin":
                    cloudkms_admin_members.extend(binding["members"])

                if binding['role'] == "roles/cloudkms.cryptoKeyEncrypterDecrypter":
                    cloudkms_encrypter_decrypter_members.extend(binding["members"])

                if binding['role'] == "roles/cloudkms.cryptoKeyDecrypter":
                    cloudkms_decrypter_members.extend(binding["members"])

                if binding['role'] == "roles/cloudkms.cryptoKeyEncrypter":
                    cloudkms_encrypter_members.extend(binding["members"])

            for member in cloudkms_admin_members:
                if (member in cloudkms_encrypter_decrypter_members) or (member in cloudkms_encrypter_members) or (
                        member in cloudkms_decrypter_members):
                    result = "Not Compliant"
                    failReason = "Separation of Duties is not enforced while assigning KMS related roles to users."
                    offenders.append(member)
                    # print(member)

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.12	Ensure API Keys Only Exist for Active Services
    def ensure_api_keys_only_exist_for_active_services(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.12"
        description = "Ensure API Keys Only Exist for Active Services"
        scored = True

        try:

            client = api_keys_v2.ApiKeysClient(credentials=self.credentials)

            keys = client.list_keys(request={"parent": f"projects/{self.project_id}/locations/global"})

            for key in keys:
                result = "Not Compliant"
                failReason = "API keys exists in this project."
                print(key)
                offenders.append(key)

        except GoogleAPIError as error:
            # print("An error occurred: {}".format(error))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.13 Ensure API Keys Are Restricted To Use by Only Specified Hosts and Apps

    def ensure_api_keys_restricted_to_be_used_by_only_specified_hosts_and_apps(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "1.13"
        description = "Ensure API Keys Are Restricted To Use by Only Specified Hosts and Apps (Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.14	Ensure API Keys Are Restricted to Only APIs That Application Needs Access (Automated)

    def ensure_api_keys_restricted_to_only_apis_that_application_needs_access(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.14"
        description = "Ensure API Keys Are Restricted to Only APIs That Application Needs Access"
        scored = True

        try:

            client = api_keys_v2.ApiKeysClient(credentials=self.credentials)

            keys = client.list_keys(request={"parent": f"projects/{self.project_id}/locations/global"})

            for key in keys:
                restrictions_api_targets = key.restrictions.api_targets
                for api_target in restrictions_api_targets:
                    if api_target.service == "cloudapis.googleapis.com":
                        result = "Not Compliant"
                        failReason = "API Keys are not restricted to only APIs that Application needs access"
                        offenders.append(key)
                    if not api_target.methods:
                        result = "Not Compliant"
                        failReason = "API Keys are not restricted to only APIs that Application needs access"
                        offenders.append(key)

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.15 Ensure API Keys Are Rotated Every 90 Days (Automated)

    def ensure_api_keys_are_rotated_every_90_days(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.15"
        description = "Ensure API Keys Are Rotated Every 90 Days"
        scored = True

        try:

            client = api_keys_v2.ApiKeysClient(credentials=self.credentials)

            keys = client.list_keys(request={"parent": f"projects/{self.project_id}/locations/global"})

            for key in keys:

                creation_time = key.create_time

                # Get the current time
                now = datetime.datetime.now(datetime.timezone.utc)
                # print(now)

                # Calculate the time difference
                time_difference = now - creation_time

                print(time_difference)

                # Check if the key rotation period is greater than 90 days
                if time_difference > datetime.timedelta(days=90):
                    result = "Not Compliant"
                    failReason = "API Keys are not rotated in every 90 days"
                    offenders.append(key)

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.16	Ensure Essential Contacts is Configured for Organization (Automated)
    def ensure_essential_contacts_is_configured_for_organization(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.16"
        description = "Ensure Essential Contacts is Configured for Organization"
        scored = True

        try:

            client = essential_contacts_v1.EssentialContactsServiceClient(credentials=self.credentials)

            # Initialize request argument(s) The parent resource name format: organizations/{organization_id},
            # folders/{folder_id} or projects/{project_id}

            # To Checka at organization level
            # request = essential_contacts_v1.ListContactsRequest(
            #     parent=f"organizations/{organization_id}",
            # )

            request = essential_contacts_v1.ListContactsRequest(
                parent=f"projects/{self.project_id}",
            )

            # Make the request
            page_result = client.list_contacts(request=request)
            # print(page_result)

            legal_notifications_contact_exists = False
            security_notifications_contact_exists = False
            suspension_notifications_contact_exists = False
            technical_notifications_contact_exists = False
            technical_incidents_notifications_contact_exists = False

            for response in page_result:
                # print(response)
                if "TECHNICAL_INCIDENTS" in response.notification_category_subscriptions:
                    technical_incidents_notifications_contact_exists = True
                elif "TECHNICAL" in response.notification_category_subscriptions:
                    technical_notifications_contact_exists = True
                elif "SECURITY" in response.notification_category_subscriptions:
                    security_notifications_contact_exists = True
                elif "LEGAL" in response.notification_category_subscriptions:
                    legal_notifications_contact_exists = True
                elif "SUSPENSION" in response.notification_category_subscriptions:
                    suspension_notifications_contact_exists = True

            if not (
                    technical_incidents_notifications_contact_exists and
                    technical_notifications_contact_exists and
                    legal_notifications_contact_exists and
                    suspension_notifications_contact_exists and
                    security_notifications_contact_exists):
                result = "Not Compliant"
                failReason = "All Essential Contacts are not configured properly"
                offenders.append(self.project_id)

        except GoogleAPIError as error:
            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.17	Ensure that Dataproc Cluster is encrypted using Customer-Managed Encryption Key
    def ensure_dataproc_cluster_encrypted_using_customer_managed_encryption_key(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.17"
        description = "Ensure that Dataproc Cluster is encrypted using Customer- Managed Encryption Key"
        scored = True

        try:
            ######
            # Clusters present globally

            dataproc_client = dataproc_v1.ClusterControllerClient(credentials=self.credentials)
            dataproc_clusters = dataproc_client.list_clusters(project_id=self.project_id, region='global')

            for cluster in dataproc_clusters:
                if not cluster.config.encryption_config.gce_pd_kms_key_name:
                    result = "Not Compliant"
                    failReason = "Dataproc Cluster is not encrypted using Customer- Managed Encryption Key"
                    offenders.append(cluster.cluster_name)

            for region in self.locations:
                # print(region.name)
                dataproc_client = dataproc_v1.ClusterControllerClient(credentials=self.credentials,
                                                                      client_options={
                                                                          "api_endpoint": f"{region}-dataproc"
                                                                                          f".googleapis.com:443"}
                                                                      )

                dataproc_clusters = dataproc_client.list_clusters(project_id=self.project_id, region=region)

                for cluster in dataproc_clusters:
                    # print(cluster.cluster_name)
                    # print(cluster.config.encryption_config.gce_pd_kms_key_name)

                    # Check encryption configuration
                    if not cluster.config.encryption_config.gce_pd_kms_key_name:
                        result = "Not Compliant"
                        failReason = "Dataproc Cluster is not encrypted using Customer- Managed Encryption Key"
                        offenders.append(cluster.cluster_name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {}".format(str(error)))
            result = "Not Compliant"
            failReason = "An error occurred: {}".format(str(error))
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.18	Ensure Secrets are Not Stored in Cloud Functions Environment Variables by Using Secret Manager (Manual)

    def ensure_secrets_not_stored_in_cloud_functions_env_variables_using_secret_manager(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "1.18"
        description = "Ensure Secrets are Not Stored in Cloud Functions Environment Variables by Using Secret " \
                      "Manager (Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def get_iam_compliance(self):
        """
        :return:
        """
        compliance = [
            self.ensure_corporate_login_credentials_are_used(),
            self.ensure_mfa_enabled_for_all_non_service_account(),
            self.ensure_security_key_enforcement_enabled_for_all_admin_account(),
            self.ensure_only_gcp_managed_service_keys_for_each_service_account(),
            self.ensure_service_accounts_have_no_admin_privileges(),
            self.ensure_service_account_keys_rotated_every_90_days(),
            self.ensure_no_service_account_user_or_service_account_token_creator_role_at_project_level(),
            self.ensure_cloud_kms_cryptokeys_are_not_publicly_or_anonymously_accessible(),
            self.ensure_separation_of_duties_while_assigning_service_account_related_roles(),
            self.ensure_cloud_kms_cryptokeys_are_rotated_within_90_days(),
            self.ensure_separation_of_duties_is_enforced_while_assigning_kms_related_roles(),
            self.ensure_api_keys_only_exist_for_active_services(),
            self.ensure_api_keys_restricted_to_be_used_by_only_specified_hosts_and_apps(),
            self.ensure_dataproc_cluster_encrypted_using_customer_managed_encryption_key(),
            self.ensure_api_keys_restricted_to_only_apis_that_application_needs_access(),
            self.ensure_api_keys_are_rotated_every_90_days(),
            self.ensure_essential_contacts_is_configured_for_organization(),
            self.ensure_secrets_not_stored_in_cloud_functions_env_variables_using_secret_manager()
        ]
        return compliance
