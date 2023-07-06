import sqlite3
from datetime import datetime

from back.message import Message


class Chat:


    def __init__(self, id, user_1, user_2):
        self.id = id
        self.user_1 = user_1
        self.user_2 = user_2
        self.messages = self.get_all_messages()
        if len(self.messages["messages_list"]) > 0:
            self.last_used = self.messages["messages_list"][-1].date

    def get_all_messages(self):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM messages WHERE chat_id = ?", (self.id,))
        messages_list = []
        quantity_new_messages = 0
        data_messages = cursor.fetchall()
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        if len(data_messages) > 0:
            for data_msg in data_messages:
                if data_msg[1] == self.user_1.email:
                    writer = self.user_1
                    get = self.user_2
                else:
                    writer = self.user_2
                    get = self.user_1
                messages_list.append(Message(data_msg[0], writer, get, data_msg[3], data_msg[4], data_msg[5], data_msg[6]))
                if data_msg[4] == "false" and data_msg[2] == self.user_1.email:
                    quantity_new_messages += 1
        dic_messages = {"quantity_new_messages": quantity_new_messages, "messages_list":messages_list}
        return dic_messages


    def new_message(self, text):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # add new message
        cursor.execute('INSERT INTO messages (user_email_writer, user_email_get, date, observed, chat_id, text) VALUES (?, ?, ?, ?, ?, ?)',(self.user_1.email, self.user_2.email, datetime.now().strftime("%d/%m/%Y | %H:%M"), "false", self.id, text,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


    def delete_message(self, message_id):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        # delete message
        cursor.execute('DELETE FROM messages WHERE rowid = ?', (message_id,))
        # commit our command
        connection.commit()
        # close our connection
        connection.close()



