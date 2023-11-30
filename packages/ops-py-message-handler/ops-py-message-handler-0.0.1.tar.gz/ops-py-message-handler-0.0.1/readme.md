# ops-py-message-handler

---

## Description
Post a message to a url (webhook).

Note: In the example code below a Slack Automation Workflow has already been built. The message part of the Slack Workflow has been defined to receive a `Title` and a `Text` variable.

---

## Installation
`pip install ops-py-message-handler`

---

## Usage
Export your slack webhook:   
`export WEBHOOK="12345blablabla...."`

Example code:   
```
from message_handler import message_handler as mh

WEBHOOK = os.getenv("WEBHOOK")
heading = "This is the heading"
message = "This is the message"
mh = MessageHandler(WEBHOOK)
mh.set_payload(Title=heading, Text=message)
mh.post_payload()
response_code = mh.get_response_code()
print(response_code)
```
