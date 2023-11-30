from collections import defaultdict

from google.api_core.exceptions import GoogleAPIError
from google.cloud import compute_v1


class vms_controls:
    def __init__(self, scopes, credentials, organization_id, project_id, locations, project_number):
        self.scopes = scopes
        self.credentials = credentials
        self.organization_id = organization_id
        self.project_id = project_id
        self.locations = locations
        self.project_number = project_number

    # 4.1	Ensure That Instances Are Not Configured To Use the Default Service Account (Automated)
    def ensure_instances_not_configured_to_use_default_service_accounts(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.1"
        description = "Ensure That Instances Are Not Configured To Use the Default Service Account"
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            # Despite using the `max_results` parameter, you don't need to handle the pagination
            # yourself. The returned `AggregatedListPager` object handles pagination
            # automatically, returning separated pages as you iterate over the results.
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    # print(f" {zone}:")
                    for instance in response.instances:
                        if instance.name.startswith("gke-"):
                            continue
                        elif "goog-gke-node" in instance.labels:
                            continue
                        else:
                            for account in instance.service_accounts:
                                # print(account.email)
                                if account.email == str(self.project_number) + "-compute@developer.gserviceaccount.com":
                                    result = "Not Compliant"
                                    failReason = "Instances are configured to use the Default Service Account"
                                    offenders.append(instance.name)
        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.2	Ensure That Instances Are Not Configured To Use the Default Service Account With Full Access to All Cloud APIs

    def ensure_instances_not_configured_to_use_default_service_accounts_with_full_access_to_all_cloud_apis(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.2"
        description = "Ensure That Instances Are Not Configured To Use the Default Service Account With Full Access to All Cloud APIs"
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            # Despite using the `max_results` parameter, you don't need to handle the pagination
            # yourself. The returned `AggregatedListPager` object handles pagination
            # automatically, returning separated pages as you iterate over the results.
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    # print(f" {zone}:")
                    for instance in response.instances:
                        if instance.name.startswith("gke-"):
                            continue
                        elif "goog-gke-node" in instance.labels:
                            continue
                        else:
                            for account in instance.service_accounts:
                                if account.email == str(self.project_number) + "-compute@developer.gserviceaccount.com":
                                    if "https://www.googleapis.com/auth/cloud-platform" in account.scopes:
                                        result = "Not Compliant"
                                        failReason = "Instances are configured to use the Default Service Account with full access to all cloud APIs"
                                        offenders.append(instance.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.3 Ensure “Block Project-Wide SSH Keys” Is Enabled for VM Instances
    def ensure_block_project_wide_ssh_keys_is_enabled_for_VM_instances(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.3"
        description = "Ensure “Block Project-Wide SSH Keys” Is Enabled for VM Instances"
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            # Despite using the `max_results` parameter, you don't need to handle the pagination
            # yourself. The returned `AggregatedListPager` object handles pagination
            # automatically, returning separated pages as you iterate over the results.
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    for instance in response.instances:
                        # print(instance.metadata.items)
                        key_is_present = False
                        for item in instance.metadata.items:

                            if item.key == "block-project-ssh-keys":
                                key_is_present = True
                                # print(instance.name, item.key, item.value)
                                if item.value != "true":
                                    result = "Not Compliant"
                                    failReason = "Block Project-Wide SSH Keys is not enabled for VM instances"
                                    offenders.append(instance.name)
                        if not key_is_present:
                            # print(instance.name, key_is_present)
                            result = "Not Compliant"
                            failReason = "Block Project-Wide SSH Keys is not enabled for VM instances"
                            offenders.append(instance.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.4 Ensure Oslogin is Enabled for a Project
    def ensure_os_login_is_enabled_for_project(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.4"
        description = "Ensure OSlogin is Enabled for a Project "
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            # project = compute_v1.Project( credentials=self.credentials)
            # print(project.common_instance_metadata.items)

            # project_client = compute_v1.ProjectsClient(credentials=self.credentials)
            # my_project = project_client.get(project=self.project_id)
            # key_present = False
            # for item in my_project.common_instance_metadata.items:
            #     # print(item)
            #     if item.key == "enable-oslogin":
            #         key_present = True
            #         if item.value == "TRUE":
            #             project_instance_metadata_enable_oslogin = True

            # if project_instance_metadata_enable_oslogin == True:

            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    for instance in response.instances:
                        if instance.name.startswith("gke-"):
                            continue
                        elif "goog-gke-node" in instance.labels:
                            continue
                        else:
                            # instance.metadata
                            # print(instance.metadata.items)
                            key_is_present = False
                            for item in instance.metadata.items:
                                # print(item)
                                if item.key == "enable-oslogin":
                                    key_is_present = True
                                    # print(instance.name, item.key, item.value)
                                    if item.value != "TRUE":
                                        result = "Not Compliant"
                                        failReason = "OSlogin is not enabled"
                                        offenders.append(instance.name)
                        if not key_is_present:
                            # print(instance.name, key_is_present)
                            result = "Not Compliant"
                            failReason = "OSlogin is not enabled"
                            offenders.append(instance.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.5	Ensure ‘Enable Connecting to Serial Ports’ Is Not Enabled for VM Instance

    def ensure_enable_connecting_to_serial_ports_is_not_enabled_for_vm_instances(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.5"
        description = "Ensure ‘Enable Connecting to Serial Ports’ Is Not Enabled for VM Instance"
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    for instance in response.instances:
                        for item in instance.metadata.items:
                            # print(item)
                            if item.key == "serial-port-enable":
                                # print(instance.name, item.key, item.value)
                                if item.value != "0" or item.value != "false":
                                    result = "Not Compliant"
                                    failReason = "‘Enable Connecting to Serial Ports’ is enabled for VM instance"
                                    offenders.append(instance.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.6	Ensure That IP Forwarding Is Not Enabled on Instances
    def ensure_ip_forwarding_is_not_enabled_on_vm_instances(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.6"
        description = "Ensure that IP forwarding is not enabled on Instances"
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    for instance in response.instances:
                        # print(instance.shielded_instance_config)
                        if instance.can_ip_forward:
                            result = "Not Compliant"
                            failReason = "IP forwarding is enabled on VM instances"
                            offenders.append(instance.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.7 Ensure VM Disks for Critical VMs Are Encrypted With Customer-Supplied Encryption Keys (CSEK)

    def ensure_vm_disks_are_encrypted_with_customer_supplied_encryption_keys(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.7"
        description = "Ensure VM Disks for Critical VMs Are Encrypted With Customer-Supplied Encryption Keys (CSEK)"
        scored = True

        try:

            # service = build('compute', 'v1', credentials=self.credentials)

            disk_client = compute_v1.DisksClient(credentials=self.credentials)

            disks = disk_client.aggregated_list(project=self.project_id)

            all_disks = defaultdict(list)

            for zone, response in disks:
                if response.disks:
                    all_disks[zone].extend(response.disks)
                    for disk in response.disks:
                        # print(disk.name)
                        if disk.disk_encryption_key:
                            if disk.disk_encryption_key.sha256:
                                continue
                            else:
                                result = "Not Compliant"
                                failReason = "VM Disks are not encrypted With Customer-Supplied Encryption Keys (CSEK)"
                                offenders.append(disk.name)

                        else:
                            result = "Not Compliant"
                            failReason = "VM Disks are not encrypted With Customer-Supplied Encryption Keys (CSEK)"
                            offenders.append(disk.name)

            # service = build('compute', 'v1', credentials=self.credentials)
            # request = service.disks().list(project=self.project_id, zone = 'us-central1-a')
            # while request is not None:
            #     response = request.execute()

            #     for disk in response['items']:

            #         if "diskEncryptionKey" in disk:
            #             if "sha256" in disk["diskEncryptionKey"]:
            #                 if disk["diskEncryptionKey"]["sha256"] == "":
            #                     result = "Not Compliant"
            #                     failReason = "IP forwarding is enabled on VM instances"
            #                     offenders.append(disk["name"])
            # request = service.disks().list_next(previous_request=request, previous_response=response)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.8 Ensure Compute Instances Are Launched With Shielded VM Enabled

    def ensure_instances_are_launched_with_shielded_vm_enabled(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.8"
        description = "Ensure Compute Instances Are Launched With Shielded VM Enabled"
        scored = True
        try:
            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    for instance in response.instances:
                        if instance.shielded_instance_config:
                            if instance.shielded_instance_config.enable_integrity_monitoring == True and instance.shielded_instance_config.enable_vtpm == True:
                                continue
                            else:
                                result = "Not Compliant"
                                failReason = "Compute Instances Are Launched With Shielded VM is not Enabled"
                                offenders.append(instance.name)

            return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                    'Description': description, 'ControlId': control}

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.9 Ensure That Compute Instances Do Not Have Public IP Addresses

    def ensure_instances_does_not_have_public_ip_addresses(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.9"
        description = "Ensure That Compute Instances Do Not Have Public IP Addresses"
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    for instance in response.instances:
                        # print(instance.name)
                        network_interfaces = instance.network_interfaces
                        for network_interface in network_interfaces:
                            if network_interface.access_configs:
                                for access_config in network_interface.access_configs:
                                    # print(access_config)
                                    if access_config.nat_i_p:
                                        result = "Not Compliant"
                                        failReason = "Compute instances have Public IP Addresses"
                                        offenders.append(instance.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.10	Ensure That App Engine Applications Enforce HTTPS Connections

    def ensure_app_engine_applications_enforce_https_connections(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "4.10"
        description = "Ensure That App Engine Applications Enforce HTTPS Connections (Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.11	Ensure That Compute Instances Have Confidential Computing Enabled

    def ensure_instances_have_confidential_computing_enabled(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.11"
        description = "Ensure that Compute instances have confidential Computing enabled"
        scored = True

        try:

            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            request = compute_v1.AggregatedListInstancesRequest()
            request.project = self.project_id
            # Use the `max_results` parameter to limit the number of results that the API returns per response page.
            request.max_results = 50

            agg_list = instance_client.aggregated_list(request=request)

            all_instances = defaultdict(list)
            for zone, response in agg_list:
                if response.instances:
                    all_instances[zone].extend(response.instances)
                    for instance in response.instances:
                        # print(type(instance.confidential_instance_config.enable_confidential_compute))
                        if "/n2d-" in instance.machine_type:
                            if not instance.confidential_instance_config.enable_confidential_compute:
                                result = "Not Compliant"
                                failReason = "Confidential Computing is not enabled on VM instances"
                                offenders.append(instance.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.12	Ensure the Latest Operating System Updates Are Installed On Your Virtual Machines in All Projects (Manual)

    def ensure_latest_operating_syatem_updates_are_intalled_on_your_virtual_machines(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "4.12"
        description = "Ensure the Latest Operating System Updates Are Installed On Your Virtual Machines in All Projects (Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def get_vms_compliance(self):
        compliance = [
            self.ensure_instances_not_configured_to_use_default_service_accounts(),
            self.ensure_instances_not_configured_to_use_default_service_accounts_with_full_access_to_all_cloud_apis(),
            self.ensure_block_project_wide_ssh_keys_is_enabled_for_VM_instances(),
            self.ensure_os_login_is_enabled_for_project(),
            self.ensure_enable_connecting_to_serial_ports_is_not_enabled_for_vm_instances(),
            self.ensure_ip_forwarding_is_not_enabled_on_vm_instances(),
            self.ensure_vm_disks_are_encrypted_with_customer_supplied_encryption_keys(),
            self.ensure_instances_are_launched_with_shielded_vm_enabled(),
            self.ensure_instances_does_not_have_public_ip_addresses(),
            self.ensure_app_engine_applications_enforce_https_connections(),
            self.ensure_instances_have_confidential_computing_enabled(),
            self.ensure_latest_operating_syatem_updates_are_intalled_on_your_virtual_machines(),
        ]
        return compliance
