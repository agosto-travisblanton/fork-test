import unittest
from func_test_config import BaseTest

__author__ = 'Aaron Olson <aaron.olson@agosto.com>'

class AddDevice(BaseTest):

    def test_add_device(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.save_screenshot(self.screenshot_dir + "tenant.png")

        driver.find_element_by_id("submit-login").click()

        driver.find_element_by_xpath("//a[@id='navbar-domains']/i[2]").click()
        driver.find_element_by_id("navbar-domains").click()
        driver.find_element_by_id("skykit-domain").click()
        driver.find_element_by_id("button-add-device").click()
        driver.find_element_by_id("device-name").send_keys("R2D2")
        driver.find_element_by_id("device-location").send_keys("Space")
        driver.find_element_by_id("mac-address").send_keys("000:875:123")
        driver.find_element_by_id("device-id").send_keys("1234567890")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector("button.confirm").click()

if __name__ == "__main__":
    unittest.main()
