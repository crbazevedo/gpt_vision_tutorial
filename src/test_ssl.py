import httpx

response = httpx.get('https://www.google.com', verify=True)
print(response.status_code)
