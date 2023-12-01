import requests 

class Config():
    def __init__(self, apikey, url, org):
        self.apikey = apikey
        self.url = url
        self.org = org

    def get(self):
        """Get client by id"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.get(f'{self.url}/configs/get-config?org={self.org}', headers=headers)
        return response.json()
    
    
    def update(self, body):
        """Update client by id"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.put(f'{self.url}/configs/update-config?org={self.org}', headers=headers, json=body)
        return response.json()
    
    def add(self, body):
        """Add new client"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.post(f'{self.url}/configs/add-config', headers=headers, json=body)
        return response.json()

    
    def delete(self, org):
        """Delete client by id"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.delete(f'{self.url}/configs/delete-config?org={org}', headers=headers)
        return response.json()