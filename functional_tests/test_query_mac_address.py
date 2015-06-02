import unittest
from time import sleep
from func_test_config import BaseTest

__author__ = 'Aaron Olson <aaron.olson@agosto.com>'

class QueryMacAddress(BaseTest):
    def test_query_mac_address(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_id("navbar-api-testing").click()
        driver.find_element_by_id("macAddress").send_keys("01:23:45:67:89:ab")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector("button.confirm").click()
