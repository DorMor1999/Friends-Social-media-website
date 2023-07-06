from back.activity import Activity


class Comment(Activity):

    def __init__(self, id, writer_user, date, text, post_id):
        super().__init__(id, writer_user, date)
        self.tags_users = self.get_tags_from_post_and_comment(post_id, id)
        self.text = text
        self.post_id = post_id
        self.likes = self.get_likes(post_id, id)