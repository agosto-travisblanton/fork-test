import unittest
from func_test_config import BaseTest

class AddTenant(BaseTest):

    def test_(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.save_screenshot(self.screenshot_dir + "tenant.png")

        driver.find_element_by_id("submit-login").click()

        driver.find_element_by_id("navbar-tenants").click()
        driver.find_element_by_id("button-add-tenant").click()

        driver.find_element_by_id("tenantName").clear()
        driver.find_element_by_id("tenantName").send_keys("Luke")
        driver.find_element_by_id("adminEmail").clear()
        driver.find_element_by_id("adminEmail").send_keys("luke.skywalker@agosto.com")
        driver.find_element_by_id("chromeDeviceDomain").clear()
        driver.find_element_by_id("chromeDeviceDomain").send_keys("Kessel Run")
        driver.find_element_by_id("contentServerUrl").clear()
        driver.find_element_by_id("contentServerUrl").send_keys("jedi.com")
        driver.find_element_by_id("active").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()

if __name__ == "__main__":
    unittest.main()
