"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Message')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('/users/index.html')

    def signin(self):
        return self.load_view('/users/signin.html')

    def login(self):
        info = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        result = self.models['User'].check_user(info)
        if result:
            session['id'] = result['id']
            session['user_level'] = result['user_level']
            return redirect('/users/dashboard')
        else:
            flash("Error logging in")
            return redirect('/users/signin')

    def register(self):
        return self.load_view('/users/register.html')

    def logout(self):
        session.pop('id')
        session.pop('user_level')
        return redirect('/')

    def create(self):
        print request.form
        info = {
            'first_name': request.form['first-name'],
            'last_name': request.form['last-name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_password': request.form['confirm-password']
        }
        result = self.models['User'].create_user(info)
        if result['status']:
            session['id'] = result['user']['id']
            #redirect to user's homepage
            return redirect('/users/dashboard')
        else:
            for error in result['errors']:
                flash(error)
            return redirect('/users/register')

    def dashboard(self):
        user = self.models['User'].get_user_by_id(session['id'])
        all_users = self.models['User'].get_users()
        return self.load_view('/users/dashboard.html', user=user, all_users=all_users)

    def new(self):
        return self.load_view('/users/new.html')

    def edit(self, id):
        user = self.models['User'].get_user_by_id(id)
        return self.load_view('/users/edit.html', user=user)

    def update(self, id):
        if request.form['field'] == 'info':
            if session['user_level'] == 9:
                if request.form['user-level'] == 'admin':
                    level = 9
                else:
                    level = 1
                info = {
                    'field': request.form['field'],
                    'email': request.form['email'],
                    'first_name': request.form['first-name'],
                    'last_name': request.form['last-name'],
                    'user_level': level
                }
            else:
                info = {
                    'field': request.form['field'],
                    'email': request.form['email'],
                    'first_name': request.form['first-name'],
                    'last_name': request.form['last-name'],
                }
        elif request.form['field'] == 'password':
            info = {
                'field': request.form['field'],
                'password': request.form['password']
            }
        elif request.form['field'] == 'description':
            info = {
                'field': request.form['field'],
                'description': request.form['description']
            }
        self.models['User'].update_user(info, id)
        return redirect('/users/dashboard')

    def destroy(self, id):
        self.models['User'].delete_user(id)
        return redirect('/users/dashboard')

    def show(self, id):
        user = self.models['User'].get_user_by_id(id)
        #change to join
        messages = self.models['Message'].get_messages_for_wall(id)
        comments = self.models['Message'].get_comments_for_wall(id)
        return self.load_view('/users/wall.html', user=user, messages=messages, comments=comments)
