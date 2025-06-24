#!/usr/bin/env python3
"""Example EC2 script using the Conjur AWS IAM Client for Python."""

import os
from conjur_iam_client import (
    create_conjur_iam_api_key,
    get_conjur_iam_session_token,
    create_conjur_iam_client_from_env,
)

# Read required configuration from the environment
APPLIANCE_URL = os.environ["CONJUR_APPLIANCE_URL"]
# Ensure the appliance URL ends with /api as required for Conjur Cloud
if not APPLIANCE_URL.rstrip("/").endswith("api"):
    APPLIANCE_URL = APPLIANCE_URL.rstrip("/") + "/api"
SERVICE_ID = os.environ["AUTHN_IAM_SERVICE_ID"]
USERNAME = os.environ["CONJUR_AUTHN_LOGIN"]
ACCOUNT = os.environ["CONJUR_ACCOUNT"]
SECRET_ID = os.environ["CONJUR_SECRET_ID"]

# Use a certificate only when connecting to a self-hosted Conjur instance.
# If CONJUR_CERT_FILE is not set, we assume Conjur Cloud and skip certificate verification.
CERT_FILE = os.getenv("CONJUR_CERT_FILE") or None

# 1- Create the AWS signature header used for IAM authentication
api_key = create_conjur_iam_api_key()
print(api_key)

# 2- Exchange the signature for a Conjur session token
session_token = get_conjur_iam_session_token(
    APPLIANCE_URL, ACCOUNT, SERVICE_ID, USERNAME, CERT_FILE
)
print(session_token)

# 3- Instantiate the Conjur client from environment variables
conjur = create_conjur_iam_client_from_env()
secret_value = conjur.get(SECRET_ID)
print("Password: " + secret_value)

