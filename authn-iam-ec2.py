#!/usr/bin/env python3
"""Example EC2 script using the Conjur AWS IAM Client for Python."""

import os
from conjur_iam_client import (
    create_conjur_iam_api_key,
    get_conjur_iam_session_token,
    create_conjur_iam_client,
)

# Configuration values can be provided through environment variables
APPLIANCE_URL = os.getenv("CONJUR_APPLIANCE_URL", "https://dap.joegarcia.dev")
SERVICE_ID = os.getenv("AUTHN_IAM_SERVICE_ID", "prod")
USERNAME = os.getenv("CONJUR_AUTHN_LOGIN", "host/aws-ec2/735280068473/ConjurAWSRoleEC2")
ACCOUNT = os.getenv("CONJUR_ACCOUNT", "cyberarkdemo")
# Conjur Cloud does not require a certificate file.  Leave CONJUR_CERT_FILE
# unset unless communicating with a self-hosted Conjur instance.
CERT_FILE = os.getenv("CONJUR_CERT_FILE")
SECRET_ID = os.getenv("CONJUR_SECRET_ID", "aws-ec2/database/password")

# 1- Create the AWS signature header used for IAM authentication
api_key = create_conjur_iam_api_key()
print(api_key)

# 2- Exchange the signature for a Conjur session token
session_token = get_conjur_iam_session_token(
    APPLIANCE_URL, ACCOUNT, SERVICE_ID, USERNAME, CERT_FILE
)
print(session_token)

# 3- Instantiate the Conjur client and retrieve a secret
conjur = create_conjur_iam_client(
    APPLIANCE_URL, ACCOUNT, SERVICE_ID, USERNAME, CERT_FILE
)
secret_value = conjur.get(SECRET_ID)
print("Password: " + secret_value)

