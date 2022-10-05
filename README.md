# DynamoDB S3 Table Import CDK Example

Repository for an article on [clarkmains.com](https://www.clarkmains.com/blog/dynamodb-import-s3/).

## Repository contents

    .
    ├── data
    │   └── *.json              # JSON data files for import to DynamoDB
    ├── dynamodb_import_s3
    │   └── stack.py            # CDK Stack
    ├── tests                   # Fine-grained assertions to check import properties
    └── app.py                  # CDK App
