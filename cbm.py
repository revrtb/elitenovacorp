from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from forms import ContactForm, SignUpForm
from flask_mail import Message
# from flaskext.mysql import MySQL

# from flask_mysqldb import MySQL
from flask import jsonify
import json
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import appconfig
from lib import db
from lib import user
from lib import email
import os

### APPLICATIO  SETUP ###
application = Flask(__name__) 
 
application.config.from_object('appconfig.DevelopmentConfig')
application.config.update(
    MAIL_PASSWORD=os.environ['MAIL_PASS'],
    RECAPTCHA_PUBLIC_KEY=os.environ['RECAPTCHA_PUBLIC_KEY'],
    RECAPTCHA_PRIVATE_KEY=os.environ['RECAPTCHA_PRIVATE_KEY']
    )

appconfig.Domain.DOMAIN = os.environ['DOMAIN']

mail = email.aMail()

mail.initApp(application)


# application.config['MYSQL_DATABASE_USER'] = appconfig.MYSQLDB.USER
# application.config['MYSQL_DATABASE_PASSWORD'] = appconfig.MYSQLDB.PASSWORD
# application.config['MYSQL_DATABASE_DB'] = appconfig.MYSQLDB.DB
# application.config['MYSQL_DATABASE_HOST'] = appconfig.MYSQLDB.HOST
# application.config['MYSQL_DATABASE_PORT'] = appconfig.MYSQLDB.PORT
# mysql = MySQL()
# mysql.init_app(application)
dbo = db.DB()

login_manager = LoginManager()
login_manager.init_app(application)

### ### ### ### ### ### ###

@application.route('/')
def index():
    return render_template('index.html', page='home', domain=appconfig.Domain.DOMAIN)

@application.route('/google76d353eef6dd1d9c.html')
def gv():
    return render_template('google76d353eef6dd1d9c.html')

@application.route('/home')
def home():
	return render_template('index.html', page='home')

@application.route('/test')
def test():
        return render_template('test.html', page='test')

@application.route('/policy')
def policy():
	return render_template('policy.html', page='policy', domain=appconfig.Domain.DOMAIN)

@application.route('/admin')
def admin_login():
    return render_template('admin_login.html', page='admin_login')

@application.route('/terms')
def terms():
    return render_template('terms.html', page='terms', domain=appconfig.Domain.DOMAIN)

@application.route('/advertisers')
def advertisers():
	return render_template('advertisers.html', page='advertisers')

@application.route('/career')
def career():
    return render_template('career.html', page='career')

@application.route('/reset')
def reset():
    user = request.args.get('user')
    if user != 'publisher' and user != 'advertiser':
        return render_template('404.html'), 404 
    return render_template('reset.html', user=user)

@application.route('/login')
def login():
    user = request.args.get('user')
    if user != 'publisher' and user != 'advertiser' and user != 'admin':
        return render_template('404.html'), 404 
    if user == 'publisher':
        action = "http://login.revrtb.com/publisher/login"
    elif user == 'advertiser':
        action = "http://login.revrtb.com/advertiser/login"
    return render_template('login.html', page='login', user=user, action=action)

@application.route('/publishers') #services
def publishers():
	return render_template('publishers.html', page='publishers')

@login_manager.user_loader
def load_user(user_id):
    usr = user.CBMUser()
    usr.get_user(user_id, dbo)
    return usr

@application.route('/dashboard', methods=['POST', 'GET']) #services
def dashboard():
    if request.method == 'GET' and not current_user.is_active:
        return render_template('dashboard_login.html', page='dashboard_login')
    else:
        if current_user.is_active:
            usero = current_user
        elif dbo.validate_login(request.form['login'], request.form['password']):
            usero = user.CBMUser()
            usero.get_user_by_uname(request.form['login'], dbo)
        else:
            return render_template('dashboard_login.html', page='dashboard_login', error="Wrong username or password!")

        login_user(usero)
        print (dbo.get_publishers())
        info, data = dbo.get_publishers()
        return render_template('dashboard.html', page='dashboard', publishers=data, fields=info, count=len(data), domain=appconfig.Domain.DOMAIN)
        
@application.route('/get_publisher', methods=['POST'])
@login_required
def get_publisher():
    data = dbo.get_publisher_by_feedid(request.form.get('feedid'))
    return jsonify({'data': data})

@application.route('/save_publisher', methods=['POST'])
@login_required
def save_publisher():
    try:
        name = request.form.get('name')
        subid = request.form.get('subid')
        feedid = request.form.get('feedid')
        feedauth = request.form.get('feedauth')
        delay = request.form.get('delay')
        max = request.form.get('max')
        period = request.form.get('period')
        default_url = request.form.get('default_url', '')
        email = request.form.get('email', '')
        short_link = request.form.get('short_link', '')
        id = request.form.get('id', 0)
        if id == 0:
            status = dbo.add_publisher(name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link)
        else:
            status = dbo.update_publisher(id, name, subid, feedid, feedauth, delay, max, period, default_url, email, short_link)
        return jsonify({'data': status})
    except Exception as e:
        return jsonify({'data': e.message})

@application.route('/delete_publisher', methods=['POST'])
@login_required
def delete_publisher():
    try:
        feedid = request.form.get('feedid')
        status = dbo.delete_publisher(feedid)
        return jsonify({'data': status})
    except Exception as e:
        return jsonify({'data': e.message})        

@application.route('/notify_publisher', methods=['POST'])
@login_required
def notify_publisher():
    try:
        html_code = request.form.get('html_code')
        pub_name = request.form.get('pub_name')
        email = request.form.get('email')
        direct_url = request.form.get('direct_url')
        feed_url = request.form.get('feed_url')
        id = request.form.get('id')
        domain = appconfig.Domain.DOMAIN
        msg = Message('%s (new adserving domain code) - %s'%(domain, pub_name), sender=appconfig.MailData.FROM, recipients=[email])
        msg.body = ""
        msg.html = render_template('notify_email.html', domain=domain, publisher_name=pub_name, feed_url=feed_url, direct_url=direct_url, html_code=html_code)
        mail.send_email(msg)
        status = dbo.update_publisher_dt([id])
        return jsonify({'data': status})
    except Exception as e:
        return jsonify({'data': e.message})

@application.route('/notify_all', methods=['POST'])
@login_required
def notify_all():
    try:
        pubs = request.form.get('pubs')
        ps = json.loads(pubs)
        domain = appconfig.Domain.DOMAIN
        status = True
        ids = []
        for p in ps:
            if  p['email'] != '' and p['email'] != 'None':
                ids.append(p['id'])
                pub_name = p['pub_name']
                email = p['email']
                feed_url = p['feed_url']
                direct_url = p['direct_url']
                html_code = p['html_code']
                msg = Message('%s (new adserving domain code) - %s'%(domain, pub_name), sender=appconfig.MailData.FROM, recipients=[email])
                msg.body = ""
                msg.html = render_template('notify_email.html', domain=domain, publisher_name=pub_name, feed_url=feed_url, direct_url=direct_url, html_code=html_code)
                mail.send_email(msg)
        status = dbo.update_publisher_dt(ids)
        return jsonify({'data': status})
    except Exception as e:
        return jsonify({'data': e.message})

@application.route("/dashboardLogout")
@login_required
def dashboardLogout():
    logout_user()
    return redirect(url_for('dashboard'))

@application.route('/cbmpop') #services
def cbmpop():
    try:
        #pubid = int(request.args.get('id'))
        feedid = int(request.args.get('id'))
        delay = 0
        max = 3
        dur = 24 * 60 * 60
        default_url = ""
        #data = dbo.get_publisher_by_subid(pubid)
        data = dbo.get_publisher_by_feedid(feedid)
        if data == None:
            return "Error: wrong id"
        else:
            delay = data[5]
            max = data[6]
            dur = int(data[7]) * 60 * 60
            default_url = data[8] if data[8] != None else ""
            feed = data[3]
            auth = data[4]
            subid = data[2]
            url="https://xml.%s/redirect?feed=%s&auth=%s&pubid=%s&url=" % (str(appconfig.Domain.DOMAIN), str(feed), auth, subid)

        return render_template('pop_templatex.js', PAR_TRGURL=url, PAR_DELAY=delay, PAR_MAX=max, PAR_DUR=dur, PAR_DEFURL=default_url)
    except Exception as e:
        return "Error: %s" % e.message

@application.route('/rtbpush') #services
def rtbpush():
    try:
        return render_template('push.js')
    except Exception as e:
        return "Error: %s" % e.message

@application.route('/cbmxmr')
def cbmxmr():
    return render_template('cbmxmr.html')



@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404    

@application.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if False != False:
            flash('All fields are required.')
            return render_template('contact-us.html', form=form, page="contact")
        else:
            msg = Message(form.subject.data, sender=appconfig.MailData.FROM, recipients=appconfig.MailData.TO)
            msg.body = ""
            msg.html = render_template('contact_email.html', name=form.name.data, subject=form.subject.data, website=form.website.data, message=form.message.data, email=form.email.data)
            try:
            	mail.send_email(msg)
            	return render_template('contact-us.html', success=True, page="contact")
            except:
            	form=ContactForm()
            	return render_template('contact-us.html',  form=form, error=True, page="contact")
            

    elif request.method == 'GET':
        return render_template('contact-us.html', form=form, success=None, page="contact")

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if False != False:
            flash('All fields are required.')
            return render_template('signup.html', form=form, page="signup")
        else:
            msg = Message('Sign up request', sender=appconfig.MailData.FROM, recipients=appconfig.MailData.TO)
            msg.body = ""
            msg.html = render_template('signup_email.html', fname=form.fname.data, lname=form.lname.data, skype=form.skype.data, website=form.website.data, username=form.username.data, \
                email=form.email.data, password=form.password.data, repassword=form.repassword.data, account_type=form.account_type.data)
            try:
                mail.send_email(msg)
                return render_template('signup.html', success=True, page="signup")
            except:
                form = SignUpForm()
                return render_template('signup.html',  form=form, error=True, page="signup")
            

    elif request.method == 'GET':
        return render_template('signup.html', form=form, success=None, page="signup")

@application.route('/robots.txt')
@application.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(application.static_folder, request.path[1:])
        
if __name__ == "__main__":
    application.run()
