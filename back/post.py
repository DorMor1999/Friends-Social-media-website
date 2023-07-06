import shutil
import sqlite3
from datetime import datetime

from back.activity import Activity
from back.comment import Comment
from back.like import Like


class Post(Activity):

    def __init__(self, id, writer_user, date, text, location):
        super().__init__(id, writer_user, date)
        self.tags_users = self.get_tags_from_post_and_comment(id, -1)
        self.text = text
        self.pictures_paths = self.get_pictures_from_post()
        self.location = location
        self.comments = self.get_comments()
        self.likes = self.get_likes(id, -1)


    def delete_comment(self, comment_id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # delete likes from likes table
        cursor.execute('DELETE FROM likes WHERE post_id = ? AND comment_id = ?', (self.id, comment_id,))
        # delete comments from comments table
        cursor.execute('DELETE FROM comments WHERE post_id = ? AND rowid = ?', (self.id, comment_id,))
        # delete tags from tags table
        cursor.execute('DELETE FROM tags WHERE post_id = ? AND comment_id = ?', (self.id, comment_id,))
        # delete notifications from notifications table
        cursor.execute('DELETE FROM notifications WHERE post_id = ? AND comment_id = ?', (self.id, comment_id,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def delete_post(self):
        # delete post test directory
        post_dir = f"front/static/assets/data/posts/post_{self.id}"
        shutil.rmtree(post_dir)
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        #delete post test from posts table
        cursor.execute('DELETE FROM posts WHERE rowid = ?', (self.id,))
        # delete likes from likes table
        cursor.execute('DELETE FROM likes WHERE post_id = ?', (self.id,))
        # delete comments from comments table
        cursor.execute('DELETE FROM comments WHERE post_id = ?', (self.id,))
        # delete tags from tags table
        cursor.execute('DELETE FROM tags WHERE post_id = ?', (self.id,))
        # delete pictures from pictures table
        cursor.execute('DELETE FROM pictures WHERE post_id = ?', (self.id,))
        # delete notifications from notifications table
        cursor.execute('DELETE FROM notifications WHERE post_id = ?', (self.id,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def like_operation(self, comment_id, the_user):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        query = f"SELECT rowid, * FROM likes WHERE writer_email = ? AND post_id = ? AND comment_id = ?"
        cursor.execute(query, (the_user.email, self.id, comment_id))
        check = cursor.fetchone()
        #new like
        if check is None:
            cursor.execute('INSERT INTO likes (writer_email, date, post_id, comment_id) VALUES (?, ?, ?, ?)', (the_user.email, datetime.now().strftime("%d/%m/%Y | %H:%M"), self.id, comment_id))
            # add notification to notifications table notify only if the user don't like to himself
            if comment_id == -1:
                cursor.execute("SELECT rowid, * FROM posts WHERE rowid = ?", (self.id,))
                the_post_data = cursor.fetchone()
                if the_user.email != the_post_data[1]:
                    cursor.execute('INSERT INTO notifications (user_1_email_writer, user_2_email_get, date, post_id, comment_id, notification, observed) VALUES (?, ?, ?, ?, ?, ?, ?)',(the_user.email, the_post_data[1], datetime.now().strftime("%d/%m/%Y | %H:%M"), self.id, -1, f"{the_user.first_name} {the_user.last_name} like your post", "false",))
            else:
                cursor.execute("SELECT rowid, * FROM comments WHERE post_id = ? AND rowid = ?", (self.id, comment_id,))
                the_comment_data = cursor.fetchone()
                if the_user.email != the_comment_data[1]:
                    cursor.execute('INSERT INTO notifications (user_1_email_writer, user_2_email_get, date, post_id, comment_id, notification, observed) VALUES (?, ?, ?, ?, ?, ?, ?)',(the_user.email, the_comment_data[1], datetime.now().strftime("%d/%m/%Y | %H:%M"), self.id, the_comment_data[0], f"{the_user.first_name} {the_user.last_name} like your comment", "false",))
        # remove like
        else:
            #delete from like table
            cursor.execute('DELETE FROM likes WHERE writer_email = ? AND post_id = ? AND comment_id = ?', (the_user.email, self.id, comment_id))
            # delete notification from notifications table
            cursor.execute('DELETE FROM notifications WHERE post_id = ? AND comment_id = ?', (self.id, comment_id,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def get_pictures_from_post(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # find the pictures
        query = f"SELECT rowid, * FROM pictures WHERE post_id = ?"
        cursor.execute(query, (self.id,))
        pictures_details = cursor.fetchall()
        pictures_paths = [img_details[2] for img_details in pictures_details]
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return pictures_paths


    def get_comments(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # find the comments
        query = f"SELECT rowid, * FROM comments WHERE post_id = ?"
        cursor.execute(query, (self.id,))
        comment_details = cursor.fetchall()
        comments_list = []
        if len(comment_details) > 0:
            for comment in comment_details:
                new_comment = Comment(comment[0], self.writer_user.get_user_by_mail(comment[1]), {"date": comment[2].split(" | ")[0], "time": comment[2].split(" | ")[1]}, comment[3], comment[4])
                comments_list.append(new_comment)
        all_comments = {"quantity": len(comments_list), "comments_list": comments_list}
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return all_comments


    def new_comment(self, the_user, tags, text):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # add to comments
        data_for_comment = (the_user.email, datetime.now().strftime("%d/%m/%Y | %H:%M"), text, self.id)
        cursor.execute('INSERT INTO comments (writer_email, date, text, post_id) VALUES (?, ?, ?, ?)', data_for_comment)
        query = f"SELECT rowid, * FROM comments WHERE writer_email = ? AND date = ? AND text = ? AND post_id = ?"
        cursor.execute(query, data_for_comment)
        comment_details = cursor.fetchone()
        # commit our command
        connection.commit()
        # add tags
        the_user.add_tags_to_table(tags, self.id, comment_details[0])
        # add notification to notifications table notify only if the user don't comment to himself
        cursor.execute("SELECT rowid, * FROM posts WHERE rowid = ?", (self.id,))
        the_post_data = cursor.fetchone()
        if the_user.email != the_post_data[1]:
            cursor.execute('INSERT INTO notifications (user_1_email_writer, user_2_email_get, date, post_id, comment_id, notification, observed) VALUES (?, ?, ?, ?, ?, ?, ?)',(the_user.email, the_post_data[1], datetime.now().strftime("%d/%m/%Y | %H:%M"), self.id, comment_details[0], f"{the_user.first_name} {the_user.last_name} comment on your post", "false",))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()



