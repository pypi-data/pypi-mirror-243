import json, warnings, uuid, os

class User:
    def __init__(self, useruuid : str, file: str):
        jsonobj = json.load(open(f'{file}.json'))
        self.userid = useruuid
        self.username = None
        self.password = None
        self.email = None
        for all in jsonobj:
            if all['uuid'] == self.userid:
                self.username = all['user'][0]
        for all in jsonobj:
            if all['uuid'] == self.userid:
                self.password = all['user'][1]
        for all in jsonobj:
            if all['uuid'] == self.userid:
                self.username = all['user'][0]
        for all in jsonobj:
            if all['uuid'] == self.userid:
                self.email = all['email']

class SetUser:
    def __init__(self, name : str, password : str, email : str, file: str):
        self.nm = name
        self.pasw = password
        self.em = email
        self.fl = file
    def create(self):
        """Codes: 200='Username Taken' 202='Success!'"""
        loaded = json.load(open(f'{self.fl}.json'))
        for all in loaded:
            if all['user'][0] == self.nm:
                return [200 ,False, {}]
        uuid_oft = uuid.uuid4()
        loaded.append({"uuid": str(uuid_oft), "user": [self.nm, self.pasw], 'email': self.em})
        with open(f'{self.fl}.json', 'w') as f:
            json.dump(loaded, f)
        return [202, True, {"uuid": str(uuid_oft), "user": [self.nm, self.pasw], 'email': self.em}]