import json
import logging
import os
import ssl
import time
import urllib.parse
import urllib.request
import urllib.response
from datetime import datetime
from typing import Dict
 
# configure logging parameters
debug = os.environ.get("DEBUG")
logging_level = logging.DEBUG if debug else logging.INFO
request_debuglevel = 5 if debug else 0
 
 
# configure logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
 
# configure request handler
request_context = ssl._create_unverified_context()
request_handler = urllib.request.HTTPSHandler(
    context=request_context, debuglevel=request_debuglevel
)
 
 
def build_patch_payload(annotations: Dict) -> Dict:
    return json.dumps(
        {"spec": {"template": {"metadata": {"annotations": annotations}}}}
    )
 
 
def build_patch_body(annotations: Dict) -> Dict:
    return json.dumps(
        {"spec": {"template": {"metadata": {"annotations": annotations}}}}
    )
 
 
def patch_coredns_service(url: str, headers: Dict[str, str], data: str) -> None:
    request = urllib.request.Request(
        url, headers=headers, data=bytes(data.encode("utf-8")), method="PATCH"
    )
    opener = urllib.request.build_opener(request_handler)
    with opener.open(request) as response:
        return response.read().decode()
 
def fix(endpoint, token, stepback):
    url = f"{endpoint}/apis/apps/v1/namespaces/kube-system/deployments/coredns"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/strategic-merge-patch+json",
    }
    
    logger.error("Waiting stepback for: %s", stepback)
    time.sleep(stepback)

    try:
        patch_payload = build_patch_payload(
            {"$patch": "delete", "eks.amazonaws.com/compute-type": "ec2"}
        )
        logging.info("Patch Request: %s", patch_payload)
        patch_response = patch_coredns_service(url, headers, patch_payload)
        logging.info("Patch Response: %s", patch_response)
 
        restart_payload = build_patch_body(
            {"kubectl.kubernetes.io/restartedAt": datetime.utcnow().isoformat()}
        )
        logging.info("Restart Request: %s", restart_payload)
        restart_response = patch_coredns_service(url, headers, restart_payload)
        logging.info("Restart Response: %s", restart_response)
    except urllib.error.HTTPError as e:
        logger.error("Request Error: %s", e)
        fix(endpoint, token, stepback * 2)


def handler(event, _):
    logger.info(event)
 
    token = event.get("token")
    endpoint = event.get("endpoint")

    fix(endpoint, token, 5)