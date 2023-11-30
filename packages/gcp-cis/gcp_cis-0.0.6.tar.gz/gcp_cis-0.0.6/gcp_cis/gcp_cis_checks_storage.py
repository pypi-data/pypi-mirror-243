from google.api_core.exceptions import GoogleAPIError
from google.cloud import storage


class storage_controls:
    def __init__(self, scopes, credentials, organization_id, project_id, locations, project_number):
        self.scopes = scopes
        self.credentials = credentials
        self.organization_id = organization_id
        self.project_id = project_id
        self.locations = locations
        self.project_number = project_number

    # 5.1	Ensure That Cloud Storage Bucket Is Not Anonymously or Publicly Accessible (Automated)
    def ensure_cloud_storage_bucket_is_not_anonymously_or_publicly_accessible(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "5.1"
        description = "Ensure That Cloud Storage Bucket Is Not Anonymously or Publicly Accessible"
        scored = True

        # https://cloud.google.com/storage/docs/access-control/using-iam-permissions#client-libraries_1
        # https://cloud.google.com/storage/docs/samples/storage-list-buckets#storage_list_buckets-python

        try:

            storage_client = storage.Client(credentials=self.credentials)
            buckets = storage_client.list_buckets()

            for i in buckets:
                bucket = storage_client.bucket(i.name)
                policy = bucket.get_iam_policy(requested_policy_version=3)

                for binding in policy.bindings:
                    # print(binding["members"])
                    for member in binding["members"]:
                        # print(member)
                        if "allUsers" in member or "allAuthenticatedUsers" in member:
                            result = "Not Compliant"
                            failReason = "Cloud Storage Bucket is Anonymously or Publicly Accessible"
                            offenders.append(bucket.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 5.2	Ensure That Cloud Storage Buckets Have Uniform Bucket-Level Access Enabled

    def ensure_cloud_storage_buckets_have_uniform_bucket_level_access_enabled(self):
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "5.2"
        description = "Ensure That Cloud Storage Buckets Have Uniform Bucket- Level Access Enabled"
        scored = True

        # https://cloud.google.com/storage/docs/access-control/using-iam-permissions#client-libraries_1
        # https://cloud.google.com/storage/docs/samples/storage-list-buckets#storage_list_buckets-python

        try:

            storage_client = storage.Client(credentials=self.credentials)
            buckets = storage_client.list_buckets()

            for i in buckets:

                bucket = storage_client.bucket(i.name)
                iam_config = bucket.iam_configuration
                uniform_bucket_level_access = iam_config.uniform_bucket_level_access_enabled

                if not uniform_bucket_level_access:
                    result = "Not Compliant"
                    failReason = "Cloud Storage Bucket doesnot have Uniform Bucket- Level Access Enabled"
                    offenders.append(bucket.name)

        except GoogleAPIError as error:

            # print(f"An error occurred: {error}")
            result = "Not Compliant"
            failReason = f"An error occurred: {error}"
            offenders.append(self.project_id)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    def get_storage_compliance(self):
        return [
            self.ensure_cloud_storage_bucket_is_not_anonymously_or_publicly_accessible(),
            self.ensure_cloud_storage_buckets_have_uniform_bucket_level_access_enabled()
        ]
