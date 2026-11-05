output "api_base_url" {
  description = "Requires an IAM principal authorised to invoke the API and SigV4 signing."
  value       = aws_apigatewayv2_api.http.api_endpoint
}
output "table_name" {
  value = aws_dynamodb_table.items.name
}
