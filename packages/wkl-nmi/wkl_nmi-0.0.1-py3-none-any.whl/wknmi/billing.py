import requests 

class Billing():
    def __init__(self, apikey, url, org):
        self.apikey = apikey
        self.url = url
        self.org = org

    def add(self, body):
        """add billing id """
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.post(f'{self.url}/billing/add', headers=headers, json=body)
        return {"response": response.json(), "status_code": response.status_code}
    
    def update_billing_info(self, body):
        """update billing id """
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.put(f'{self.url}/billing/update-billing-info', headers=headers, json=body)
        return {"response": response.json(), "status_code": response.status_code}
        
    def delete(self, org, user_id, billing_id):
        """delete billing id """
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.delete(f'{self.url}/billing/delete?org={org}&user_id={user_id}&billing_id={billing_id}', headers=headers)
        return {"response": response.json(), "status_code": response.status_code}
    
    def set_priority(self, body):
        """change billing id priority"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.put(f'{self.url}/billing/change-priority', headers=headers, json=body)
        return {"response": response.json(), "status_code": response.status_code}
    

    def info(self, org, user_id):
        """get billing info"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.get(f'{self.url}/billing/billing-of-user?org={org}&user_id={user_id}', headers=headers)
        return {"response": response.json(), "status_code": response.status_code}