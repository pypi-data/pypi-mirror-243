# windmill_client

## Overview

`windmill_client` is a Python package designed to interact with the Windmill API. It provides a convenient way to manage jobs, resources, and states within the Windmill environment, offering functionalities like job creation, execution, status tracking, and state management.

It's designed to remain api-compatible with the `wmill` package, but with some added features and a more direct usage
of Windmill's REST API.

## Installation

To install `windmill_client`, run the following command:

```bash
pip install windmill-client
```

## Usage

### Basic Usage

The `wmill` package has several methods at the top-level for the most frequent operations you will need.

The following are some common examples:

```python
import time
import windmill_client as wmill


def main():
    # Get the value of a variable
    wmill.get_variable("u/user/variable_path")
    
    # Run a script synchronously and get the result
    wmill.run_script("f/pathto/script", args={"arg1": "value1"})
    
    # Get the value of a resource
    wmill.get_resource("u/user/resource_path")
    
    # Set the script's state
    wmill.set_state({"ts": time.time()})
    
    # Get the script's state
    wmill.get_state()
```

### Advanced Usage

The `wmill` package also exposes the `Windmill` class, which is the core client for the Windmill platform.

```python
import time
from windmill_client import Windmill

def main():
    client = Windmill(
        # token=...  <- this is optional. otherwise the client will look for the WM_TOKEN env var
    )

    # Get the current version of the client
    client.version

    # Get the current user
    client.user
    
    # Convenience get and post methods exist for https://app.windmill.dev/openapi.html#/
    # these are thin wrappers around the httpx library's get and post methods
    # list worker groups
    client.get("/configs/list_worker_groups")
    # create a group
    client.post(
        f"/w/{client.workspace}/groups/create",
        json={
            "name": "my-group",
            "summary": "my group summary",
        }
    )
    
    # Get and set the state of the script
    now = time.time()
    client.state = {"ts": now}
    assert client.state == {"ts": now}
    
    # Run a job asynchronously
    job_id = client.run_script_async(path="path/to/script")
    # Get its status
    client.get_job_status(job_id)
    # Get its result
    client.get_result(job_id)
```
