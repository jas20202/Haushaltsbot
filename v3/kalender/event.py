import uuid 

class Event:
    def __init__(self, date, event_name, event_info, author, entry_date):
        self.id = uuid.uuid1()
        self.date = date
        self.event_name = event_name
        self.event_info = event_info
        self.author = author
        self.entry_date = entry_date