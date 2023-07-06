class Notification:

    def __init__(self, id, user_1_writer, user_2_get, date, post_id, comment_id, notification, observed):
        self.id = id
        self.user_1_writer = user_1_writer
        self.user_2_get = user_2_get
        self.date = date
        self.post_id = post_id
        self.comment_id = comment_id
        self.notification = notification
        if observed == "false":
            self.observed = False
        else:
            self.observed = True
