import requests
import base64

with open("test.png", "rb") as f:
    image = base64.b64encode(f.read()).decode('utf-8')

data = {
    "distance":35,
    "image":image
}

r = requests.post('http://127.0.0.1:5001/alert/email',json=data)

print(r)
print(r.content)

