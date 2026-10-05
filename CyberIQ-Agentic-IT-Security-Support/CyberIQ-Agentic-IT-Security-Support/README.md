# CyberIQ – Agentic IT & Security Support

CyberIQ is an agentic IT and security support MVP for the **AWS Communications Developer Services (CDS) Agentic AI Partner Hackathon**.

It accepts an IT/security request, routes it to specialized agents, uses Amazon Bedrock when configured, and can return the response through **AWS End User Messaging RCS**.

## Architecture

```text
User
  |
  v
AWS End User Messaging RCS
  |
  v
Inbound adapter / API
  |
  v
CyberIQ Router
  |------------------|
  v                  v
Network Agent     Security Agent
  |                  |
  +---------> Amazon Bedrock
                     |
                     v
              Response / Escalation
                     |
                     v
             AWS End User Messaging RCS
```

### Example

> My VPN is not connecting and I received a suspicious login alert.

CyberIQ identifies **network + security** intents, invokes the appropriate specialized agents, marks the request as high risk, and produces a combined response with security escalation guidance.

## AWS services used

- AWS End User Messaging RCS
- Pinpoint SMS and Voice v2 API (`pinpoint-sms-voice-v2`) for outbound text/RCS
- Amazon Bedrock Runtime (`converse`) for intent routing and agent responses
- FastAPI for the application layer

## Important: real AWS RCS usage

This repository is designed for real AWS integration. It does **not** claim that an RCS message was sent unless the AWS API call succeeds.

AWS documents that `SendTextMessage` can route a text message over RCS when the origination identity is an AWS RCS Agent ARN. A phone pool can also be used when SMS fallback is desired.

## 1. Local setup

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Load the environment variables in your shell or use a dotenv loader of your choice. The application intentionally does not read `.env` automatically so secrets are not silently loaded in production.

## 2. Configure AWS

Configure AWS credentials using your normal AWS CLI/SDK method:

```bash
aws configure
aws sts get-caller-identity
```

The IAM principal running CyberIQ needs permission to invoke the required Bedrock model and send messages through AWS End User Messaging.

## 3. Configure RCS

In AWS End User Messaging:

1. Create an **AWS RCS Agent**.
2. Submit a testing registration.
3. Add a test device and accept the tester invitation.
4. Copy the AWS RCS Agent ARN into `RCS_ORIGINATION_IDENTITY`.

Then test the service:

```bash
uvicorn backend.app:app --reload --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## 4. Test routing locally

```bash
curl -X POST http://127.0.0.1:8000/support ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"My VPN is not connecting and I received a suspicious login alert\"}"
```

On macOS/Linux, use the same request with `\` line continuations.

## 5. Send a real RCS response

```bash
curl -X POST http://127.0.0.1:8000/support \
  -H "Content-Type: application/json" \
  -d '{"message":"My VPN is not connecting","destination_phone_number":"+91XXXXXXXXXX","send_response":true}'
```

The `send_response=true` path calls AWS `SendTextMessage` through boto3. If the call fails, the API returns an error rather than pretending delivery occurred.

## 6. Inbound RCS production path

AWS End User Messaging can publish inbound RCS messages to an Amazon SNS topic. A Lambda function or HTTPS subscriber can normalize the SNS payload and call `/webhook/rcs`.

For a hackathon demo, the simplest production-like flow is:

```text
RCS test device
   -> AWS End User Messaging
   -> SNS
   -> Lambda / adapter
   -> CyberIQ router
   -> specialized agent
   -> Bedrock
   -> SendTextMessage
   -> RCS test device
```

## Environment variables

| Variable | Purpose |
|---|---|
| `AWS_REGION` | AWS region used by the SDK |
| `RCS_ORIGINATION_IDENTITY` | RCS Agent ARN or configured pool ID |
| `RCS_MESSAGE_TYPE` | Usually `TRANSACTIONAL` for support messages |
| `USE_BEDROCK` | Enable/disable Bedrock |
| `BEDROCK_MODEL_ID` | Model ID accessible to your AWS account |
| `LOG_LEVEL` | Python logging level |

## Safety and demo behavior

CyberIQ is an IT/security support assistant, not an autonomous incident-remediation engine. It does not request passwords, MFA codes, or other secrets. Security alerts are treated conservatively and can be marked for SOC review.

If Bedrock is not configured, the router and agents use a clearly defined local fallback so the application can still be tested. For the final hackathon demo, configure Bedrock and real RCS so the end-to-end AWS path is visible.

## Next implementation steps

- Add SNS signature validation and an AWS Lambda inbound adapter.
- Add CloudWatch structured logging and metrics.
- Add a knowledge base/tool layer for approved troubleshooting actions.
- Add a human escalation queue for high-risk incidents.
- Add a demo UI or message transcript for the submission video.
