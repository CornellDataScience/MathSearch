# ML Model Branch

## Backend Environment:
- Option 1: `/opt/conda/bin`
- Option 2: `/home/ubuntu/MathSearch/ml-model/venv/bin`
- Option 3 (apply to SWE): packages all installed to default python, no need to activate any venv

## Connect to s3
To test connection, run below (notice the "-" on the second option). It should display directory in s3 buckets or cat the file.

option 1
```
aws s3 ls s3://mathsearch-intermediary
```
option 2
```
aws s3 cp s3://mathsearch-intermediary/test.txt -
```