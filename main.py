from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


class FacebookLogin:
    """To Open Facebook.com and login with it"""

    def __init__(self, driver, url="https://www.facebook.com/"):
        self.driver = driver
        self.url = url

    def navigate(self):
        self.driver.get(self.url)
        print("Navigate for login")

    def login(self, username, password):
        username_field = self.driver.find_element(By.ID, "email")
        password_field = self.driver.find_element(By.ID, "pass")
        login_button = self.driver.find_element(By.NAME, "login")

        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button.click()

        print("Login Clicked..")

        time.sleep(5)


class FacebookPost:
    """Open facebook.com click on post box to popup post form and submit the new post."""

    def __init__(self, driver, url="https://www.facebook.com/"):
        self.driver = driver
        self.url = url

    def navigate(self):
        self.driver.get(self.url)
        print("Navigate for post")

    def send_post(self, post_content):

        print("send_post begin...")

        post_popup = self.driver.find_element(By.XPATH, f"//div[./div/span[contains(text(), 's on your mind,')]]")
        post_popup.click()
        time.sleep(1)

        post_message_element = self.driver.find_element(By.XPATH, "//form//p[contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm')]")

        post_message_element.send_keys(post_content)

        post_button = self.driver.find_element(By.XPATH, '//div[@aria-label="Post"]')
        post_button.click()


class ExcelSheetReader:
    """To read excel sheet from local device and return a list."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read_file(self):
        try:
            self.data = pd.read_excel(self.file_path)
        except Exception as e:
            print(f"Error reading Excel file: {e}")

    def get_posts(self):
        if self.data is not None:
            try:
                posts = self.data["Post Message"].tolist()

                return list(set(posts))
            except KeyError:
                print("The Excel sheet does not contain a 'Message' column.")
                return []
        else:
            print("No data loaded.")
            return[]


class FacebookAutomation:

    """Manage all automation steps, login facebook, read excel and send post."""
    def __init__(self, driver, username, password, file_path):
        self.driver = driver
        self.username = username
        self.password = password
        self.file_path = file_path
        self.posts = None

    def execute(self):
        """Execute the login and post process."""
        # Login to Facebook
        login_page = FacebookLogin(self.driver)
        login_page.navigate()
        login_page.login(self.username, self.password)

        excel_sheet_reader = ExcelSheetReader(self.file_path)
        excel_sheet_reader.read_file()
        self.posts = excel_sheet_reader.get_posts()

        # Create a post in facebook
        post_page = FacebookPost(self.driver)
        post_page.navigate()
        for post in self.posts:
            post_page.send_post(post)
            time.sleep(2)


if __name__ == "__main__":
    # Set up the WebDriver (Make sure to have chromedriver installed and in your PATH)

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")

    service = Service(executable_path="C:\\chromedriver-win64\\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Facebook credentials and post content (replace with real credentials)
    username = "test@example.com"
    password = "test password"
    file_path = "facebook_posts1.xlsx"

    # Create an instance of the automation class
    automation = FacebookAutomation(driver, username, password, file_path)

    # Run the automation
    automation.execute()

    # Keep the browser open for inspection (Optional)
    input("Press Enter to close the browser...")

    # Quit the driver
    driver.quit()

