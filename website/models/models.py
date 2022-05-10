class Application:
    def __init__(self, data):
        self.company = data['company']
        self.position = data['position']
        self.type = data['type']
        self.date = data['date']
        self.status = data['status']
        self.userID = data['userID']
        try:
            self.url = data['url']
        except Exception:
            print('url does not exist, setting url to default value of 0')
            self.url = 0
        try:
            self.location = data['location']
        except Exception:
            print('location does not exist, setting location to default value of 0')
            self.location = 0
        try:
            self.notes = data['notes']
        except Exception:
            print('notes does not exist, setting notes to default value of 0')
            self.notes = 0


class Skill:
    def __init__(self, data):
        x = eval(data['position'])

        self.skill = data['skill']
        self.position = x['position']
        self.company = x['company']
        self.type = x['type']
        self.posID = x['id']
        try:
            self.userID = data['userID']
        except Exception:
            print('Skills: handling userID')
            self.userID = x['userID']
            