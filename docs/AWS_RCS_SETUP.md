# AWS RCS setup checklist

Use the current AWS End User Messaging RCS setup guide for the console flow.

1. Open AWS End User Messaging.
2. Go to **Configurations → RCS agents**.
3. Create an AWS RCS Agent.
4. Complete the testing registration.
5. Add a test device and accept the tester invitation.
6. Copy the RCS Agent ARN.
7. Set it as `RCS_ORIGINATION_IDENTITY`.
8. Start CyberIQ and test `/support` with `send_response=true`.

For inbound messages, configure two-way RCS messaging to publish to SNS and connect SNS to Lambda/HTTPS. The adapter should normalize the inbound event before calling CyberIQ's `/webhook/rcs` endpoint.
