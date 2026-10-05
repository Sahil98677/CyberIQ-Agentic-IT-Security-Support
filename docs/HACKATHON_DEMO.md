# CyberIQ demo script

## 60–90 second demo

1. Show the architecture briefly.
2. Send an RCS message:
   `My VPN is not connecting and I received a suspicious login alert.`
3. Show CyberIQ routing to **Network + Security**.
4. Show the Network Agent troubleshooting VPN connectivity.
5. Show the Security Agent treating the login alert as high risk.
6. Show Bedrock being used for the agent reasoning when configured.
7. Show the response returned through AWS End User Messaging RCS.
8. Point out that high-risk security cases are marked for SOC/human review.

Do not describe simulated delivery as real AWS delivery. Only claim an AWS message was sent when the `SendTextMessage` API call succeeds.
