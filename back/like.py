from back.activity import Activity


class Like(Activity):

    def __init__(self, id, writer_user, date, post_id, comment_id):
        super().__init__(id, writer_user, date)
        self.comment_id = comment_id
        self.post_id = post_id