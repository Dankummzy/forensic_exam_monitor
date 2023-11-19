import json
from urllib.request import urlopen

url = 'https://jsonplaceholder.typicode.com/posts'  # Example API endpoint

with urlopen(url) as response:
    source = response.read()

data = json.loads(source)

print(json.dumps(data, indent=2))
