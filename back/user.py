import os
import sqlite3
from datetime import datetime

from back.chat import Chat
from back.friend_request import Friend_request
from back.notification import Notification
from back.post import Post


class User:

    def __init__(self, id, first_name, last_name, email, password, gender, profile_picture_path, birthday, connected):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.gender = gender
        self.profile_picture_path = profile_picture_path
        self.birthday = birthday
        if connected == "false":
            self.connected = False
        else:
            self.connected = True
        self.friends_list = None
        self.notifications = None
        self.friend_requests = None
        self.chats = None


    def get_friend(self, email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM friends WHERE (user_1_email = ? AND user_2_email = ?) OR (user_1_email = ? AND user_2_email = ?)", (self.email, email, email, self.email,))
        data_friend = cursor.fetchone()
        if data_friend is None:
            friend = None
        else:
            if data_friend[1] != self.email:
                friend = self.get_user_by_mail(data_friend[1])
            else:
                friend = self.get_user_by_mail(data_friend[0])
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return friend

    def get_friends_of_user(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM friends WHERE user_1_email = ? OR user_2_email = ?", (self.email, self.email,))
        friends_list = []
        data_friends = cursor.fetchall()
        if len(data_friends) > 0:
            for friend in data_friends:
                if friend[1] != self.email:
                    friend_add = self.get_user_by_mail(friend[1])
                else:
                    friend_add = self.get_user_by_mail(friend[0])
                friends_list.append(friend_add)
        friends_list_sorted = self.sort_list_of_users_by_name(friends_list)
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return friends_list_sorted


    def get_notifications_of_user(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        #get all notifications
        cursor.execute("SELECT rowid, * FROM notifications WHERE user_2_email_get = ?", (self.email,))
        notifications_data = cursor.fetchall()
        notifications_list = []
        new_notifications_quantity = 0
        if len(notifications_data) > 0:
            for notification in notifications_data:
                if notification[7] == "false":
                    new_notifications_quantity += 1
                notifications_list.append(Notification(notification[0], self.get_user_by_mail(notification[1]), self.get_user_by_mail(notification[2]), {"date": notification[3].split(" | ")[0], "time": notification[3].split(" | ")[1]}, notification[4], notification[5], notification[6], notification[7]))
        all_notifications = {"new_notifications_quantity": new_notifications_quantity, "notifications_list": notifications_list}
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return all_notifications


    def sort_list_of_users_by_name(self, list):
        new_list = sorted(list, key=lambda user: user.first_name + " " + user.last_name)
        return new_list


    def refrash(self):
        self.friends_list = self.get_friends_of_user()
        self.notifications = self.get_notifications_of_user()
        self.friend_requests = self.get_all_friend_requests()
        self.chats = self.get_all_chats()
        self.chats["chats"] = self.sort_chats_by_date()


    def get_user_by_mail(self, email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        query = f"SELECT rowid, * FROM users WHERE email = ?"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        if user_data is None:
            user = None
        else:
            user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5],user_data[6], user_data[7], user_data[8])
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return user


    def get_user_by_id(self, id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM users WHERE rowid = ?", (id,))
        user_data = cursor.fetchone()
        if user_data is None:
            user = None
        else:
            user = self.get_user_by_mail(user_data[3])
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return user


    def notification_observed(self, notification_id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # Update
        cursor.execute("UPDATE notifications SET observed = ? WHERE rowid = ?", ("true", notification_id,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def all_notifications_observed(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # Update
        cursor.execute("UPDATE notifications SET observed = ? WHERE user_2_email_get = ?", ("true", self.email,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def send_friend_request(self, email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        #add new row
        data_for_friend_request = (self.email, email)
        cursor.execute('INSERT INTO friend_requests (user_1_email_writer, user_2_email_get) VALUES (?, ?)', data_for_friend_request)
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def cancel_friend_request(self, send_email, get_email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # delete friend_request row
        cursor.execute('DELETE FROM friend_requests WHERE (user_1_email_writer = ? AND user_2_email_get = ?) OR (user_1_email_writer = ? AND user_2_email_get = ?)', (send_email, get_email, get_email, send_email,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def get_friend_request(self, email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM friend_requests WHERE (user_1_email_writer = ? AND user_2_email_get = ?) OR (user_1_email_writer = ? AND user_2_email_get = ?)",(self.email, email, email, self.email,))
        data = cursor.fetchone()
        if data is not None:
            friend_request = Friend_request(data[0], self.get_user_by_mail(data[1]), self.get_user_by_mail(data[2]))
        else:
            friend_request = None
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return friend_request


    def get_all_friend_requests(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM friend_requests WHERE user_2_email_get = ?",(self.email,))
        data = cursor.fetchall()
        requests = []
        if len(data) > 0:
            for request in data:
                requests.append(Friend_request(request[0], self.get_user_by_mail(request[1]), self.get_user_by_mail(request[2])))
        all_requests = {"quantity": len(requests), "requests": requests}
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return all_requests


    def accept_friend_request(self, email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # add new row
        data = (self.email, email)
        cursor.execute('INSERT INTO friends (user_1_email, user_2_email) VALUES (?, ?)', data)
        # create a chat between two users
        data = (self.email, email)
        cursor.execute('INSERT INTO chats (user_1_email, user_2_email) VALUES (?, ?)', data)
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        #delte friend request
        self.cancel_friend_request(email, self.email)


    def delete_friend(self, email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # delete friend row
        cursor.execute('DELETE FROM friends WHERE (user_1_email = ? AND user_2_email = ?) OR (user_1_email = ? AND user_2_email = ?)', (self.email, email, email, self.email,))
        # delete chat with this friend row
        chat_id = self.get_chat_id_by_other_email(email)
        cursor.execute('DELETE FROM chats WHERE rowid = ?', (chat_id, ))
        # delete messages with this friend rows
        cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def search(self, search):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        query = "SELECT rowid, * FROM users WHERE first_name LIKE ? OR last_name LIKE ?"
        cursor.execute(query, ('%' + search + '%', '%' + search + '%',))
        # Fetch all the rows that match the query
        rows = cursor.fetchall()
        search_list = []
        if len(rows) > 0:
            for data in rows:
                search_list.append(self.get_user_by_mail(data[3]))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return search_list


    def get_friends_connected_or_not(self, connected):
        list = []
        for friend in self.friends_list:
            if friend.connected == connected:
                list.append(friend)
        return list


    def get_all_chats(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # find the all chats
        query_1 = f"SELECT rowid, * FROM chats WHERE user_1_email = ? OR user_2_email = ?"
        cursor.execute(query_1, (self.email, self.email, ))
        chats_data = cursor.fetchall()
        chats = []
        new_messages = 0
        if len(chats_data) > 0:
            for chat_data in chats_data:
                if chat_data[1] == self.email:
                    other_email = chat_data[2]
                else:
                    other_email = chat_data[1]
                new_chat = Chat(chat_data[0], self, self.get_user_by_mail(other_email))
                new_messages += new_chat.messages["quantity_new_messages"]
                if hasattr(new_chat, 'last_used'):
                    chats.append(new_chat)
        chats_dic = {"quantity_new_messages": new_messages, "chats": chats}
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return chats_dic


    def sort_chats_by_date(self):
        sorted_chats = sorted(self.chats["chats"], key=lambda x: datetime.strptime(x.last_used["date"] + " | " + x.last_used["time"], "%d/%m/%Y | %H:%M"))
        return sorted_chats

    def get_chat_id_by_other_email(self, other_email):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # find the chat
        query_1 = f"SELECT rowid, * FROM chats WHERE (user_1_email = ? AND user_2_email = ?) OR (user_1_email = ? AND user_2_email = ?)"
        cursor.execute(query_1, (self.email, other_email, other_email, self.email,))
        chat_data = cursor.fetchone()
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return chat_data[0]


    def get_chat_by_id(self, id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # find the chat
        query_1 = f"SELECT rowid, * FROM chats WHERE rowid = ?"
        cursor.execute(query_1, (id,))
        chat_data = cursor.fetchone()
        if self.email != chat_data[2]:
            chat = Chat(id, self, self.get_user_by_mail(chat_data[2]))
        else:
            chat = Chat(id, self, self.get_user_by_mail(chat_data[1]))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return chat


    def change_all_messages_to_observed(self, chat_id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        cursor.execute("UPDATE messages SET observed = 'true' WHERE chat_id = ? AND user_email_get = ? AND observed = ?",(chat_id, self.email, "false",))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def get_post(self, post_id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        #find the post test
        query_1 = f"SELECT rowid, * FROM posts WHERE rowid = ?"
        cursor.execute(query_1, (post_id,))
        post_details = cursor.fetchone()
        # find the writer
        writer_user = self.get_user_by_mail(post_details[1])
        post = Post(post_details[0], writer_user, {"date": post_details[2].split(" | ")[0], "time": post_details[2].split(" | ")[1]}, post_details[3], post_details[4])
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return post


    def get_posts(self, posts_from):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        all_posts = []
        if posts_from == "all":
            query = f"SELECT rowid, * FROM posts WHERE writer_email = ?"
            data = ()
            data += (self.email,)
            for user in self.friends_list:
                query += f" OR writer_email = ?"
                data += (user.email,)
            cursor.execute(query, data)
            posts_data = cursor.fetchall()
            if len(posts_data) > 0:
                for post in posts_data:
                    all_posts.append(self.get_post(post[0]))
        else:
            query = f"SELECT rowid, * FROM posts WHERE writer_email = ?"
            data = ()
            data += (posts_from,)
            cursor.execute("SELECT rowid, * FROM tags WHERE tag_email = ?", (posts_from,))
            tags_data = cursor.fetchall()
            for tag in tags_data:
                query += "OR rowid = ?"
                data += (tag[2],)
            cursor.execute(query, data)
            posts_data = cursor.fetchall()
            if len(posts_data) > 0:
                for post in posts_data:
                    all_posts.append(self.get_post(post[0]))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return all_posts


    def new_post(self, tags, location, text, files):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # add to posts
        data_for_posts = (self.email, datetime.now().strftime("%d/%m/%Y | %H:%M"), text, location)
        cursor.execute('INSERT INTO posts (writer_email, date, text, location) VALUES (?, ?, ?, ?)', data_for_posts)
        query = f"SELECT rowid, * FROM posts WHERE writer_email = ? AND date = ? AND text = ? AND location = ?"
        cursor.execute(query, data_for_posts)
        post_details = cursor.fetchone()
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        # add tags
        self.add_tags_to_table(tags, post_details[0], -1)
        # saving the pictures
        # open new directory
        new_dir_path = f"front/static/assets/data/posts/post_{post_details[0]}"
        os.makedirs(new_dir_path)
        # save files
        if files[0].filename != "":
            # create connection to database
            connection = sqlite3.connect("back/data/data.db")
            # create cursor
            cursor = connection.cursor()
            for index in range(len(files)):
                if ".png" in files[index].filename:
                    img_path = f"{new_dir_path}/{index + 1}.png"
                elif ".jpg" in files[index].filename:
                    img_path = f"{new_dir_path}/{index + 1}.jpg"
                files[index].save(img_path)
                # add to pictures
                data_for_pictures = (post_details[0], img_path)
                cursor.execute('INSERT INTO pictures (post_id, picture_path) VALUES (?, ?)', data_for_pictures)
            # commit our command
            connection.commit()
            # close our connection
            connection.close()
        return post_details[0]


    def add_tags_to_table(self, tags, post_id, comment_id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        #notification msg
        if comment_id == -1:
            notification_msg = f"{self.first_name} {self.last_name} tag you in post"
        else:
            notification_msg = f"{self.first_name} {self.last_name} tag you in comment"
        # add tags
        if len(tags) > 0:
            for tag in tags:
                data_for_tags = (tag.split(" | ")[1], post_id, comment_id)
                cursor.execute('INSERT INTO tags (tag_email, post_id, comment_id) VALUES (?, ?, ?)', data_for_tags)
                # add notification to notifications table
                cursor.execute('INSERT INTO notifications (user_1_email_writer, user_2_email_get, date, post_id, comment_id, notification, observed) VALUES (?, ?, ?, ?, ?, ?, ?)', (self.email, tag.split(" | ")[1], datetime.now().strftime("%d/%m/%Y | %H:%M"), post_id, comment_id, notification_msg, "false",))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def change_first_name_or_last_name_or_password(self, what_to_change, new_value):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        msg = ""
        query = f"UPDATE users SET {what_to_change} = ? WHERE rowid = {self.id}"
        cursor.execute(query, (new_value,))
        setattr(self, what_to_change, new_value)
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return msg


    def change_profile_picture(self, new_profile_picture):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        file_path = self.profile_picture_path
        if os.path.exists(file_path):
            os.remove(file_path)
        if ".png" in new_profile_picture.filename:
            profile_picture_path = f"front/static/assets/data/users/{self.email}/profile picture/profile picture.png"
        elif ".jpg" in new_profile_picture.filename:
            profile_picture_path = f"front/static/assets/data/users/{self.email}/profile picture/profile picture.jpg"
        new_profile_picture.save(profile_picture_path)
        #update path
        query = f"UPDATE users SET profile_picture_path = ? WHERE email = ?"
        cursor.execute(query, (profile_picture_path, self.email,))
        self.profile_picture_path = profile_picture_path
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def change_email(self, new_email):
        if self.get_user_by_mail(new_email) is not None:
            return "We already have a user with this email!"
        else:
            #reaname directory of user
            old_name_path = f"front/static/assets/data/users/{self.email}"
            new_name_path = f"front/static/assets/data/users/{new_email}"
            os.rename(old_name_path, new_name_path)

            # create connection to database
            connection = sqlite3.connect("back/data/data.db")
            # create cursor
            cursor = connection.cursor()

            #change tags
            query = f"UPDATE tags SET tag_email = ? WHERE tag_email = ?"
            cursor.execute(query, (new_email, self.email,))

            # change posts
            query = f"UPDATE posts SET writer_email = ? WHERE writer_email = ?"
            cursor.execute(query, (new_email, self.email,))

            # change likes
            query = f"UPDATE likes SET writer_email = ? WHERE writer_email = ?"
            cursor.execute(query, (new_email, self.email,))

            # change comments
            query = f"UPDATE comments SET writer_email = ? WHERE writer_email = ?"
            cursor.execute(query, (new_email, self.email,))

            # change chats
            query = f"UPDATE chats SET user_1_email = ? WHERE user_1_email = ?"
            cursor.execute(query, (new_email, self.email,))
            query = f"UPDATE chats SET user_2_email = ? WHERE user_2_email = ?"
            cursor.execute(query, (new_email, self.email,))

            # change messages
            query = f"UPDATE messages SET user_email_writer = ? WHERE user_email_writer = ?"
            cursor.execute(query, (new_email, self.email,))
            query = f"UPDATE messages SET user_email_get = ? WHERE user_email_get = ?"
            cursor.execute(query, (new_email, self.email,))

            # change friend requests
            query = f"UPDATE friend_requests SET user_1_email_writer = ? WHERE user_1_email_writer = ?"
            cursor.execute(query, (new_email, self.email,))
            query = f"UPDATE friend_requests SET user_2_email_get = ? WHERE user_2_email_get = ?"
            cursor.execute(query, (new_email, self.email,))

            # change friends
            query = f"UPDATE friends SET user_1_email = ? WHERE user_1_email = ?"
            cursor.execute(query, (new_email, self.email,))
            query = f"UPDATE friends SET user_2_email = ? WHERE user_2_email = ?"
            cursor.execute(query, (new_email, self.email,))

            # change notifications
            query = f"UPDATE notifications SET user_1_email_writer = ? WHERE user_1_email_writer = ?"
            cursor.execute(query, (new_email, self.email,))
            query = f"UPDATE notifications SET user_2_email_get = ? WHERE user_2_email_get = ?"
            cursor.execute(query, (new_email, self.email,))

            # change users
            query = f"SELECT rowid, * FROM users WHERE email = ?"
            cursor.execute(query, (self.email,))
            user_data = cursor.fetchone()
            #update profile pic path
            query = f"UPDATE users SET profile_picture_path = ? WHERE email = ?"
            pic_path = user_data[6].replace(self.email, new_email)
            cursor.execute(query, (pic_path, self.email,))
            #update email
            query = f"UPDATE users SET email = ? WHERE email = ?"
            cursor.execute(query, (new_email, self.email,))

            # commit our command
            connection.commit()
            # close our connection
            connection.close()
            self.email = new_email
            self.profile_picture_path = pic_path
            return ""

