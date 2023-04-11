#!/usr/bin/env python3

import os, boto3, base64, json, requests
import urllib.parse
from signer import headers_for_signed_url

# Create session and get credentials from AWS IMDS
session = boto3.Session()
credentials = session.get_credentials()

# Get signed AWSv4 headers from STS GetCallerID Function
# NOTE: region must remain us-east-1 because Conjur is hard-coded
# to verify signed headers against that region's STS service
signed_headers = headers_for_signed_url(credentials.access_key, 
    credentials.secret_key, 
    credentials.token,
    'us-east-1')

# Declare and init Conjur variables
conjur_url = "https://dap.joegarcia.dev"
conjur_acct = 'cyberarkdemo'
conjur_service_id = "prod"
secretID = "aws-ec2/database/password"
host = "host/aws-ec2/735280068473/ConjurAWSRoleEC2"
cert = "/path/to/conjur.pem" # Can also be a boolean value: True or False

# Get authentication token by providing AWSv4 signature,
# Conjur will validate the signature against AWS
authenticate_url = "{conjur_appliance_url}/authn-iam/{conjur_service_id}/{account}/{host}/authenticate".format(
                        conjur_appliance_url = conjur_url,
                        conjur_service_id = conjur_service_id,
                        account = conjur_acct,
                        host = urllib.parse.quote_plus(host)
                    )
print("Authenticate URL: {}".format(authenticate_url))
authResponse = requests.post(authenticate_url, data=signed_headers, verify=cert)
print("Authentication Response: " + str(authResponse.status_code))
# Convert auth token to base64
token_b64 = base64.b64encode(authResponse.text.encode('utf-8')).decode("utf-8")

# Now we can retrieve secrets until our heart's content
retrieve_variable_url = "{conjur_appliance_url}/secrets/{account}/variable/".format(
                            conjur_appliance_url = conjur_url,
                            account = conjur_acct
                            )
password = requests.get(retrieve_variable_url + secretID,
                    headers={'Authorization' : "Token token=\"" + token_b64 + "\""}, verify=cert).text

result = 'Password:' + password
print(result)
