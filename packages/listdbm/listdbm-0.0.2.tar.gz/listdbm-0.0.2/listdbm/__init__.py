import json, warnings, uuid, os

class User:
    def __init__(self, useruuid : str, file: str):
        self.userid = useruuid
        self.fl = file
    def username(self):
        """Gets The Username Of The Desired User"""
        jsonobj = json.load(open(f'{self.fl}.json', 'r'))
        usernam = None
        for all in jsonobj:
            if all['uuid'] == self.userid:
                usernam = all['user'][0]
        if not usernam:
            warnings.warn("Error: USER NOT FOUND")
            return "Error Finding User"
        return usernam
    def userpass(self, coded = False):
        """Gets The Password(Binary/String) Of The Desired User"""
        jsonobj = json.load(open(f'{self.fl}.json', 'r'))
        userpass = None
        for all in jsonobj:
            if all['uuid'] == self.userid:
                userpass = all['user'][1]
        if not userpass:
            warnings.warn("Error: USER NOT FOUND")
            return "Error Finding User"
        if coded == True:
            return "".join([format(ord(char), '#010b')[2:] for char in userpass])
        return userpass
    def useremail(self):
        """Gets The Email Address Of The Desired User"""
        jsonobj = json.load(open(f'{self.fl}.json', 'r'))
        useremm = None
        for all in jsonobj:
            if all['uuid'] == self.userid:
                useremm = all['email']
        if not useremm:
            warnings.warn("USER NOT FOUND")
            return "Error Finding User"
        return useremm

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