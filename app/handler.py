"""AWS Lambda HTTP API handler: signed endpoints, basic item storage."""
import json
import os
from uuid import uuid4


def respond(code, payload):
    return {"statusCode": code, "headers": {"content-type": "application/json"}, "body": json.dumps(payload)}


def lambda_handler(event, context):
    route = event.get("routeKey")
    if route == "GET /health":
        return respond(200, {"status": "ok"})
    if route not in ("GET /items/{id}", "POST /items"):
        return respond(404, {"error": "Not found"})
    if not os.environ.get("TABLE_NAME"):
        return respond(500, {"error": "Configuration error"})
    import boto3
    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    if route == "POST /items":
        try:
            data = json.loads(event.get("body") or "{}")
        except (TypeError, ValueError):
            return respond(400, {"error": "Invalid JSON"})
        if not isinstance(data, dict) or not isinstance(data.get("name"), str) or not 1 <= len(data["name"].strip()) <= 100:
            return respond(400, {"error": "name must be a string of 1–100 characters"})
        item = {"id": str(uuid4()), "name": data["name"].strip()}
        table.put_item(Item=item)
        return respond(201, item)
    item_id = (event.get("pathParameters") or {}).get("id", "")
    if not isinstance(item_id, str) or not 1 <= len(item_id) <= 64:
        return respond(400, {"error": "Invalid item id"})
    item = table.get_item(Key={"id": item_id}).get("Item")
    return respond(200, item) if item else respond(404, {"error": "Not found"})
