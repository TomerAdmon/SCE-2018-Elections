import unittest
from app import app

class AuthenticationTest(unittest.TestCase):
# dlsfds
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.check = app.test_client(self)

    #######################################
    def login_without_id(self):
        return self.check.post('login',
                                data=dict(first_name='aa', last_name='aa')
                               )

    def test_login_without_id(self):
        rv = self.login_without_id()
        self.assertEqual(rv.status_code, 400)
    #######################################

    #######################################
    def manager_access_by_url(self):
        return self.check.get('/admin')

    def test_manager_access_by_url(self):
        rv = self.manager_access_by_url()
        self.assertEqual(rv.status_code, 404)
    #######################################


    #######################################
    def not_registered_user(self):
        return self.check.post('login',data=dict(first_name='example', last_name='example',id_num ='123456789'))


    def test_not_registered_user(self):
        rv = self.not_registered_user()
        assert 'The user is not registered!' in rv.data
    #######################################

    def tearDown(self):
        del self.check
        self.app_context.pop()

if __name__ == '__main__':
  unittest.main()
