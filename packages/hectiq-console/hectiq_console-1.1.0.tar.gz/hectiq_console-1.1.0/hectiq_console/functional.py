from hectiq_console import CONSOLE_APP_URL

import os
import contextvars 
import requests
import time
from typing import Optional, Union, List
from contextlib import contextmanager

import logging
logger = logging.getLogger(__name__)

ressource_cvar = contextvars.ContextVar("ressource_id", default=None) 

def set_ressource(ressource: str):
    ressource_cvar.set(ressource)

def get_ressource(ressource: Optional[str] = None) -> Optional[str]:
    """Get a ressource from the Hectiq Console.

    Args:
        ressource (Optional[str], optional): Ressource ID of the ressource to get. Defaults to None.

    Returns:
        dict: Ressource object
    """
    if ressource is None:
        ressource = ressource_cvar.get()
    if ressource is None:
        raise ValueError("You must provide a ressource ID to the get_ressource method or use `set_ressource`.")
    return ressource

def create_incident(title: str, 
                    description: Optional[str] = None,
                    filenames: Optional[List] = None, 
                    ressource: Optional[str] = None):
    """Create an incident in the Hectiq Console.

    Args:
        title (str): Title of the incident
        description (Optional[str], optional): Description of the incident. Defaults to None.
        ressource (Optional[str], optional): Ressource ID of the ressource to which the incident is related. 
            Defaults to None.
    """
    ressource = get_ressource(ressource)
    body = {"name": title, "description": description}
    if filenames is not None:
        body["files"] = []
        for filename in filenames:
            assert os.path.exists(filename), f"File {filename} does not exist."
            name = os.path.basename(filename)
            num_bytes = os.path.getsize(filename)
            extension = os.path.splitext(filename)[1].replace(".", "")
            body["files"].append({"name": name, "num_bytes": num_bytes, "extension": extension})
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{ressource}/incidents", 
                 json=body)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while creating the incident with hectiq_console.create_incident: {res.text}")
        return
    
    # Upload the files
    if filenames is not None:
        from hectiq_console.upload import upload_file
        for filename, policy in zip(filenames, res.json()["policies"]):
            upload_file(filepath=filename, policy=policy)

def add_file(filename: str,
             ressource: Optional[str] = None):
    """Add a file to a ressource in the Hectiq Console.

    Args:
        filename (str): Name of the file
        ressource (Optional[str], optional): Ressource ID of the ressource to which the file is related. 
            Defaults to None.
    """
    from hectiq_console.upload import upload_file
    ressource = get_ressource(ressource)

    assert os.path.exists(filename), f"File {filename} does not exist."
    name = os.path.basename(filename)
    num_bytes = os.path.getsize(filename)
    extension = os.path.splitext(filename)[1].replace(".", "")
    json = {"name": name, "num_bytes": num_bytes, "extension": extension}
    res = requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{ressource}/files", json=json)
    if res.status_code != 200:
        logger.error(f"⚠️ Error while creating the file with hectiq_console.add_file: {res.text}")
        return
    try:
        policy = res.json()
    except:
        logger.error(f"⚠️ Error while creating the file with hectiq_console.add_file: {res.text}")
        return
    upload_file(filepath=filename, policy=policy)

def add_metrics(name: str, 
                value: Union[float, int], 
                ressource: Optional[str] = None):
    """Add metrics to the Hectiq Console.

    Args:
        key (str): Key of the metrics
        value (Union[float, int]): Value of the metrics
        ressource (Optional[str], optional): Ressource ID of the ressource to which the metrics are related. 
            Defaults to None.
    """
    ressource = get_ressource(ressource)
    body = {
        "metrics" : [{"name": name, "value": value}]
    }
    requests.post(f"{CONSOLE_APP_URL}/app/sender-client/{ressource}/metrics", 
                 json=body)
    
@contextmanager
def timer_context(name: str, 
                  ressource: Optional[str] = None):
    """Context manager to time a block of code.

    Args:
        key (str): Key of the timer
        ressource (Optional[str], optional): Ressource ID of the ressource to which the timer is related. 
            Defaults to None.
    """
    start = time.time()
    yield
    end = time.time()
    duration = end - start
    add_metrics(name=name, value=duration, ressource=ressource)
