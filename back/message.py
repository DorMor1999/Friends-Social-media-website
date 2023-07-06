class Message:

    def __init__(self, id, writer_user, get_user, date, observed, chat_id, text):
        self.id = id
        self.writer_user = writer_user
        self.get_user = get_user
        self.date = {"date": date.split(" | ")[0], "time": date.split(" | ")[1]}
        if observed == "false":
            self.observed = False
        else:
            self.observed = True
        self.chat_id = chat_id
        self.text = text