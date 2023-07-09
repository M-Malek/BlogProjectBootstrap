from flask import Flask, render_template
import requests
import os


app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


def render_data():
    url = "https://api.npoint.io/d12847198b94a4df5e11"
    raw_data = requests.get(url).json()
    return raw_data


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
    return render_template("contact.html")


@app.route("/post/<int:post_id>")
def render_post(post_id):
    all_data = render_data()
    post = all_data[post_id]
    return render_template("post.html", post=post)
