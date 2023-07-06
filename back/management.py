import shutil
import sqlite3
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from PIL import Image

from back.user import User



class Management:
    def __init__(self):
        self.the_user = None
        self.verification_code = None
        self.temp_user = None


    def register(self, first_name,  last_name, birthday, gender, email, password, profile_picture):
        user_details = self.get_user_by_mail(email)
        #check if we have a user with this email
        if user_details is not None:
            return "We already have a user with this email!"
        else:
            #open all new directories
            new_dir_path1 = f"front/static/assets/data/users/{email}"
            if not os.path.exists(new_dir_path1):
                os.makedirs(new_dir_path1)
            new_dir_path2 = f"front/static/assets/data/users/{email}/profile picture"
            os.makedirs(new_dir_path2)

            # put the profile picture in the right directory and choose picture
            profile_picture_path = ""
            if profile_picture.filename == "":
                image_path = ""
                # male automate picture
                if gender == "Male":
                    # set the path of the image you want to open
                    image_path = "back/automatic profile pictures/male.jpg"
                # female automate picture
                else:
                    # set the path of the image you want to open
                    image_path = "back/automatic profile pictures/female.jpg"
                # open the image using the PIL library
                image = Image.open(image_path)
                # set the path where you want to save the opened image
                profile_picture_path = f"{new_dir_path2}/profile picture.jpg"
                # save the image to the specified path
                image.save(profile_picture_path)

            # picture the user choose
            else:
                if ".png" in profile_picture.filename:
                    profile_picture_path = f"{new_dir_path2}/profile picture.png"
                elif ".jpg" in profile_picture.filename:
                    profile_picture_path = f"{new_dir_path2}/profile picture.jpg"
                profile_picture.save(profile_picture_path)

            # create connection to database
            connection = sqlite3.connect("back/data/data.db")
            # create cursor
            cursor = connection.cursor()
            # save as a row in the db
            data = (first_name, last_name, email, password, gender, profile_picture_path, birthday, 'false')
            cursor.execute('INSERT INTO users (first_name, last_name, email, password, gender, profile_picture_path, birthday, connected) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

            # commit our command
            connection.commit()
            # close our connection
            connection.close()
            return ""


    def sign_in(self, email, password):
        user = self.get_user_by_mail(email)
        if user is None:
            return "We do not have a user with this email!"
        else:
            #check password
            if password != user.password:
                return "Incorrect password!"
            else:
                self.the_user = user
                self.update_connected_status("true")
                return ""


    def update_connected_status(self, new_status):
        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()
        if new_status == "true":
            query = "UPDATE users SET connected = ? WHERE email = ?;"
            cursor.execute(query, (new_status, self.the_user.email,))
            self.the_user.connected = True
        else:
            query = "UPDATE users SET connected = ? WHERE email = ?;"
            cursor.execute(query, (new_status, self.the_user.email,))
            self.the_user = None
        # commit our command
        connection.commit()
        # close our connection
        connection.close()


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
            user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7], user_data[8])
        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        return user


    def delete_user(self):
        msg = ""

        #delete directory of user
        dir_path = f"front/static/assets/data/users/{self.the_user.email}"
        try:
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            msg = "An error occurred!"
            return msg

        # create connection to database
        connection = sqlite3.connect("back/data/data.db")
        # create cursor
        cursor = connection.cursor()

        # delete tags
        query = f"DELETE FROM tags WHERE tag_email = ?"
        cursor.execute(query, (self.the_user.email,))

        # delete posts
        query = f"DELETE FROM posts WHERE writer_email = ?"
        cursor.execute(query, (self.the_user.email,))

        # delete likes
        query = f"DELETE FROM likes WHERE writer_email = ?"
        cursor.execute(query, (self.the_user.email,))

        # delete comments
        query = f"DELETE FROM comments WHERE writer_email = ?"
        cursor.execute(query, (self.the_user.email,))

        # delete chats
        query = f"DELETE FROM chats WHERE user_1_email = ? OR user_2_email = ?"
        cursor.execute(query, (self.the_user.email, self.the_user.email,))

        # delete messages
        query = f"DELETE FROM messages WHERE user_email_writer = ? OR user_email_get = ?"
        cursor.execute(query, (self.the_user.email, self.the_user.email,))

        # delete friend requests
        query = f"DELETE FROM friend_requests WHERE user_1_email_writer = ? OR user_2_email_get = ?"
        cursor.execute(query, (self.the_user.email, self.the_user.email,))

        # delete friends
        query = f"DELETE FROM friends WHERE user_1_email = ? OR user_2_email = ?"
        cursor.execute(query, (self.the_user.email, self.the_user.email,))

        # delete notifications
        query = f"DELETE FROM notifications WHERE user_1_email_writer = ? OR user_2_email_get = ?"
        cursor.execute(query, (self.the_user.email, self.the_user.email,))

        # delete user
        query = f"DELETE FROM users WHERE email = ?"
        cursor.execute(query, (self.the_user.email,))

        # commit our command
        connection.commit()
        # close our connection
        connection.close()
        self.the_user = None
        return msg


    def send_and_get_verification_code(self, email):
        verification_code = random.randint(100000, 999999)

        # Recipient's email address
        recipient_email = email

        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = os.environ['sender_email']
        message["To"] = recipient_email
        message["Subject"] = " Friends - verification code"

        # Add body to the email
        body = f"The verification code is : {verification_code}"
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server (in this case, Gmail's SMTP server)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable secure connection
            server.login(os.environ['sender_email'], os.environ['sender_password'])
            server.sendmail(os.environ['sender_email'], recipient_email, message.as_string())
        self.verification_code = verification_code