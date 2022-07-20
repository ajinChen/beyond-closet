import os
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import secure_filename

# built-in
from models import Customer, RegisterTime, RegistrationForm, LogInForm, UploadForm
from connection import commit_tables
from __init__ import app, db, login_manager, team_members_yaml
import boto3
import time
import sys

# data science model
from combined import cloth_rec


# create tables
commit_tables(db)

# Flask Route Area
@login_manager.user_loader
# user_loader: use user ID reload the user object
def load_user(id):
    return Customer.query.get(int(id))


@app.route('/')
# home page for signIn user
def home():
    return render_template('index.html', authenticated_user=current_user.is_authenticated)


@app.route('/index.html')
# home page
def home_index():
    return render_template('index.html')


@app.route('/about.html')
# about page
def about():
    return render_template('about.html', team_members_yaml=team_members_yaml)


@app.route('/signIn.html', methods=['GET', 'POST'])
# signIn page
def sign_in():
    login_form = LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = Customer.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            session['messages'] = username
            return redirect(url_for('home_index'))
        else:
            flash('Invalid username and password combination!')
    return render_template('signIn.html', form=login_form)


@app.route('/signUp.html', methods=('GET', 'POST'))
# signUp page
def sign_up():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        user_count = Customer.query.filter_by(username=username).count()
        if (user_count > 0):
            flash('Sorry, this email has already been registered : ' + username)
        else:
            user = Customer(username, password)
            rt = RegisterTime(username)
            db.session.add(user)
            db.session.add(rt)
            db.session.commit()
            flash('Thanks for registering!')
            return redirect(url_for('sign_in'))
    return render_template('signUp.html', form=registration_form)


@app.route('/dynamic_tab.html', methods=('GET', 'POST'))
@login_required
# dynamic panel
def dynamic_tab():
    user_fileform = UploadForm()
    username = session['messages']
    user_contents = {
        'urls': [],
        'num_recommendation': 0,
        'pattern': False
    }
    color_vecs = {
        'coat': (255, 255, 255),
        'shirt': (255, 255, 255),
        'trousers': (255, 255, 255)
    }

    if request.method == 'POST':
        # pattern and num of choices
        user_contents['num_recommendation'] = len(request.form.getlist('recommendation'))
        user_contents['pattern'] = False if str(request.form.get('pattern')) == 'complementary' else True
        # image file storage
        coat_image = request.files['coat_image']
        shirt_image = request.files['shirt_image']
        trousers_image = request.files['trousers_image']

        # upload image and return url
        for item, item_type in zip((coat_image, shirt_image, trousers_image), ('coat', 'shirt', 'trousers')):
            if item:
                image_url = upload_clothing_jpeg_to_s3(username, item, item_type)
                user_contents['urls'].append(image_url)
                print(os.getenv('AWS_ACCESS_KEY'), file=sys.stderr)
                print(os.getenv('AWS_SECRET_ACCESS_KEY'), file=sys.stderr)
                print(image_url, file=sys.stderr)
        color_recommed = cloth_rec(user_contents)
        # if user_contents['pattern']:
        #     color_recommed = [(119, 60, 139), (207, 51, 109)]
        # else:
        #     color_recommed = [(46, 106, 176), (211, 223, 240)]
        for tup in zip(request.form.getlist('recommendation'), color_recommed):
            color_vecs[tup[0]] = tup[1]
        session['color'] = color_vecs

        # the following return is for test only, please deleted after testing
        # return f'''<!DOCTYPE html>
        #             <html>
        #             <body>
        #             <h1>Number of Recommendations: {str(user_contents['num_recommendation'])}</h1>
        #             <h1>Pattern: {str(user_contents['pattern'])}</h1>
        #             <h1>Image File Content:</h1>
        #             <p>{str(coat_image)[:10]}</p>
        #             <p>{str(shirt_image)[:10]}</p>
        #             <p>{str(trousers_image)[:10]}</p>
        #             <p>{str(user_contents['urls'])}</p>
        #             </body>
        #             </html>'''
        return redirect(url_for('result_page'))
    return render_template('dynamic_tab.html')

# @app.route('/logout')
# @login_required
# # logout page
# def logout():
#     before_logout = '<h1> Before logout - is_autheticated : ' \
#                     + str(current_user.is_authenticated) + '</h1>'
#     logout_user()
#     after_logout = '<h1> After logout - is_autheticated : ' \
#                    + str(current_user.is_authenticated) + '</h1>'
#     return before_logout + after_logout
#


@app.route('/result_page.html')
# recommendation result display page
def result_page():
    rgb_vecs = session['color']
    return render_template('result_page.html', vecs=rgb_vecs)


# S3 (need fit)
# sql_connection_string = os.environ["SQL_STRING"]
bucket_name = os.getenv('AWS_BUCKET_NAME')
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def upload_clothing_jpeg_to_s3(user_id, image_file, style):
    ts = int(time.time())
    filename = secure_filename(f"{user_id}_{ts}_{style}.jpeg")
    try:
        s3.put_object(Body=image_file,
            Bucket=bucket_name,
            Key=filename,
            ContentType=request.mimetype)
    except Exception as e:
        print(f"Something Happened: {e}", file=sys.stderr)
        return f'''<!DOCTYPE html><html><body><p>{str(e)}</p></body></html>'''
    # after upload file to s3 bucket, return filename of the uploaded file
    region = 'us-west-2'
    url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{filename}"
    return url


# Main area
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
