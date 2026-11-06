# Deployment and Security Testing Log

## Deployment 001 — Initial AWS Environment
**Date:** 6 November 2026
**Region:** ap-southeast-2 (Sydney)
**Provisioning:** Terraform v1.17.0
**AWS Provider:** v6.72.0
**Environment:** Personal AWS security lab

### Objective
Deploy the initial serverless API infrastructure using Terraform and verify that its exposed API routes reject unauthenticated requests.

### Deployment
Terraform execution plan:

`Plan: 12 to add, 0 to change, 0 to destroy.`

Resources deployed include API Gateway, Lambda, DynamoDB and supporting IAM and CloudWatch resources.

### Security Test 001 — Unauthenticated API Access
**Method:** HTTP GET request without AWS credentials or SigV4 signing.

**Endpoint:** `/health`

**Expected:** HTTP 403 Forbidden

**Observed:**

```
HTTP/1.1 403 Forbidden
Content-Type: application/json

{"message":"Forbidden"}
```
**Result:** PASS

**Interpretation:** The API Gateway endpoint rejected the unsigned request, consistent with the configured AWS IAM authorisation requirement.

**Limitation:** This test alone does not prove that legitimate IAM-authorised requests succeed or that every route has been correctly protected.

### Lessons Learned

- Terraform uses the AWS provider credential chain to authenticate to AWS.
- Explicitly selecting `AWS_PROFILE=security-lab` resolved an initial authentication error.
- Terraform plans can be reviewed before infrastructure is created.
- Security controls should be verified using negative and positive tests rather than relying solely on configuration inspection.

### Next Actions

- Perform a SigV4-signed request using an authorised IAM identity.
- Verify create/read operations against DynamoDB.
- Review CloudWatch application logs.
- Examine IAM policy scope and API Gateway routes.
- Document cost controls and environment teardown.
