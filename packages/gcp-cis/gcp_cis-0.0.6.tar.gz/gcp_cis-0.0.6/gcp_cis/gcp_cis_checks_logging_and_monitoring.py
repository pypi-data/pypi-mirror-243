import googleapiclient.discovery
from google.api_core.exceptions import GoogleAPIError
from google.cloud import accessapproval_v1
from google.cloud import asset_v1
# from datetime import datetime, timezone, timedelta
from google.cloud import compute_v1
from google.cloud import logging_v2
from google.cloud import monitoring_v3
from google.cloud import storage
# Authentication
from googleapiclient.discovery import build


class logging_monitoring_controls:
    def __init__(self, scopes, credentials, organization_id, project_id, locations, project_number):
        self.scopes = scopes
        self.credentials = credentials
        self.organization_id = organization_id
        self.project_id = project_id
        self.locations = locations
        self.project_number = project_number

    # 2.1 Ensure That Cloud Audit Logging Is Configured Properly (
    def ensure_cloud_audit_logging_is_enabled_properly(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.1"
        description = "Ensure That Cloud Audit Logging Is Configured Properly"
        scored = True

        service = googleapiclient.discovery.build(
            'cloudresourcemanager', 'v1', credentials=self.credentials)

        response = service.projects().getIamPolicy(resource=self.project_id, body={}).execute()

        # https://cloud.google.com/logging/docs/audit/configure-data-access#auditconfig_objects

        try:
            if "auditConfigs" in response:
                for config in response["auditConfigs"]:
                    if config["service"] == "allServices":
                        log_type_data_read = False
                        log_type_data_write = False
                        for i in config["auditLogConfigs"]:
                            if "exemptedMembers" not in i:
                                if i["logType"] == 'DATA_READ':
                                    log_type_data_read = True
                                if i["logType"] == 'DATA_WRITE':
                                    log_type_data_write = True
                        if log_type_data_read and log_type_data_write:
                            # print("tested")
                            continue
                        else:
                            result = "Not Compliant"
                            failReason = "cloud_audit_logging_is_not_enabled_properly"
                            offenders.append(self.project_id)
                    else:
                        result = "Not Compliant"
                        failReason = "cloud_audit_logging_is_not_enabled_properly"
                        offenders.append(self.project_id)
            else:
                result = "Not Compliant"
                failReason = "cloud_audit_logging_is_not_enabled_properly"
                offenders.append(self.project_id)

        except GoogleAPIError as error:
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.2 Ensure That Sinks Are Configured for All Log Entries
    def ensure_sinks_are_configured_for_all_log_entries(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.2"
        description = "Ensure That Sinks Are Configured for All Log Entries"
        scored = True

        try:
            # Create a Logging client
            client = logging_v2.Client(credentials=self.credentials)

            # List sinks for the project
            parent = f"projects/{self.project_id}"
            sinks = client.list_sinks(parent=parent)

            empty_filter_sink_exists = False

            sink_list = []

            for sink in sinks:
                # print(sink.filter_)
                # print(sink.destination)
                if not sink.filter_:
                    empty_filter_sink_exists = True
                else:
                    sink_list.append(sink.name)

            if not empty_filter_sink_exists:
                result = "Not Compliant"
                failReason = "No sinks with an empty filter found"
                offenders.extend(sink_list)

        except GoogleAPIError as error:
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.3 Ensure That Retention Policies on Cloud Storage Buckets Used for Exporting Logs Are Configured Using Bucket
    # Lock
    def ensure_retention_policies_on_cloud_storage_buckets_used_for_exporting_logs_are_configured_using_bucket_lock(
            self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.3"
        description = "Ensure That Retention Policies on Cloud Storage Buckets Used for Exporting Logs Are " \
                      "Configured Using Bucket Locks"
        scored = True

        try:
            client = logging_v2.Client(credentials=self.credentials)
            # List sinks for the project
            parent = f"projects/{self.project_id}"
            sinks = client.list_sinks(parent=parent)

            storage_client = storage.Client(credentials=self.credentials)

            for sink in sinks:
                # print(sink.filter_)
                # print(type(sink.destination))
                destination = str(sink.destination)
                if destination.startswith("storage.googleapis.com/"):
                    bucket_name = destination[len("storage.googleapis.com/"):]
                    bucket = storage_client.get_bucket(bucket_or_name=bucket_name)
                    if not bucket.retention_policy_locked:
                        result = "Not Compliant"
                        failReason = "Retention Policies on Cloud Storage Buckets used for exporting Logs are not " \
                                     "configured using bucket locks"
                        offenders.append(destination)

        except GoogleAPIError as error:
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.4 Ensure Log Metric Filter and Alerts Exist for Project Ownership Assignments/Changesdef

    def ensure_log_metrics_filter_and_alerts_exist_for_project_ownership_assignments(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.4"
        description = "Ensure Log Metric Filter and Alerts Exist for Project Ownership Assignments/Changesdef"
        scored = True

        try:

            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == '(protoPayload.serviceName' \
                                                                          '="cloudresourcemanager.googleapis.com' \
                                                                          '")AND(' \
                                                                          'ProjectOwnershipORprojectOwnerInvitee)OR(' \
                                                                          'protoPayload.serviceData.policyDelta' \
                                                                          '.bindingDeltas.action="REMOVE' \
                                                                          '"ANDprotoPayload.serviceData.policyDelta' \
                                                                          '.bindingDeltas.role="roles/owner")OR(' \
                                                                          'protoPayload.serviceData.policyDelta' \
                                                                          '.bindingDeltas.action="ADD"ANDprotoPayload' \
                                                                          '.serviceData.policyDelta.bindingDeltas' \
                                                                          '.role="roles/owner")':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for Project Ownership Assignments/Changesdef"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.5 Ensure That the Log Metric Filter and Alerts Exist for Audit Configuration Changes

    def ensure_log_metrics_filter_and_alerts_exist_for_audit_configuration_changes(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.5"
        description = "Ensure Log Metric Filter and Alerts Exist for Audit Configuration Changes"
        scored = True

        try:

            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == 'protoPayload.methodName="SetIamPolicy' \
                                                                          '"ANDprotoPayload.serviceData.policyDelta' \
                                                                          '.auditConfigDeltas:*':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for Audit Configuration Changes"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.6 Ensure That the Log Metric Filter and Alerts Exist for Custom Role Changes

    def ensure_log_metrics_filter_and_alerts_exist_for_custom_role_changes(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.6"
        description = "Ensure Log Metric Filter and Alerts Exist for Audit Custom Role Changes"
        scored = True

        try:

            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == 'resource.type="iam_role"AND(' \
                                                                          'protoPayload.methodName="google.iam.admin' \
                                                                          '.v1.CreateRole"ORprotoPayload.methodName' \
                                                                          '="google.iam.admin.v1.DeleteRole' \
                                                                          '"ORprotoPayload.methodName="google.iam' \
                                                                          '.admin.v1.UpdateRole")':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for Custom Role Changes"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.7 Ensure That the Log Metric Filter and Alerts Exist for VPC Network Firewall Rule Changes

    def ensure_log_metrics_filter_and_alerts_exist_for_vpc_network_firewall_rule_changes(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.7"
        description = "Ensure Log Metric Filter and Alerts Exist for VPC Network Firewall Rule Changes"
        scored = True

        try:

            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == 'resource.type="gce_firewall_rule"AND(' \
                                                                          'protoPayload.methodName:"compute.firewalls' \
                                                                          '.patch"ORprotoPayload.methodName:"compute' \
                                                                          '.firewalls.insert"ORprotoPayload' \
                                                                          '.methodName:"compute.firewalls.delete")':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for VPC Network Firewall Rule Changes"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.8 Ensure That the Log Metric Filter and Alerts Exist for VPC Network Route Changes

    def ensure_log_metrics_filter_and_alerts_exist_for_vpc_network_firewall_route_changes(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.8"
        description = "Ensure Log Metric Filter and Alerts Exist for VPC Network Firewall Route Changes"
        scored = True

        try:
            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == 'resource.type="gce_route"AND(' \
                                                                          'protoPayload.methodName:"compute.routes' \
                                                                          '.delete"ORprotoPayload.methodName:"compute' \
                                                                          '.routes.insert")':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for VPC Network Firewall Route Changes"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.9 Ensure That the Log Metric Filter and Alerts Exist for VPC Network Changes

    def ensure_log_metrics_filter_and_alerts_exist_for_vpc_network_changes(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.9"
        description = "Ensure Log Metric Filter and Alerts Exist for VPC Network Changes"
        scored = True

        try:

            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == 'resource.type="gce_network"ANDprotoPayload' \
                                                                          '.methodName="beta.compute.networks.insert' \
                                                                          '"ORprotoPayload.methodName="beta.compute' \
                                                                          '.networks.patch"ORprotoPayload.methodName' \
                                                                          '="v1.compute.networks.delete' \
                                                                          '"ORprotoPayload.methodName="v1.compute' \
                                                                          '.networks.removePeering"ORprotoPayload' \
                                                                          '.methodName="v1.compute.networks' \
                                                                          '.addPeering"':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for VPC Network Changes"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.10 Ensure That the Log Metric Filter and Alerts Exist for Cloud Storage IAM Permission Changes

    def ensure_log_metrics_filter_and_alerts_exist_for_cloud_storage_iam_permission_changes(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.10"
        description = "Ensure Log Metric Filter and Alerts Exist for Cloud Storage IAM Permission Changes"
        scored = True

        try:

            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == 'resource.type=gcs_bucketANDprotoPayload' \
                                                                          '.methodName="storage.setIamPermissions"':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for Cloud Storage IAM Permission Changes"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.11 Ensure That the Log Metric Filter and Alerts Exist for SQL Instance Configuration Changes

    def ensure_log_metrics_filter_and_alerts_exist_for_sql_instance_configuration_changes(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.11"
        description = "Ensure Log Metric Filter and Alerts Exist for SQL Instance Configuration Changes"
        scored = True

        try:

            logging_client = logging_v2.Client(credentials=self.credentials)

            metrics = logging_client.list_metrics()

            metric_filter_exists = False
            alert_policy_exists = False
            metrics_list = []

            monitoring_client = monitoring_v3.AlertPolicyServiceClient(credentials=self.credentials)

            request = monitoring_v3.ListAlertPoliciesRequest(
                name=f"projects/{self.project_id}"
            )

            alert_policies = monitoring_client.list_alert_policies(request=request)

            for metric in metrics:

                metrics_list.append(metric.name)
                # print(str(metric.filter_).replace("\r\n", "").replace(" ", ""))
                if str(metric.filter_).replace("\r\n", "").replace(" ",
                                                                   "") == 'protoPayload.methodName="cloudsql' \
                                                                          '.instances.update"':
                    metric_filter_exists = True
                    # print(metric_filter_present)
                    for alert_policy in alert_policies:
                        if alert_policy.enabled:
                            for condition in alert_policy.conditions:
                                # print(condition.condition_threshold.filter)
                                if condition.condition_threshold.filter == \
                                        f'metric.type="logging.googleapis.com/user/{metric.name}"':
                                    alert_policy_exists = True

            # print(alert_policy_exists and metric_filter_exists)

            if not (alert_policy_exists and metric_filter_exists):
                result = "Not Compliant"
                failReason = "Log metric filter and alerts does not exist for SQL Instance Configuration Changes"
                offenders.extend(metrics_list)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.12	Ensure That Cloud DNS Logging Is Enabled for All VPC Networks

    def ensure_dns_logging_is_enabled_for_all_vpc_networks(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.12"
        description = "Ensure That Cloud DNS Logging Is Enabled for All VPC Networks"
        scored = True

        try:

            client = compute_v1.NetworksClient(credentials=self.credentials)

            # List all VPC networks in the project
            vpcs = client.list(project=self.project_id)

            service = build('dns', 'v1', credentials=self.credentials)

            dns_policies = service.policies()
            dns_policy_list = dns_policies.list(project=self.project_id).execute()

            # print(dns_policy_list["policies"])

            vpc_names = []

            for vpc in vpcs:
                vpc_names.append(vpc.name)

            for policy in dns_policy_list["policies"]:

                if policy['enableLogging']:

                    # print(policy["networks"])
                    for network in policy["networks"]:
                        if network in vpc_names:
                            vpc_names.remove(network)

            if vpc_names:
                result = "Not Compliant"
                failReason = "Cloud DNS Logging is not enabled for all VPC networks"
                offenders.extend(vpc_names)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.13 Ensure Cloud Asset Inventory Is Enabled
    def ensure_cloud_asset_inventory_enabled(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.13"
        description = "Ensure Cloud Asset Inventory Is Enabled"
        scored = True

        # client = service_usage.ServiceUsageClient(credentials=credentials)
        # # Build the parent resource name
        # parent = f"projects/{project_id}"
        # # List enabled services using the parent resource name
        # response = client.list_services(request={"parent":parent})
        # # Print the list of enabled services
        # for service in response.services:
        #     print(service.name)
        #     print(service.state)

        try:
            # Create a client for the Cloud Asset API
            client = asset_v1.AssetServiceClient(credentials=self.credentials)

            # Build the parent resource name
            parent = f"projects/{self.project_id}"

            # List assets using the parent resource name
            assets = client.list_assets(parent=parent)

            # Check if any assets are returned
            for _ in assets:
                # If assets are returned, Cloud Asset Inventory is enabled
                continue

        except GoogleAPIError:

            result = "Not Compliant"
            failReason = "Cloud Asset Inventory is not enabled "
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.14	Ensure 'Access Transparency' is 'Enabled' (Manual)
    def ensure_access_transparency_is_enabled(self):
        result = "Manual"
        failReason = "Control not implemented using API, please verify manually"
        offenders = []
        control = "2.14"
        description = "Ensure 'Access Transparency' is 'Enabled' (Manual)"
        scored = True

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.15	Ensure 'Access Approval' is 'Enabled'
    def ensure_access_approval_enabled(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.15"
        description = "Ensure 'Access Approval' is 'Enabled'"
        scored = True

        try:

            client = accessapproval_v1.AccessApprovalClient(credentials=self.credentials)
            accessapproval_v1.GetAccessApprovalSettingsMessage()
            client.get_access_approval_settings()

        except GoogleAPIError:

            result = "Not Compliant"
            failReason = "Access Approval is not enabled"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.16 Ensure Logging is enabled for HTTP(S) Load Balancer
    def ensure_logging_is_enabled_for_https_load_balancer(self):

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.16"
        description = "Ensure Logging is enabled for HTTP(S) Load Balancer"
        scored = True

        try:

            service = build('compute', 'v1', credentials=self.credentials)

            request = service.backendServices().list(project=self.project_id)
            while request is not None:
                response = request.execute()

                if 'items' in response:
                    for backend_service in response['items']:
                        # Change code below to process each `backend_service` resource:
                        if not backend_service['logConfig']['enable']:
                            result = "Not Compliant"
                            failReason = "Logging is not enabled in all backend services for HTTP(S) Load Balancer"
                            offenders.append(backend_service['name'])

                request = service.backendServices().list_next(previous_request=request, previous_response=response)

        except GoogleAPIError as error:

            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def get_logging_monitoring_compliance(self):
        """
        :return:
        """
        compliance = []
        compliance.append(self.ensure_cloud_audit_logging_is_enabled_properly())
        compliance.append(self.ensure_access_approval_enabled())
        compliance.append(self.ensure_access_transparency_is_enabled())
        compliance.append(self.ensure_cloud_asset_inventory_enabled())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_audit_configuration_changes())
        compliance.append(self.ensure_sinks_are_configured_for_all_log_entries())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_custom_role_changes())
        compliance.append(self.ensure_retention_policies_on_cloud_storage_buckets_used_for_exporting_logs_are_configured_using_bucket_lock())
        compliance.append(self.ensure_dns_logging_is_enabled_for_all_vpc_networks())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_sql_instance_configuration_changes())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_project_ownership_assignments())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_cloud_storage_iam_permission_changes())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_vpc_network_firewall_rule_changes())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_vpc_network_firewall_route_changes())
        compliance.append(self.ensure_log_metrics_filter_and_alerts_exist_for_vpc_network_changes())
        compliance.append(self.ensure_logging_is_enabled_for_https_load_balancer())

        return compliance
