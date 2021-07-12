import requests
response = requests.get("https://192.168.200.208", verify=False)
print (response.status_code)
