import unittest
from time import sleep
from func_test_config import BaseTest


__author__ = 'Aaron Olson <aaron.olson@agosto.com>'

class AddTenant(BaseTest):

    def test_1_add_tenant(self):
        driver = self.driver

        driver.find_element_by_id("navbar-tenants").click()
        driver.find_element_by_id("button-add-tenant").click()

        driver.find_element_by_id("tenantName").send_keys("Luke")
        driver.find_element_by_id("adminEmail").send_keys("luke.skywalker@agosto.com")
        driver.find_element_by_id("chromeDeviceDomain").send_keys("Tatooine")
        driver.find_element_by_id("contentServerUrl").send_keys("jedi.com")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(.3)

        self.assertTrue(driver.find_element_by_class_name("tenant-name").text == u"Luke")
        self.assertTrue(driver.find_element_by_class_name("tenant-admin-email").text == u"luke.skywalker@agosto.com")
        self.assertTrue(driver.find_element_by_class_name("content-server-url").text == u"jedi.com")

    def test_2_edit_tenant(self):
        driver = self.driver
        driver.find_element_by_id("navbar-tenants").click()
        driver.find_element_by_name("edit-tenant").click()
        driver.find_element_by_id("tenantName").clear()
        driver.find_element_by_id("tenantName").send_keys("Yoda")
        driver.find_element_by_id("adminEmail").clear()
        driver.find_element_by_id("adminEmail").send_keys("yoda@agosto.com")
        driver.find_element_by_id("chromeDeviceDomain").clear()
        driver.find_element_by_id("chromeDeviceDomain").send_keys("")
        driver.find_element_by_id("chromeDeviceDomain").clear()
        driver.find_element_by_id("chromeDeviceDomain").send_keys("Dagobah")
        driver.find_element_by_id("contentServerUrl").clear()
        driver.find_element_by_id("contentServerUrl").send_keys("yoda.com")
        driver.find_element_by_css_selector("div.form-group.ng-binding > label").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        sleep(.3)

        self.assertTrue(driver.find_element_by_class_name("tenant-name").text == u"Yoda")
        self.assertTrue(driver.find_element_by_class_name("tenant-admin-email").text == u"yoda@agosto.com")
        self.assertTrue(driver.find_element_by_class_name("content-server-url").text == u"yoda.com")

    def test_3_delete_tenant(self):
        driver = self.driver
        driver.find_element_by_id("navbar-tenants").click()
        driver.find_element_by_name("delete-tenant").click()



if __name__ == "__main__":
    unittest.main()
