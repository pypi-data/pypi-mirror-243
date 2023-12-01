import requests 


class Subscriptions():
    def __init__(self, apikey, url, org):
        self.apikey = apikey
        self.url = url
        self.org = org
    
    def get_subscriptions(self):
        """Get all subscriptions"""
        url = self.url + '/subscriptions'
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.get(url, headers=headers)
        return response.json()
    
    
    def add_with_custom_month_frequency_config(self, body):
        """Add a subscription with custom month frequency config"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        body['org'] = self.org
        response = requests.post(f'{self.url}/subscriptions/month-frequency-config', headers=headers, json=body)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}
    
    def add_with_custom_day_frequency_config(self, body):
        """Add a subscription with custom day frequency config"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        body['org'] = self.org
        response = requests.post(f'{self.url}/subscriptions/day-frequency-config', headers=headers, json=body)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}


    def pause(self, subscription_id, pause):
        """Pause a subscription"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.put(f'{self.url}/subscriptions/pause?org={self.org}&subscription_id={subscription_id}&pause={pause}', headers=headers)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}
        

    def cancel(self, subscription_id):
        """Pause a subscription"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.delete(f'{self.url}/subscriptions/cancel-subscription?org={self.org}&subscription_id={subscription_id}', headers=headers)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}
    

    def by_user_id(self, user_id):
        """Get subscriptions by user id"""
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.get(f'{self.url}/subscriptions/by-user-id?org={self.org}&user_id={user_id}', headers=headers)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}


