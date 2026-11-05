import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.handler import lambda_handler


def test_health():
    result = lambda_handler({"routeKey": "GET /health"}, None)
    assert result["statusCode"] == 200
    assert json.loads(result["body"])["status"] == "ok"


def test_unknown_route():
    assert lambda_handler({"routeKey": "DELETE /items"}, None)["statusCode"] == 404


def test_create_and_get(monkeypatch):
    monkeypatch.setenv("TABLE_NAME", "test-items")
    table = MagicMock()
    table.get_item.return_value = {"Item": {"id": "abc", "name": "Example"}}
    resource = MagicMock()
    resource.Table.return_value = table
    monkeypatch.setitem(sys.modules, "boto3", SimpleNamespace(resource=lambda _: resource))
    created = lambda_handler({"routeKey": "POST /items", "body": '{"name":"Example"}'}, None)
    assert created["statusCode"] == 201
    table.put_item.assert_called_once()
    retrieved = lambda_handler({"routeKey": "GET /items/{id}", "pathParameters": {"id": "abc"}}, None)
    assert json.loads(retrieved["body"])["name"] == "Example"


def test_invalid_payload(monkeypatch):
    monkeypatch.setenv("TABLE_NAME", "test-items")
    monkeypatch.setitem(sys.modules, "boto3", SimpleNamespace(resource=lambda _: MagicMock()))
    result = lambda_handler({"routeKey": "POST /items", "body": "{"}, None)
    assert result["statusCode"] == 400
