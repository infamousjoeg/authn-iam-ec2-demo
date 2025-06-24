# AuthN IAM EC2 Demo

This repository contains a minimal example showing how an EC2 instance can authenticate to Conjur Cloud using the **Conjur AWS IAM Client for Python** and then retrieve a secret.  The repository includes a small Python script and sample policy files.

## Prerequisites

- Python 3.10 or later
- Access to Conjur Cloud with the IAM authenticator enabled
- An EC2 instance or environment with AWS IAM credentials

## Installation

1. Clone this repository.
2. Install the Python dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

   The packages `conjur-client` and `conjur-iam-client` are required in addition to standard HTTP libraries.

## Configuration

The demo script reads the following environment variables.  Default values were removed so these must be defined before running the script.

- `CONJUR_APPLIANCE_URL` – URL of the Conjur appliance or Conjur Cloud instance
- `AUTHN_IAM_SERVICE_ID` – service ID of the IAM authenticator
- `CONJUR_AUTHN_LOGIN` – Conjur host identity (e.g., `host/aws-ec2/<account-id>/<role-name>`)
- `CONJUR_ACCOUNT` – Conjur account name (usually `conjur`)
- `CONJUR_CERT_FILE` – path to the Conjur SSL certificate when connecting to a
  self‑hosted Conjur instance
- `TARGET` – set to `cloud` when using Conjur Cloud (the default), otherwise
  the script expects `CONJUR_CERT_FILE`
- `CONJUR_SECRET_ID` – identifier of the secret to fetch

Export these variables before running the script, for example:

```bash
export CONJUR_APPLIANCE_URL=https://<subdomain>.secretsmgr.cyberark.cloud
export AUTHN_IAM_SERVICE_ID=aws-prod
export CONJUR_AUTHN_LOGIN=host/data/iam-ec2/111111111111/IAMConjurRole
export CONJUR_ACCOUNT=conjur
export CONJUR_SECRET_ID=aws-ec2/database/password
```

## Running the example

Invoke the script directly once the environment variables are set:

```bash
python3 authn-iam-ec2.py
```

The script will:

1. Generate an AWS signature for IAM authentication.
2. Exchange the signature for a Conjur session token.
3. Instantiate a Conjur client using the environment variables and fetch the
   secret specified by `CONJUR_SECRET_ID`.

## Docker

A simple `Dockerfile` is provided for experimentation.  Build the image with:

```bash
docker build -t authn-iam-demo .
```

Run the container while passing the required environment variables:

```bash
docker run --rm \
  -e CONJUR_APPLIANCE_URL \
  -e AUTHN_IAM_SERVICE_ID \
  -e CONJUR_AUTHN_LOGIN \
  -e CONJUR_ACCOUNT \
  -e CONJUR_SECRET_ID \
  authn-iam-demo
```

The container simply executes `authn-iam-ec2.py` and then exits.

## Policy Examples

The `policies/` directory contains example Conjur policies that define an IAM authenticator service and an EC2 host identity.  These policies must be loaded into Conjur prior to running the demo so that the host has permission to read the desired secret.

## Limitations

This sample is intended for demonstration purposes only.  The Conjur AWS IAM Client for Python does not currently support updating or deleting secrets, and the obtained session token is valid for only a few minutes.

