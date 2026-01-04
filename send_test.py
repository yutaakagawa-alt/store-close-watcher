import os

token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

print("TOKEN EXISTS:", token is not None)
print("TOKEN LENGTH:", len(token) if token else 0)
