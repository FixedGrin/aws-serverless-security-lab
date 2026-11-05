# Architecture and security rationale

```text
AWS IAM authenticated client (SigV4)
               |
       API Gateway HTTP API
      AWS_IAM authentication
               |
         Python Lambda
          /        \
 DynamoDB table    CloudWatch Logs
 (on-demand, PITR) (14-day retention)
```

## Initial controls

- IAM authorisation on every route, including health. An IAM principal also needs `execute-api:Invoke` permissions for the API ARN.
- Lambda execution role permits only GetItem/PutItem for the specific DynamoDB table and log writes to the specific Lambda log group.
- API stage has basic throttling. DynamoDB PITR helps recover accidental deletion (additional cost).
- No long-lived credentials, secrets or AWS access in CI.

## Threats and next milestones

| Threat | Current control | Future verification |
|---|---|---|
| Unauthenticated client | AWS_IAM on API routes | Verify unsigned request fails with 403 |
| Excessive IAM access | Narrow Lambda actions/resources | Test Deny and least privilege |
| Unexpected cost | Throttling, manual deployment | Configure AWS Budgets and teardown |
| Data loss | DynamoDB PITR | Restoration drill |
| Supply chain issues | Basic Python tests | Add dependency and IaC scanning |
| Undetected abuse | Lambda logging | Add alarms, metrics and dashboards |

## Constraints

Not production-ready or deployed. Real AWS usage may incur charges. Initial Terraform backend is local for learning; never commit state. Add secure remote backend and state locking before team/CI deployments. Do not store work/customer data.
