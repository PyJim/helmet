from flask import Flask, render_template, request, g, redirect, flash, url_for
from queries import PasswordCheck, EmailCheck, check_author, create_author, find_author, create_author_reports, create_report, edit_report, add_report, get_all_reports, get_author_reports, addEvent, searchEvents, allEvents, searchPosts, deleteEvent, deletePost, searchUserEvents, searchUserPosts, getUserEvents
import os
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime

#postgres://helmet_user:tB66JRufNVQ2MzdCXKmkasCAXe5CFMRs@dpg-chl4l5m7avj2179h6sq0-a.oregon-postgres.render.com/helmet

app = Flask(__name__)
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'static/images/'

app.secret_key = 'secrete key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'png', 'gif', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    print(events)
    return render_template('index.html', events=events)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    target_url = url_for('create_account') + "#signup"
    return redirect(target_url)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        """if signup_empty(name, username, email, password, confirm_password):
            message = 'please fill all available'
            flash(message)
            return redirect(request.url)"""
        if name and name.strip():  # Check if name is not None or empty
            name = name.strip().capitalize()
        else:
            message = 'Please enter a valid name'
            flash(message)
            return redirect(request.url)

        user_password = PasswordCheck(password, confirm_password)
        user_email = EmailCheck(email)

        if user_password.mismatch():
            message = 'password mismatch'
            flash(message)
            return redirect(request.url)
        elif user_password.not_strong():
            message = 'weak password'
            flash(message)
            return redirect(request.url)
        elif user_email.invalid():
            message = 'invalid email'
            flash(message)
            return redirect(request.url)

        author = check_author(username, email)
        result1 = author[0]
        result2 = author[1]

        if result1 and result2:
            message = f'{username} and {email} already exist'
            flash(message)
            return redirect(request.url)
        elif result1:
            message = f'{username} already exist'
            flash(message)
            return redirect(request.url)
        elif result2:
            message = f'{email} already exist'
            flash(message)
            return redirect(request.url)
        else:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            create_author(name.strip().capitalize(), username, email, password)
            create_author_reports(username)
            message = f'Account created successfully'
            flash(message)
            return redirect('/signin')
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    return render_template('index.html', signin=False, events=events)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    target_url = url_for('login') + "#signup"
    return redirect(target_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    # ensuring that only non empty passwords are allowed
        """if signin_empty(username, password):
            message = 'please fill all available'
            flash(message)
            return redirect(request.url)"""

        global author
        author = find_author(username)
        if author:
            author = author[0]
            correct_password = bcrypt.check_password_hash(author[4], password)
            if correct_password:
                # return render_template('author.html', author=author, reports=reports)
                flash('Signed in successfully')
                return redirect(f'/author/{username}')
            else:
                message = 'incorrect password'
                flash(message)
                return redirect(request.url)
        else:
            message = 'User does not exist'
            flash(message)
            return redirect(request.url)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    return render_template('index.html', signin = True, event=events)

@app.route('/author/<username>', methods=['GET', 'POST'])
def author_home(username):
    global user
    user = username
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    reports = []
    all_reports = get_all_reports()

    if request.method == 'POST':
        phrase = request.form.get('q')
        if phrase != '':
            all_reports = searchPosts(phrase)
            events = searchEvents(phrase, current_datetime)
    
    if all_reports:
        for report in all_reports:
            reports.append(list(report))
    
    """author_rep = []
    author_reports = get_author_reports(username)
    for report in author_reports:
        author_rep.append(list(report))"""

    author = find_author(username)
    if author:
        author = author[0]
        return render_template('user.html', author=author, reports=reports, events=events)#, author_reports = author_rep)
    else:
        message = 'ID does not exist'
        return redirect(request.url)

@app.route('/<username>/report', methods=['GET', 'POST'])
def report(username):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = getUserEvents(username, current_datetime)
    all_reports = get_author_reports(username)

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        description = request.form.get('description')
        video = request.form.get('video')

        if 'file' not in request.files:
            flash('No file chosen')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(str(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Image successfully uploaded')

            create_report(username, title, location, description, filename, video)
            add_report(username, title, location, description, filename, video)

            return redirect(f'/{username}/myposts')

        else:
            flash('Allowed image types are - png, jpg, jpeg and gif')
            return redirect(request.url)

    author = find_author(username)
    if author:
        return render_template('add.html', author=author[0], events=events, reports=all_reports)
    else:
        flash('No such user')
        return redirect('/signup')

@app.route('/<username>/events', methods=['GET', 'POST'])
def user_events(username):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    reports = get_all_reports()

    author = find_author(username)
    if author:
        author = author[0]

    if request.method == 'POST':
        phrase = request.form.get('q')
        if phrase != '':
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            events = searchEvents(phrase, date_time)
            reports = get_author_reports(username)

    return render_template('user.html', user=username, author=author, events=events, reports=reports)

@app.route('/<username>/my_events', methods=['GET', 'POST'])
def user_myevents(username):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    reports = get_author_reports(username)

    author = find_author(username)
    if author:
        author = author[0]

    if request.method == 'POST':
        phrase = request.form.get('q')
        if phrase != '':
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            events = searchUserEvents(phrase, username, date_time)
            reports = searchUserPosts(phrase, username)

    return render_template('add.html', user=username, author=author, events=events, reports=reports)

@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        phrase = request.form.get('q')
        if phrase != '':
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            events = searchEvents(phrase, date_time)

    target_url = url_for('find_events') + "#events"
    return redirect(target_url)
    
@app.route('/find_events')
def find_events():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    return render_template('index.html', signin=False, events=events)


@app.route('/<username>/myposts', methods=['GET', 'POST'])
def user_posts(username):
    reports = []
    all_user_reports = get_author_reports(username)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = allEvents(current_datetime)
    if all_user_reports:
        for report in all_user_reports:
            reports.append(list(report))
    
    author = find_author(username)
    if author:
        author = author[0]
    return render_template('add.html', reports=reports, author=author, events=events)


@app.route('/<username>/home', methods=['GET', 'POST'])
def home(username):
    return redirect(f'/author/{username}')

@app.route('/<username>/report', methods=['GET', 'POST'])
def user_report(username):
    return render_template('report.html')

@app.route('/<username>/add_event', methods=['GET', 'POST'])
def add_event(username):
    if request.method == 'POST':
        # title, date, time, desc, org, loc, story, image
        title = request.form.get('title')
        date_time = request.form['datetime']
        desc = request.form.get('description')
        org = request.form.get('organizer')
        loc = request.form.get('location')

        if 'file' not in request.files:
            flash('No file chosen')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(str(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Image successfully uploaded')
            addEvent(title, date_time, desc, org, loc, filename, username)
            print("done")
            flash('Event added successfully')
            return redirect(request.url)
        
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = getUserEvents(username, current_datetime)
    all_reports = get_author_reports(username)
    author = find_author(username)
    if author:
        author = author[0]
        return render_template('add.html', author=author, reports=all_reports, events=events)
    return redirect(request.url)


@app.route('/event/del', methods=['GET', 'POST'])
def del_event():
    if request.method == 'POST':
        event_id = request.form.get("event_id")
        deleteEvent(event_id)

    return redirect(f'/{user}/myposts')
    
@app.route('/post/del', methods=['GET', 'POST'])
def del_post():
    if request.method == 'POST':
        post_id = request.form.get("post_id")
        deletePost(post_id)

    return redirect(f'/{user}/myposts')

@app.route('/<username>/notification')
def user_notification(username):
    return render_template('notification.html')

@app.route('/edit_post/<post_id>', methods=['GET','POST'])
def edit_post(post_id):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    events = getUserEvents(user, current_datetime)
    all_reports = get_author_reports(user)
    author = find_author(user)

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        description = request.form.get('description')
        video = request.form.get('video')

        if 'file' not in request.files:
            flash('No file chosen')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(str(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Image successfully uploaded')

            edit_report(user, title, location, description, filename, video, post_id)

            return redirect(f'/{user}/myposts')

        else:
            flash('Allowed image types are - png, jpg, jpeg and gif')
            return redirect(request.url)

    return render_template('modal.html', author=author, reports=all_reports, events=events,report_id = post_id)



if __name__ == '__main__':
    app.run(debug=True)
