from system.core.model import Model

class Message(Model):
    def __init__(self):
        super(Message, self).__init__()

    def create_message(self, info, wall_id, user_id):
    	query = 'INSERT INTO messages (message, created_at, user_id, wall_id) VALUES (:message, NOW(), :user_id, :wall_id)'
    	data = {
    		'message': info['message'],
    		'wall_id': wall_id,
    		'user_id': user_id
    	}
    	return self.db.query_db(query, data)

    def get_messages(self):
    	query = 'SELECT * FROM messages'
    	return self.db.query_db(query)

    def get_message_by_id(self, id):
        query = 'SELECT * FROM messages WHERE id=:id'
        data = {'id': id}
        messages = self.db.query_db(query, data)
        return messages[0]

    def get_messages_for_wall(self, id):
    	query = 'SELECT messages.id, users.first_name, users.last_name, messages.message, messages.created_at FROM messages JOIN users ON messages.user_id = users.id WHERE messages.wall_id = :id ORDER BY messages.created_at DESC'
    	data = {'id': id}
    	return self.db.query_db(query, data)

    def create_comment(self, info, message_id, user_id):
        query = 'INSERT INTO comments (comment, created_at, message_id, user_id) VALUES (:comment, NOW(), :message_id, :user_id)'
        data = {
            'comment': info['comment'],
            'message_id': message_id,
            'user_id': user_id
        }
        return self.db.query_db(query, data)

    def get_comments_for_wall(self, id):
        query = 'SELECT users.first_name, users.last_name, comments.comment, comments.created_at, messages.wall_id, messages.id AS "message_id" FROM comments JOIN users ON comments.user_id = users.id JOIN messages ON comments.message_id = messages.id WHERE messages.wall_id = :id ORDER BY comments.created_at ASC'
        data = {'id': id}
        comments = self.db.query_db(query, data)
        return comments
