from flask import Flask, render_template, request
import requests
import os
import smtplib


app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


def render_data():
    """Download simple test post data"""
    url = "https://api.npoint.io/d12847198b94a4df5e11"
    raw_data = requests.get(url).json()
    return raw_data


def send_email_to_me(message):
    """Send email to me"""
    mail_address = os.getenv('mailaddress')
    password = os.getenv("mailPassword")

    # Start connection with mail and log in user:
    con = smtplib.SMTP('smtp.gmail.com')
    con.starttls()
    con.login(user=mail_address, password=password)
    con.sendmail(from_addr=mail_address, to_addrs=mail_address, msg=message)
    con.close()


@app.route("/")
def home():
    return render_template("index.html", blog_data=render_data(), length=len(render_data()))


@app.route("/home")
def return_home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html", error="")


@app.route('/send_contact', methods=["POST"])
def send_contact():
    def validation(query):
        for entry in query:
            if entry == "":
                return False
        return True

    def error_check(validation_data):
        errors = ""
        for field_name, value in validation_data.items():
            if value == "":
                errors += field_name + ", "
        errors = errors[:-2]
        error_text = f"Please, fill this fields before moving on: {errors}"
        return error_text

    name = request.form.get('name')
    phone = request.form.get('phone')
    mail = request.form.get('email')
    message = request.form.get('message')

    if validation([name, phone, mail, message]):
        await send_email_to_me(f"Message from: {name}, message text: {mail} \n "
                               f"Contact to {name}: phone: {phone}, email: {mail}")
        return render_template('contact_send.html')
    else:
        text_error = error_check({"Name": name, "Phone number": phone, "Email address": mail, "Message": message})
        return render_template('contact.html', error=text_error)


@app.route("/post/<int:post_id>")
def render_post(post_id):
    all_data = render_data()
    post = all_data[post_id]
    return render_template("post.html", post=post)
