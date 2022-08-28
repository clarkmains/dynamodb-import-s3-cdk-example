#!/usr/bin/env python3
import os

import aws_cdk as cdk

from dynamodb_import_s3.stack import DynamodbImportS3Stack


app = cdk.App()

DynamodbImportS3Stack(app, "dynamodb-import-s3-demo",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

app.synth()
