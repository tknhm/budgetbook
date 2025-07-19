import json
from flask import Response


def json_response(data, status=200):
    """日本語対応のJSONレスポンス"""
    return Response(
        json.dumps(data, ensure_ascii=False), status=status, mimetype="application/json"
    )
