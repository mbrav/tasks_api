import pytest


@pytest.fixture
def app():
    from fastapi import FastAPI
    return FastAPI()


@pytest.fixture
def client(app):
    from fastapi.testclient import TestClient
    return TestClient(app)
