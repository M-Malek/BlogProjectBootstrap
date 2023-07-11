from flask import Flask, render_template, request
import requests
import os
import smtplib

# Create Flask app and prepare to host app on render
app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


def render_data():
    """Function: Download simple test post data"""
    url = "https://api.npoint.io/d12847198b94a4df5e11"
    raw_data = requests.get(url).json()
    return raw_data


def send_email_to_me(message):
    """Send email to given email address as contact form between user and site owner"""
    # Custom env variables for smtp con with Gmail
    mail_address = os.getenv('mailaddress')
    password = os.getenv("mailPassword")

    # Start connection with mail and log in user:
    with smtplib.SMTP('smtp.gmail.com') as con:
        con.starttls()
        con.login(user=mail_address, password=password)
        con.sendmail(from_addr=mail_address, to_addrs=mail_address, msg=message)


@app.route("/")
def home():
    """Function: Render home page"""
    return render_template("index.html", blog_data=render_data(), length=len(render_data()))


@app.route("/home")
def return_home():
    """Function: Go back to home page"""
    return render_template("index.html")


@app.route("/about")
def about():
    """Function: Render About us page"""
    return render_template("about.html")


@app.route("/contact")
def contact():
    """Function: Render Contact page"""
    return render_template("contact.html", error="")


@app.route('/send_contact', methods=["POST"])
def send_contact():
    """Function responsible for collect data from HMTL form and preparing it to send contact message to site owner"""
    def validation(query):
        """Validation: test if user has left no blank fields"""
        for entry in query:
            if entry == "":
                return False
        return True

    def error_check(validation_data):
        """Function: prepare message to user which field user has to fill before proceed"""
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
        # !!!WARNING: send_email_to_me has to be disabled because of low resources on free render plan :|
        # App cannot send message: end of memory

        # Use this command in your app on your custom server to send message to you
        # send_email_to_me(f"Message from: {name}, message text: {mail} \n "
        #                  f"Contact to {name}: phone: {phone}, "
        #                  f"email: {mail}")
        return render_template('contact_send.html')
    else:
        text_error = error_check({"Name": name, "Phone number": phone, "Email address": mail, "Message": message})
        return render_template('contact.html', error=text_error)


@app.route("/post/<int:post_id>")
def render_post(post_id):
    """Function: render posts on home page"""
    all_data = render_data()
    post = all_data[post_id]
    return render_template("post.html", post=post)
