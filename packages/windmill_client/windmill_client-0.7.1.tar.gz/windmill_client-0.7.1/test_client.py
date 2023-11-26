import os
import time
from types import SimpleNamespace

import pytest

import windmill_client as wmill


@pytest.fixture(scope="session")
def client():
    return wmill.Windmill()


@pytest.fixture
def script():
    return SimpleNamespace(
        path="f/scripts/say_hello",
        hash="eba535ffcbddbe36",
    )


def test_user(client):
    assert client.user


def test_get_workspace(client):
    workspace = wmill.get_workspace()
    assert workspace == os.environ["WM_WORKSPACE"]


def test_run_script_async(client, script):
    job_id = wmill.run_script_async(hash=script.hash)
    assert job_id is not None
    assert isinstance(job_id, str)


def test_run_script_sync(client, script):
    result = wmill.run_script_sync(hash=script.hash)
    assert result is not None


def test_run_script(client, script):
    result = wmill.run_script(script.path)
    assert result is not None


def test_get_job_status(client, script):
    # Start an asynchronous job
    job_id = wmill.run_script_async(hash=script.hash)
    assert job_id is not None
    assert isinstance(job_id, str)
    time.sleep(1)
    # Now check the status of this job
    status = wmill.get_job_status(job_id)
    assert status in ["RUNNING", "WAITING", "COMPLETED"]
