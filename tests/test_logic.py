import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from flask import Flask
from flask_testing import LiveServerTestCase
from app.models import User, Party
from app import app , db




class SeleniumTest(LiveServerTestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True


    def init_db(self):
        db.session.commit()
        testUser = User('test', 'me',123456789,0,0)
        db.session.add(testUser)
        db.session.commit()


    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        db.init_app(app)
        with app.app_context():
            db.create_all()
            self.init_db()
        return app



    def setUp(self):
         self.browser = webdriver.PhantomJS(executable_path="./phantomjs")
         self.browser.get(self.get_server_url())
         self.msg = 'The user is not registered!'


    def test_registered_user(self):
        first_name = self.browser.find_element_by_id("first_name")
        first_name.send_keys("test")

        last_name = self.browser.find_element_by_id("last_name")
        last_name.send_keys("me")

        id_num = self.browser.find_element_by_id("id_num")
        id_num.send_keys(123456789)

        submit = self.browser.find_element_by_id("submit")
        submit.click()

        assert self.msg not in self.browser.page_source
        self.browser.save_screenshot('registered_user.png')

    def test_unregistered_user(self):
        first_name = self.browser.find_element_by_id("first_name")
        first_name.send_keys("test1")

        last_name = self.browser.find_element_by_id("last_name")
        last_name.send_keys("me1")

        id_num = self.browser.find_element_by_id("id_num")
        id_num.send_keys(123456788)

        submit = self.browser.find_element_by_id("submit")
        submit.click()

        assert self.msg in self.browser.page_source
        self.browser.save_screenshot('unregistered_user.png')



    def tearDown(self):
        self.browser.quit()
        with app.app_context():
            db.drop_all()
            db.session.remove()

if __name__ == '__main__':
    unittest.main()