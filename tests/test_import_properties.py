"""Test suite for the DynamoDB Import from S3 Stack.
"""

from aws_cdk import App, Stack
from aws_cdk.assertions import Match, Template
from dynamodb_import_s3.stack import DynamodbImportS3Stack

app = App()

stack = DynamodbImportS3Stack(app, "test-import-properties")

template = Template.from_stack(stack)


def test_import_properties_defined():
    """Assert the DynamoDB import properties created using property overrides
    are present on the DynamoDB Table."""
    template.has_resource_properties(
        "AWS::DynamoDB::Table", {
            "ImportSourceSpecification": {
                "S3BucketSource": {
                    "S3Bucket": Match.any_value()
                },
                "InputFormat": "DYNAMODB_JSON"
            }
        }
    )