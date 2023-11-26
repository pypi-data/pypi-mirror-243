# Simple Mail Sender
A simple mail sender.

## Usage
```python
from simplemailsender.simplemailsender import SimpleMailSender

sms = SimpleMailSender("<SMTP Server>", "<SMTP Port>", "<SSL or TLS>", "<User>", "<Password>")

sms.send(
    "<Sender e-mail>",
    ["<Recipients e-mail>"],
    "<Subject>",
    "<Message body>",
    "<Path to attachment>"
)