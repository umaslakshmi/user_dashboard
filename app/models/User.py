""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if len(info['first_name']) < 2:
            errors.append("First name must be at least 2 characters")
        elif not (info['first_name']).isalpha():
            errors.append("First name must contain only letters")
        if len(info['last_name']) < 2:
            errors.append("Last name must be at least 2 characters")
        elif not (info['last_name']).isalpha():
            errors.append("Last name must contain only letters")
        if not EMAIL_REGEX.match(info['email']):
            errors.append("Invalid email format")
        if len(info['password']) < 8:
            errors.append("Password must be at least 8 characters")
        elif info['password'] != info['confirm_password']:
            errors.append("Passwords do not match")

        if errors:
            return {'status': False, 'errors': errors}

        #check if first user
        check_query = 'SELECT * FROM users'
        users = self.db.query_db(check_query)
        if users:
            #insert new normal user
            query = 'INSERT INTO users (first_name, last_name, email, pw_hash, description, created_at, updated_at, user_level) VALUES (:first_name, :last_name, :email, :pw_hash, :description, NOW(), NOW(), :user_level)'
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'pw_hash': self.bcrypt.generate_password_hash(info['password']),
                'description': '',
                'user_level': 1
            }
        else:
            #insert admin user
            query = 'INSERT INTO users (first_name, last_name, email, pw_hash, description, created_at, updated_at, user_level) VALUES (:first_name, :last_name, :email, :pw_hash, :description, NOW(), NOW(), :user_level)'
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'pw_hash': self.bcrypt.generate_password_hash(info['password']),
                'description': '',
                'user_level': 9
            }
        self.db.query_db(query, data)
        return_query = 'SELECT * FROM users ORDER BY id DESC LIMIT 1'
        users = self.db.query_db(return_query)
        return {'status': True, 'user': users[0]}

    def get_user_by_id(self, id):
        query = 'SELECT * FROM users WHERE id=:id'
        data = {'id': id}
        users = self.db.query_db(query, data)
        return users[0]

    def get_users(self):
        query = 'SELECT * FROM users'
        return self.db.query_db(query)

    def check_user(self, info):
        query = 'SELECT * FROM users WHERE email=:email'
        data={'email': info['email']}
        users = self.db.query_db(query, data)
        if users:
            user = users[0]
            if self.bcrypt.check_password_hash(user['pw_hash'], info['password']):
                return user
        return False

    def update_user(self, info, id):
        if info['field'] == 'info':
            query = 'UPDATE users SET email=:email, first_name=:first_name, last_name=:last_name, user_level=:user_level, updated_at=NOW() WHERE id=:id'
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'user_level': info['user_level'],
                'id': id
            }
        elif info['field'] == 'password':
            query = 'UPDATE users SET password=:password, updated_at=NOW() WHERE id=:id'
            data = {'password': self.bcrypt.generate_password_hash(info['password']), 'id': id}
        elif info['field'] == 'description':
            query = 'UPDATE users SET description=:description WHERE id=:id'
            data = {'description': info['description'], 'id': id}
        return self.db.query_db(query, data)

    def delete_user(self, id):
        query = 'DELETE FROM users WHERE id=:id'
        data={'id': id}
        return self.db.query_db(query, data)


    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """