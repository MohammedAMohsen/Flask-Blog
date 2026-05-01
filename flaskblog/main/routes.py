from flaskblog.models import Post
from flask import render_template,request, Blueprint, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', posts=posts)
 

@main.route("/about")
def about():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return  render_template('about.html', title = "About")