import requests
import json

url = "http://localhost:8080/api/v1/user/create" 

# ข้อมูล input
data = {
    "name": "testing",
    "email": "strinsdasd124334tawrgg@gmail.com"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI3YTY5ZWRlMC05M2YwLTQ1OWEtODJmNC03MGY1ZjMzYTNhNTMifQ.ZMAqIA0I54SnJwq3dr5k_fS7l58y9Wlx9ZKMpCqnPvk"
}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        print("Response:", response.json())
    else:
        print(response.status_code)
        print("Detail:", response.text)

except Exception as e:
    print(e)

# Key เริ่ม = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI3YTY5ZWRlMC05M2YwLTQ1OWEtODJmNC03MGY1ZjMzYTNhNTMifQ.ZMAqIA0I54SnJwq3dr5k_fS7l58y9Wlx9ZKMpCqnPvk
# Key หลัง = eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwMmQ1YmVmNi1kYWZjLTQ5NzUtYmIyMy1jMWQ3ODY0YzYwNWMiLCJpYXQiOjE3NzcxMzI0MTIsImV4cCI6MTc3NzIxODgxMn0._0iexZb5yyD3I3qHdhvV9Byvp3MUL40GH8GVvx_o7Bo