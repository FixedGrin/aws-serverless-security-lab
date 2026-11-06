# AWS Serverless Security Lab

A personal **cloud security engineering portfolio project** exploring AWS, Terraform, IAM and secure delivery. This is Option A from the November 2026–January 2027 roadmap.

**Status: Initial AWS deployment completed — 6 November 2026**

The first version of the serverless architecture has been provisioned in AWS Sydney (`ap-southeast-2`) using Terraform.

**Completed:**

- Terraform initialised and configuration validated.
- Deployment plan reviewed: 12 resources to create.
- Initial infrastructure deployment completed.
- API Gateway endpoint provisioned.
- DynamoDB table provisioned.
- Unauthenticated API request rejected with HTTP `403 Forbidden`, as intended.

**Next milestones:**

- Verify and document successful IAM-authorised API requests.
- Test creating and retrieving DynamoDB items.
- Inspect CloudWatch logs and investigate how application activity is recorded.
- Review Lambda execution-role permissions and API Gateway authorisation.
- Introduce infrastructure security checks and automated testing.

This is an educational cloud security engineering project, not a production-ready application.

## Architecture

```text
AWS IAM client (SigV4)
        |
API Gateway HTTP API (AWS_IAM)
        |
Python Lambda (3.12) ----> DynamoDB (on-demand, PITR)
        |
CloudWatch Logs (14 days)
```

Details and threat model: [docs/architecture.md](docs/architecture.md).

## Project layout

- `app/handler.py`: create/read items and a health endpoint.
- `tests/test_handler.py`: unit tests without an AWS account.
- `infra/terraform/`: AWS resources managed through Terraform.
- `.github/workflows/tests.yml`: tests only; no deployment or cloud credentials.
- `docs/`: architecture and control rationale.

## Test locally

Install Python 3.12+ and run:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Deploy intentionally (not automatic)

Requires a personal AWS account, Terraform >= 1.6, an authenticated AWS profile and appropriate provisioning permissions. **AWS resources can incur costs.** Configure billing alerts first.

```bash
cd infra/terraform
terraform init
terraform fmt -check
terraform validate
terraform plan -out=local.tfplan
# Review the plan carefully:
terraform apply local.tfplan
terraform output
```

All API routes are protected with AWS IAM authorisation. An unsigned HTTP call is **expected to fail**. To test successful calls, provision an authorised client principal with narrowly scoped `execute-api:Invoke`, and send a properly SigV4-signed request.

After your exercise:

```bash
terraform destroy
```

Verify resources and billing in the AWS console. For this first lab, Terraform state is local and ignored by Git; keep it secure. Use remote state with locking before collaborating or automating deployment.

## Quarter-one checklist

- [ ] Month 1: run tests; learn Terraform init/plan/apply/destroy; review resource costs and least privilege.
- [ ] Month 2: prove authorised and unauthorised API behaviour; introduce secure CI and IaC checks.
- [ ] Month 3: add monitoring, failure tests, design review and an engineering retrospective.

Evidence matters: retain design decisions, meaningful tests and review feedback, not credentials or confidential screenshots.

## Licence

MIT. Existing GitHub `LICENSE` file remains authoritative.
