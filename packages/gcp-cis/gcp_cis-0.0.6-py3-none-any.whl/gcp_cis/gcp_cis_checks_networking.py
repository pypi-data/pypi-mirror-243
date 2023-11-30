import googleapiclient.discovery
from google.api_core.exceptions import GoogleAPIError
from google.cloud import compute_v1
from google.cloud import dns


class networking_controls:
    def __init__(self, scopes, credentials, organization_id, project_id, locations, project_number):
        self.scopes = scopes
        self.credentials = credentials
        self.organization_id = organization_id
        self.project_id = project_id
        self.locations = locations
        self.project_number = project_number

    # 3.1	Ensure That the Default Network Does Not Exist in a Project
    def ensure_default_network_doesnot_exist_in_project(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.1"
        description = "Ensure That the Default Network Does Not Exist in a Project"
        scored = True

        try:

            network_client = compute_v1.NetworksClient(credentials=self.credentials)

            networks = network_client.list(project=self.project_id)

            for network in networks:

                if network.name == "default":
                    result = "Not Compliant"
                    failReason = "Default network is present in project"
                    offenders.append(network.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def ensure_legacy_network_doesnot_exist_in_project(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.2"
        description = "Ensure Legacy Networks Does Not Exist for Older Projects "
        scored = True

        try:

            network_client = compute_v1.NetworksClient(credentials=self.credentials)

            networks = network_client.list(project=self.project_id)

            for network in networks:
                # autoCreateSubnetworks: Must be set to create a VPC network. If not set, a legacy network is created.

                auto_create_subnetworks = network.auto_create_subnetworks
                if auto_create_subnetworks is not False and auto_create_subnetworks is not True:
                    result = "Not Compliant"
                    failReason = "Legacy network exists in the project"
                    offenders.append(network.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.3	Ensure That DNSSEC Is Enabled for Cloud DNS
    def ensure_dnssec_enabled_for_cloud_dns(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.3"
        description = "Ensure That DNSSEC Is Enabled for Cloud DNS"
        scored = True

        try:

            dns_client = dns.Client(project=self.project_id, credentials=self.credentials)

            zones = dns_client.list_zones()

            # Create the DNS API client
            service = googleapiclient.discovery.build('dns', 'v1', credentials=self.credentials)

            for zone in zones:
                # print(zone.description)
                # https://cloud.google.com/dns/docs/reference/v1/managedZones#resource
                request = service.managedZones().get(project=self.project_id, managedZone=zone.name)
                response = request.execute()
                if response['visibility'] == "public":
                    if response['dnssecConfig']['state'] != "on":
                        result = "Not Compliant"
                        failReason = "DNSSEC is not enabled for Cloud DNS"
                        offenders.append(zone.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.4	Ensure That RSA SHA1 Is Not Used for the Key-Signing Key in Cloud DNS DNSSEC (Automated)
    def ensure_rsasha1_not_used_for_key_signing_key_in_cloud_dns_dnssec(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.4"
        description = "Ensure That RSASHA1 Is Not Used for the Key-Signing Key in Cloud DNS DNSSEC"
        scored = True

        try:

            dns_client = dns.Client(project=self.project_id, credentials=self.credentials)

            zones = dns_client.list_zones()

            # Create the DNS API client
            service = googleapiclient.discovery.build('dns', 'v1', credentials=self.credentials)

            for zone in zones:
                # print(zone.description)
                # https://cloud.google.com/dns/docs/reference/v1/managedZones#resource
                request = service.managedZones().get(project=self.project_id, managedZone=zone.name)
                response = request.execute()
                # print(response)
                # print(zone.description)
                if response['visibility'] == "public":
                    default_key_specs = response['dnssecConfig']["defaultKeySpecs"]
                    if default_key_specs["algorithm"] == "rsasha1" and default_key_specs["keyType"] == "keySigning":
                        result = "Not Compliant"
                        failReason = "RSASHA1 is used for the Key-Signing Key in Cloud DNS DNSSEC"
                        offenders.append(zone.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.5	Ensure That RSASHA1 Is Not Used for the Zone-Signing Key in Cloud DNS DNSSEC (Automated)

    def ensure_rsasha1_not_used_for_zone_signing_key_in_cloud_dns_dnssec(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.5"
        description = "Ensure That RSASHA1 Is Not Used for the Zone-Signing Key in Cloud DNS DNSSEC"
        scored = True

        try:

            dns_client = dns.Client(project=self.project_id, credentials=self.credentials)

            zones = dns_client.list_zones()

            # Create the DNS API client
            service = googleapiclient.discovery.build('dns', 'v1', credentials=self.credentials)

            for zone in zones:
                # print(zone.description)
                # https://cloud.google.com/dns/docs/reference/v1/managedZones#resource
                request = service.managedZones().get(project=self.project_id, managedZone=zone.name)
                response = request.execute()
                # print(response)
                # print(zone.description)
                if response['visibility'] == "public":
                    default_key_specs = response['dnssecConfig']["defaultKeySpecs"]
                    if default_key_specs["algorithm"] == "rsasha1" and default_key_specs["keyType"] == "zoneSigning":
                        result = "Not Compliant"
                        failReason = "RSASHA1 is used for the Zone-Signing Key in Cloud DNS DNSSEC"
                        offenders.append(zone.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.6	Ensure That SSH Access Is Restricted From the Internet

    def ensure_ssh_access_restricted_over_internet(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.6"
        description = "Ensure That SSH Access Is Restricted From the Internet"
        scored = True

        try:

            service = googleapiclient.discovery.build('compute', 'v1', credentials=self.credentials)

            request = service.firewalls().list(project=self.project_id)
            while request is not None:
                response = request.execute()

                for firewall in response['items']:
                    # print(firewall)
                    if firewall['direction'] == "INGRESS":
                        if 'sourceRanges' in firewall and ('0.0.0.0/0' in firewall["sourceRanges"]):
                            for i in firewall["allowed"]:
                                # print(i)
                                if i["IPProtocol"] == "tcp" or i["IPProtocol"] == "ALL":
                                    if "ports" in i:
                                        # print(i["ports"])
                                        for port in i["ports"]:
                                            if "-" in port:
                                                a, b = port.split("-")
                                                if int(a) <= 22 <= int(b):
                                                    result = "Not Compliant"
                                                    failReason = "SSH Access is not restricted from the Internet"
                                                    offenders.append(firewall['name'])
                                            elif port == "22":
                                                result = "Not Compliant"
                                                failReason = "SSH Access is not restricted from the Internet"
                                                offenders.append(firewall['name'])
                                    else:
                                        result = "Not Compliant"
                                        failReason = "SSH Access is not restricted from the Internet"
                                        offenders.append(firewall['name'])

                request = service.firewalls().list_next(previous_request=request, previous_response=response)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.7	Ensure That RDP Access Is Restricted From the Internet
    def ensure_rdp_access_restricted_over_internet(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.7"
        description = "Ensure That RDP Access Is Restricted From the Internet"
        scored = True

        try:

            service = googleapiclient.discovery.build('compute', 'v1', credentials=self.credentials)

            request = service.firewalls().list(project=self.project_id)
            while request is not None:
                response = request.execute()

                for firewall in response['items']:
                    # print(firewall)
                    if firewall['direction'] == "INGRESS":
                        if 'sourceRanges' in firewall and ('0.0.0.0/0' in firewall["sourceRanges"]):
                            for i in firewall["allowed"]:
                                # print(i)
                                if i["IPProtocol"] == "tcp" or i["IPProtocol"] == "ALL":
                                    if "ports" in i:
                                        # print(i["ports"])
                                        for port in i["ports"]:
                                            if "-" in port:
                                                a, b = port.split("-")
                                                # print(a,b)
                                                if int(a) <= 3389 <= int(b):
                                                    result = "Not Compliant"
                                                    failReason = "RDP Access is not restricted from the Internet"
                                                    offenders.append(firewall['name'])
                                            elif port == "3389":
                                                result = "Not Compliant"
                                                failReason = "RDP Access is not restricted from the Internet"
                                                offenders.append(firewall['name'])
                                    else:
                                        result = "Not Compliant"
                                        failReason = "RDP Access is not restricted from the Internet"
                                        offenders.append(firewall['name'])

                request = service.firewalls().list_next(previous_request=request, previous_response=response)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.8	Ensure that VPC Flow Logs is Enabled for Every Subnet in a VPC Network

    def ensure_vpc_flow_logs_enabled_for_every_subnets(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.8"
        description = "Ensure that VPC Flow Logs is Enabled for Every Subnet in a VPC Network"
        scored = True

        try:

            service = googleapiclient.discovery.build('compute', 'v1', credentials=self.credentials)

            region_client = compute_v1.RegionsClient(credentials=self.credentials)
            region_list = region_client.list(project=self.project_id)

            for region in region_list:

                request = service.subnetworks().list(project=self.project_id, region=region.name)
                while request is not None:
                    response = request.execute()

                    for subnetwork in response['items']:
                        # print(subnetwork)
                        if subnetwork["purpose"] == "PRIVATE":
                            if "enableFlowLogs" in subnetwork:
                                if subnetwork["enableFlowLogs"]:
                                    if 'logConfig' in subnetwork:
                                        if subnetwork["logConfig"]["aggregationInterval"] == 'INTERVAL_5_SEC':
                                            if subnetwork["logConfig"]["flowSampling"] == 1:
                                                if subnetwork["logConfig"]["metadata"] == 'INCLUDE_ALL_METADATA':
                                                    pass
                                                else:
                                                    result = "Not Compliant"
                                                    failReason = "VPC Flow Logs is not Enabled for Every Subnet in a " \
                                                                 "VPC Network"
                                                    offenders.append(subnetwork["name"])
                                            else:
                                                result = "Not Compliant"
                                                failReason = "VPC Flow Logs is not Enabled for Every Subnet in a VPC " \
                                                             "Network"
                                                offenders.append(subnetwork["name"])
                                        else:
                                            result = "Not Compliant"
                                            failReason = "VPC Flow Logs is not Enabled for Every Subnet in a VPC " \
                                                         "Network"
                                            offenders.append(subnetwork["name"])
                                    else:
                                        result = "Not Compliant"
                                        failReason = "VPC Flow Logs is not Enabled for Every Subnet in a VPC Network"
                                        offenders.append(subnetwork["name"])
                                else:
                                    result = "Not Compliant"
                                    failReason = "VPC Flow Logs is not Enabled for Every Subnet in a VPC Network"
                                    offenders.append(subnetwork["name"])
                            else:
                                result = "Not Compliant"
                                failReason = "VPC Flow Logs is not Enabled for Every Subnet in a VPC Network"
                                offenders.append(subnetwork["name"])

                    request = service.subnetworks().list_next(previous_request=request, previous_response=response)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.9	Ensure No HTTPS or SSL Proxy Load Balancers Permit SSL Policies With Weak Cipher Suites (Manual)

    def ensure_no_https_or_ssl_proxy_loadbalancers_permit_ssl_policies_with_weak_cipher_suites(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "3.9"
        description = "Ensure No HTTPS or SSL Proxy Load Balancers Permit SSL Policies With Weak Cipher Suites (Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.10	Use Identity Aware Proxy (IAP) to Ensure Only Traffic From Google IP Addresses are 'Allowed' (Manual)

    def ensure_only_traffic_from_google_ip_addresses_are_allowed_using_IAP(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "3.10"
        description = "Use Identity Aware Proxy (IAP) to Ensure Only Traffic From Google IP Addresses are 'Allowed' (" \
                      "Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def get_networking_compliance(self):
        compliance = [
            self.ensure_default_network_doesnot_exist_in_project(),
            self.ensure_legacy_network_doesnot_exist_in_project(),
            self.ensure_dnssec_enabled_for_cloud_dns(),
            self.ensure_rsasha1_not_used_for_key_signing_key_in_cloud_dns_dnssec(),
            self.ensure_rsasha1_not_used_for_zone_signing_key_in_cloud_dns_dnssec(),
            self.ensure_ssh_access_restricted_over_internet(),
            self.ensure_rdp_access_restricted_over_internet(),
            self.ensure_vpc_flow_logs_enabled_for_every_subnets(),
            self.ensure_no_https_or_ssl_proxy_loadbalancers_permit_ssl_policies_with_weak_cipher_suites(),
            self.ensure_only_traffic_from_google_ip_addresses_are_allowed_using_IAP()
        ]
        return compliance
