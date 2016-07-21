from system.core.controller import *

class Messages(Controller):
    def __init__(self, action):
        super(Messages, self).__init__(action)
        self.load_model('Message')
        self.db = self._app.db

    def create(self, id):
    	print request.form
    	info = {'message': request.form['message']}
    	self.models['Message'].create_message(info, id, session['id'])
    	ret = '/users/show/{}'.format(id)
    	return redirect(ret)

    def create_comment(self, message_id):
        print request.form
        info = {
            'comment': request.form['comment']
        }
        message = self.models['Message'].get_message_by_id(message_id)
        self.models['Message'].create_comment(info, message_id, session['id'])
        ret = "/users/show/{}".format(message['wall_id'])
        return redirect(ret)