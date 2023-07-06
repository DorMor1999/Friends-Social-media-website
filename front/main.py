from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for

from back.chat import Chat
from back.management import Management


app = Flask(__name__)


global management
management = Management()


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # new post test
        if "new_post" in request.form:
            post_id = management.the_user.new_post(request.form.getlist("tag"), str(request.form["location"]), str(request.form["text"]), request.files.getlist('files'))
            return redirect(url_for('post test', post_id=post_id))
        # sign out
        elif "sign_out" in request.form:
            management.update_connected_status("false")
            return redirect(url_for('home'))
        #search
        elif "search" in request.form:
            return redirect(url_for('search', search_term=request.form["search"]))
    if management.the_user is None:
        return render_template("index/index not connected.html", office=management)
    else:
        management.the_user.refrash()
        return render_template("index/index connected.html", office=management, posts=management.the_user.get_posts("all"))


@app.route("/register", methods=['POST', 'GET'])
def register():
    msg = ""
    if request.method == 'POST':
        msg = management.register(str(request.form["first_name"]), str(request.form["last_name"]), str(request.form["birthday"]), str(request.form["inlineRadioOptions"]), str(request.form["email"]).lower(), str(request.form["password"]), request.files['profile_picture'])
        if msg == "":
            return redirect(url_for('home'))
    return render_template("register/register.html", office=management, msg=msg)


@app.route("/sign_in", methods=['POST', 'GET'])
def sign_in():
    msg = ""
    if request.method == 'POST':
        msg = management.sign_in(str(request.form["email"]).lower(), str(request.form["password"]))
        if msg == "":
            return redirect(url_for('home'))
    return render_template("sign in/sign in.html", office=management, msg=msg)


@app.route("/forgot_my_password", methods=['POST', 'GET'])
def forgot_my_password():
    msg = ""
    if request.method == 'POST':
        if "email" in request.form:
            management.temp_user = management.get_user_by_mail(request.form["email"])
            if management.temp_user is None:
                msg = "We do not have a user with this email!"
            else:
                return redirect(url_for('user_authentication'))
    return render_template("forgot my password/forgot my password.html", office=management, msg=msg)


@app.route("/user_authentication", methods=['POST', 'GET'])
def user_authentication():
    msg = ""
    if management.verification_code is None:
        management.send_and_get_verification_code(management.temp_user.email)
    if request.method == 'POST':
        if "verification_code" in request.form:
            if management.verification_code == (int)(request.form["verification_code"]):
                management.verification_code = None
                return redirect(url_for('new_password'))
            else:
                msg = "Incorrect verification code!"
    return render_template("user authentication/user authentication.html", office=management, msg=msg)


@app.route("/new_password", methods=['POST', 'GET'])
def new_password():
    if request.method == 'POST':
        if "password" in request.form:
            management.temp_user.change_first_name_or_last_name_or_password("password", str(request.form["password"]))
            management.temp_user = None
            return redirect(url_for('home'))
    return render_template("new password/new password.html", office=management)


@app.route("/profile/<first_name>_<last_name>_<id>", methods=['POST', 'GET'])
def profile(first_name, last_name, id):
    if request.method == 'POST':
        if "send_friend_request" in request.form:
            management.the_user.send_friend_request(request.form["send_friend_request"])
        elif "cancel_friend_request" in request.form:
            management.the_user.cancel_friend_request(management.the_user.email, request.form["cancel_friend_request"])
        elif "accept_friend_request" in request.form:
            management.the_user.accept_friend_request(request.form["accept_friend_request"])
        elif "decline_friend_request" in request.form:
            management.the_user.cancel_friend_request(request.form["decline_friend_request"], management.the_user.email)
        elif "delete_friend" in request.form:
            management.the_user.delete_friend(request.form["delete_friend"])
        return redirect(url_for('profile', first_name=first_name, last_name=last_name, id=id))
    management.the_user.refrash()
    profile_user = management.the_user.get_user_by_id(id)
    profile_user.refrash()
    return render_template("profile/profile.html", office=management, profile_user=profile_user, posts=management.the_user.get_posts(profile_user.email))


@app.route("/profile/<first_name>_<last_name>_<id>/gallery", methods=['POST', 'GET'])
def gallery(first_name, last_name, id):
    management.the_user.refrash()
    profile_user = management.the_user.get_user_by_id(id)
    profile_user.refrash()
    return render_template("profile/gallery/gallery.html", office=management, profile_user=profile_user, posts=management.the_user.get_posts(profile_user.email))



@app.route("/posts/post_<post_id>", methods=['POST', 'GET'])
def post(post_id):
    the_post = management.the_user.get_post(post_id)
    if request.method == 'POST':
        if "like" in request.form:
            the_post.like_operation(-1, management.the_user)
        elif 'like_comment' in request.form:
            the_post.like_operation(int(request.form["like_comment"]), management.the_user)
        elif "comment" in request.form:
            the_post.new_comment(management.the_user, request.form.getlist("tag_comment"), str(request.form["text_comment"]))
        elif "delete_post" in request.form:
            the_post.delete_post()
            return redirect(url_for('home'))
        elif "delete_comment" in request.form:
            the_post.delete_comment(int(request.form["delete_comment"]))
        elif "specific_notification" in request.form:
            management.the_user.notification_observed(int(request.form["specific_notification"]))
        return redirect(url_for('post test', post_id=post_id))
    the_post = management.the_user.get_post(post_id)
    management.the_user.refrash()
    return render_template("post test/post test.html", office=management, the_post=the_post)


@app.route("/notifications/<first_name>_<last_name>_<id>", methods=['POST', 'GET'])
def notifications(first_name, last_name, id):
    if request.method == 'POST':
        if "read_and_show_all" in request.form:
            management.the_user.all_notifications_observed()
        return redirect(url_for('notifications', first_name=first_name, last_name=last_name, id=id))
    management.the_user.refrash()
    return render_template("notifications/notifications.html", office=management)


@app.route("/search_<search_term>", methods=['POST', 'GET'])
def search(search_term):
    search_list = management.the_user.search(search_term)
    management.the_user.refrash()
    return render_template("search/search.html", office=management, search_list=search_list)


@app.route("/chat_<chat_id>", methods=['POST', 'GET'])
def chat(chat_id):
    chat = management.the_user.get_chat_by_id(chat_id)
    if request.method == 'POST':
        if "new_message" in request.form:
            chat.new_message(str(request.form["new_message"]))
        elif "delete_message" in request.form:
            chat.delete_message(request.form["delete_message"])
        return redirect(url_for('chat', chat_id=chat_id))
    management.the_user.change_all_messages_to_observed(chat_id)
    chat = management.the_user.get_chat_by_id(chat_id)
    management.the_user.refrash()
    return render_template("chat/chat.html", office=management, chat=chat)


@app.route("/profile/<first_name>_<last_name>_<id>/private", methods=['POST', 'GET'])
def private(first_name, last_name, id):
    msg = ""
    if request.method == 'POST':
        if "first_name" in request.form:
            management.the_user.change_first_name_or_last_name_or_password("first_name", str(request.form["first_name"]))
        elif "last_name" in request.form:
            management.the_user.change_first_name_or_last_name_or_password("last_name", str(request.form["last_name"]))
        elif "email" in request.form:
            msg = management.the_user.change_email(str(request.form["email"]))
        elif "password" in request.form:
            management.the_user.change_first_name_or_last_name_or_password("password", str(request.form["password"]))
        elif "delete_user" in request.form:
            msg = management.delete_user()
            if msg == "":
                return redirect(url_for('home'))
        else:
            management.the_user.change_profile_picture(request.files['profile_picture'])
    management.the_user.refrash()
    return render_template("profile/private/private.html", office=management, msg=msg)


if __name__ == "__main__":
    app.run(debug=True)