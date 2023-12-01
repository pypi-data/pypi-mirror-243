import requests 


class Plans():
    def __init__(self, apikey, url, org):
        self.apikey = apikey
        self.url = url
        self.org = org

    def all(self):
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.get(f'{self.url}/plans/all-plans?org={self.org}', headers=headers)
        return response.json()
    

    def id(self, id):
        headers = {'Authorization': 'Bearer ' + self.apikey}
        response = requests.get(f'{self.url}/plans/plan-id/{id}?org={self.org}', headers=headers)
        return response.json()
    

    def add_month_configuration(self, body):
        headers = {'Authorization': 'Bearer ' + self.apikey}
        body['org'] = self.org
        response = requests.post(f'{self.url}/plans/month-frequency-config', headers=headers, json=body)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}
        

    def edit_month_configuration(self, body):
        headers = {'Authorization': 'Bearer ' + self.apikey}
        body['org'] = self.org
        response = requests.put(f'{self.url}/plans/edit-month-frequency-config', headers=headers, json=body)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}


    def add_day_configuration(self, body):
        headers = {'Authorization': 'Bearer ' + self.apikey}
        body['org'] = self.org
        response = requests.post(f'{self.url}/plans/day-frequency-config', headers=headers, json=body)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}
        

    def edit_day_configuration(self, body):
        headers = {'Authorization': 'Bearer ' + self.apikey}
        body['org'] = self.org
        response = requests.put(f'{self.url}/plans/edit-day-frequency-config', headers=headers, json=body)
        if (response.status_code == 200):
            return {"response":response.json(), "status_code":response.status_code}
        else:
            return {"response":response.json(), "status_code":response.status_code}
        
