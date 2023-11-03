import random
import requests
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles import finders
from selenium.webdriver.support.select import Select

from .models import Census, PointCategory


# class MySeleniumTests(StaticLiveServerTestCase):
#     # fixtures = ["user-data.json"]
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()
#         cls.selenium.implicitly_wait(10)
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()
#
#     def test_full_census(self):
#         self.selenium.get(f"{self.live_server_url}/census/f/1?city=Казань&street=Калинина&house=15к1&guid=00000000001&name=На%20посту/")
#         self.selenium.implicitly_wait(60)
#         self.selenium.find_element(By.ID, 'signboardId').send_keys("Motul")
#         self.selenium.find_element(By.ID, 'formFileMultiple').send_keys(finders.find('images/logo.jpg'))
#         # self.selenium.find_element(By.ID, 'formFileMultiple').submit()
#
#         nets = Select(self.selenium.find_element(By.ID, 'typeId'))
#
#         yes = self.selenium.find_element(By.CSS_SELECTOR, '#typeId>option[value="1"]')
#         no = self.selenium.find_element(By.CSS_SELECTOR, '#typeId>option[value="0"]')
#
#         nets.select_by_visible_text("Да")
#
#         self.assertEqual(yes.is_selected(), True)
#
#         nets.select_by_visible_text("Нет")
#         self.assertEqual(no.is_selected(), True)
