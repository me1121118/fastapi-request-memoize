import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_request_memoize import request_memoize, RequestMemoizeMiddleware

def test_request_memoize():
    app = FastAPI()
    app.add_middleware(RequestMemoizeMiddleware)

    call_count = 0

    @request_memoize
    def expensive_lookup(key: str):
        nonlocal call_count
        call_count += 1
        return f"result_for_{key}"

    @app.get("/compute")
    def compute():
        res1 = expensive_lookup("foo")
        res2 = expensive_lookup("foo")
        res3 = expensive_lookup("bar")
        return {"res1": res1, "res2": res2, "res3": res3}

    client = TestClient(app)
    client.get("/compute")

    # expensive_lookup("foo") was called twice in route, but only computed once!
    # expensive_lookup("bar") was computed once.
    # Total executions: 2
    assert call_count == 2
