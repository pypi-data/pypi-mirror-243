import requests 

class CustomerVault():
    def __init__(self, apikey, url, org):
        self.apikey = apikey
        self.url = url
        self.org = org

    def add(self, body):
        headers = {'Authorization': 'Bearer ' + self.apikey}
        body['org'] = self.org
        response = requests.post(f'{self.url}/customer-vault/add', headers=headers, json=body)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}