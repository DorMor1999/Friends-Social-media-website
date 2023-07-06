import sqlite3


class Activity:

    def __init__(self, id, writer_user, date):
        self.id = id
        self.writer_user = writer_user
        self.date = date


    def get_likes(self, post_id, comment_id):
        from back.like import Like
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        query = f"SELECT rowid, * FROM likes WHERE post_id = ? AND comment_id = ?"
        cursor.execute(query, (post_id, comment_id))
        likes_data = cursor.fetchall()
        likes_list = []
        if likes_data != []:
            for like in likes_data:
                new_like = Like(like[0], self.writer_user.get_user_by_mail(like[1]), like[2], like[3], like[4])
                likes_list.append(new_like)
        all_likes = {"quantity": len(likes_data), "likes_list": likes_list}
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return all_likes


    def get_tags_from_post_and_comment(self, post_id, comment_id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        all_tags_users = []
        query = f"SELECT rowid, * FROM tags WHERE post_id = ? AND comment_id =?"
        cursor.execute(query, (post_id, comment_id))
        all_tags = cursor.fetchall()
        if all_tags != []:
            for tag in all_tags:
                tag_user = self.writer_user.get_user_by_mail(tag[1])
                all_tags_users.append(tag_user)
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return all_tags_users
