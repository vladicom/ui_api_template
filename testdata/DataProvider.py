import json

my_file = open('test_data.json')
global_data = json.load(my_file)

class DataProvider:

    def __init__(self) -> None:
        self.data = global_data

    def get(self, prop: str) -> str:
        return self.data.get(prop)
    
    def getint(self, prop: str) -> int:
        return self.data.get(int(prop))
    
    def get_token(self):
        return self.data.get("token")
    
    def login(self):
        return self.data.get("log_path")
    def e_mail(self):
        return self.data.get("email")
    
    def org_id(self):
        return self.data.get("orgID")
    
    def password(self):
        return self.data.get("password")