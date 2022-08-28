from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    Stack,
)
from constructs import Construct


class DynamodbImportS3Stack(Stack):
    """This Stack demonstrates the AWS DynamoDB Import from S3 feature in CDK.

    Original AWS blog post:
        https://aws.amazon.com/blogs/database/amazon-dynamodb-can-now-import-amazon-s3-data-into-a-new-table/
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # local path to the import data
        DATA_PATH = "./data"

        # name for the dynamodb table
        TABLE_NAME = "customer_events"

        # bucket to store data that will be imported to dynamodb
        bucket = s3.Bucket(self, "Bucket")

        # s3 bucket deployment copies the import data to s3
        deployment = s3_deployment.BucketDeployment(self, "BucketDeployment",
            destination_bucket=bucket,
            sources=[s3_deployment.Source.asset(DATA_PATH)]
        )

        # define the dynamodb table where the data will be imported
        table = dynamodb.Table(self, "Table",
            table_name=TABLE_NAME,
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING
            )
        )

        # add dependency so the import data will be uploaded to s3 before
        # the dynamodb table is created, otherwise data import process may fail
        table.node.add_dependency(deployment)

        # use the L1 construct of the dynamodb table to add property overrides
        # to implement the import from s3 functionality - this functionality
        # is not yet stable and thus not natively in the dynamodb L2 construct
        cfn_table: dynamodb.CfnTable = table.node.default_child

        cfn_table.add_property_override(
            "ImportSourceSpecification.S3BucketSource.S3Bucket",
            bucket.bucket_name
        )

        cfn_table.add_property_override(
            "ImportSourceSpecification.InputFormat",
            "DYNAMODB_JSON"
        )
