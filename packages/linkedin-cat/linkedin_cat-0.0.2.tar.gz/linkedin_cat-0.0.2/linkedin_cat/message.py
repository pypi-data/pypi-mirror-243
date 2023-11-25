import time
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from colorama import Fore, Style
from typing import List
from .base import LinkedinBase

class LinkedinMessage(LinkedinBase):
    """
    Encapsulates the functionality related to interacting with
    LinkedIn using Selenium.
    """
    def __int__(self,linkedin_cookies_json:str,headless = False):
        super().__init__(linkedin_cookies_json,headless)

    def open_linkedin_url(self,url):
        try:
            # Wait for a short duration
            self.short_wait()

            # Get the URL
            print(Fore.GREEN + f"Opening Linkedin URL: {url}" + Style.RESET_ALL)
            self.driver.get(url)

            # Wait for a medium duration
            self.medium_wait()

            # Scroll to the middle of the page
            print(Fore.GREEN + "Scrolling to the middle of the page" + Style.RESET_ALL)
            self.scroll_to_middle()

            # Wait for a short duration
            self.medium_wait()

            # Scroll to a random position
            print(Fore.GREEN + "Scrolling to a random position" + Style.RESET_ALL)
            self.scroll_to_random()

            # Wait for a short duration
            self.medium_wait()

            # Scroll to the bottom of the page
            print(Fore.GREEN + "Scrolling to the bottom of the page" + Style.RESET_ALL)
            self.scroll_to_bottom()

            # Wait for a short duration
            self.medium_wait()

            # Scroll to the top of the page
            print(Fore.GREEN + "Scrolling to the top of the page" + Style.RESET_ALL)
            self.scroll_to_top()

            # Wait for a medium duration
            self.short_wait()
        except Exception as e:
            # If an exception occurs, print an error message
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
    def send_connection_request(self, message):
        """
        Sends a connection request to a LinkedIn profile.

        Returns: True if connection request was successful, False otherwise.

        Parameter message: The connection message being sent.
        Precondition: message must be a String where len(message) <= 300.
        """
        try:
            print(Fore.GREEN + "Locating the 'Connect' button" + Style.RESET_ALL)
            connect_button = self.driver.find_element(By.XPATH, "(//button[contains(@aria-label, 'Invite') "
                                                                "and contains(@class, 'pvs-profile-actions__action')])")
            connect_button.click()
            self.medium_wait()
            print(Fore.GREEN + "Clicked on the 'Connect' button" + Style.RESET_ALL)

            print(Fore.GREEN + "Locating the 'Add a note' button" + Style.RESET_ALL)
            add_note_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
            add_note_button.click()
            self.medium_wait()
            print(Fore.GREEN + "Clicked on the 'Add a note' button" + Style.RESET_ALL)

            print(Fore.GREEN + "Locating the message entry field" + Style.RESET_ALL)
            message_entry = self.driver.find_element(By.XPATH, "//textarea[@name='message']")
            message_entry.send_keys(message)
            self.medium_wait()
            print(Fore.GREEN + "Typed the message" + Style.RESET_ALL)

            print(Fore.GREEN + "Locating the 'Send now' button" + Style.RESET_ALL)
            send_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
            send_button.click()
            self.medium_wait()
            print(Fore.GREEN + "Clicked on the 'Send now' button" + Style.RESET_ALL)

            print(Fore.GREEN + "Verifying if connection request is sent" + Style.RESET_ALL)
            self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Pending') "
                                               "and contains(@class, 'pvs-profile-actions__action') "
                                               "and .//span[contains(@class, 'artdeco-button__text') "
                                               "and text()='Pending']]")
            print(Fore.GREEN + "Connection request sent" + Style.RESET_ALL)
            return True

        except NoSuchElementException:
            print(Fore.RED + "Failed to send connection request" + Style.RESET_ALL)
            return False

    def more_then_connect(self, message):
        """
        Sends a conenction request to a LinkedIn profile when the blue
        connection button isn't visible.

        Returns: True if the connection request was successful, False otherwise.

        Parameter message: The connection message being sent.
        Precondition: message must be a String where len(message) <= 300.
        """
        try:
            print(Fore.GREEN + "Locating and clicking the 'More' button" + Style.RESET_ALL)
            more_button = self.driver.find_element(By.XPATH, "(//button[contains(@class, 'artdeco-dropdown__trigger') "
                                                             "and contains(@class, 'artdeco-dropdown__trigger--placement-"
                                                             "bottom') and contains(@class, 'ember-view') and contains(@class,"
                                                             " 'pvs-profile-actions__action') and contains(@class, "
                                                             "'artdeco-button') and contains(@class, "
                                                             "'artdeco-button--secondary') and contains(@class, "
                                                             "'artdeco-button--muted') and contains(@class,"
                                                             " 'artdeco-button--2') and @aria-label='More actions'])[2]")
            more_button.click()
            self.driver.execute_script("window.scrollBy(0, 300)")
            self.medium_wait()
            print(Fore.GREEN + "Clicked on the 'More' button" + Style.RESET_ALL)

            print(Fore.GREEN + "Locating and clicking the 'Connect' button" + Style.RESET_ALL)
            connect_button = self.driver.find_element(By.XPATH, "(//div[contains(@aria-label, 'Invite') and "
                                                                "contains(@aria-label, 'to connect')])")
            self.driver.execute_script("arguments[0].click();", connect_button)
            self.medium_wait()
            print(Fore.GREEN + "Clicked on the 'Connect' button" + Style.RESET_ALL)

            print(Fore.GREEN + "Locating and clicking the 'Add a note' button" + Style.RESET_ALL)
            add_note_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
            add_note_button.click()
            self.medium_wait()
            print(Fore.GREEN + "Clicked on the 'Add a note' button" + Style.RESET_ALL)

            print(Fore.GREEN + "Locating the message entry field" + Style.RESET_ALL)
            message_entry = self.driver.find_element(By.XPATH, "//textarea[@name='message']")
            message_entry.send_keys(message)
            self.medium_wait()
            print(Fore.GREEN + "Typed the message" + Style.RESET_ALL)

            print(Fore.GREEN + "Locating and clicking the 'Send now' button" + Style.RESET_ALL)
            send_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
            send_button.click()
            self.medium_wait()
            print(Fore.GREEN + "Clicked on the 'Send now' button" + Style.RESET_ALL)

            print(Fore.GREEN + "Verifying if connection request is sent" + Style.RESET_ALL)
            self.driver.find_element('xpath', "//div[contains(@aria-label, 'Pending') and "
                                              "contains(@class, 'artdeco-dropdown__item')]")
            print(Fore.GREEN + "Connection request sent" + Style.RESET_ALL)
            return True

        except WebDriverException:
            print(Fore.RED + "Failed to send connection request" + Style.RESET_ALL)
            return False

    def is_friend(self):
        try:
            print(Fore.GREEN + "Checking friend status" + Style.RESET_ALL)
            friend_status = self.driver.find_element(By.XPATH,
                                                     "//span[contains(@class, 'distance-badge')]/span[contains(@class, 'dist-value')]")
            if friend_status.text.strip() == "1st":
                print(Fore.GREEN + "Friend status: True" + Style.RESET_ALL)
                return True
            else:
                print(Fore.GREEN + "Friend status: False" + Style.RESET_ALL)
                return False
        except NoSuchElementException:
            print(Fore.RED + "Friend status: Element not found" + Style.RESET_ALL)
            return False
        finally:
            self.short_wait()

    def is_pending(self):
        try:
            print(Fore.GREEN + "Checking pending status" + Style.RESET_ALL)
            pending_status = self.driver.find_element(By.XPATH, ("//button[contains(@aria-label, 'Pending') and "
                                                                 "contains(@class, 'pvs-profile-actions__action') and .//span[contains(@class, "
                                                                 "'artdeco-button__text') and text()='Pending']]"))
            print(Fore.GREEN + "Pending status: True" + Style.RESET_ALL)
            return True
        except NoSuchElementException:
            print(Fore.GREEN + "Pending status: False" + Style.RESET_ALL)
            return False
        finally:
            self.short_wait()

    def has_connect_button(self):
        """
        Checks if LinkedIn gives the user the option to connect with the current profile.

        Returns: True if the profile has the conenct button, False otherwise.
        """
        try:
            connect = self.driver.find_element(By.XPATH,
                                               "(//span[@class='artdeco-button__text'])[6]")
            connect_following = self.driver.find_element(By.XPATH,
                                                         "(//span[@class='artdeco-button__text'])[8]")
            if connect.text == "Connect" or connect_following.text == "Connect":
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def has_hidden_connect_button(self):
        """
        Checks if the user can send a request after clicking more.

        Returns True if the profile has a hidden connect button, False otherwise.
        """
        try:
            self.driver.find_element(By.XPATH,
                                     ("(//div[contains(@class, 'artdeco-dropdown__item') and "
                                      "contains(@class, 'artdeco-dropdown__item--is-dropdown')"
                                      " and contains(@class, 'ember-view') and contains(@class,"
                                      " 'full-width') and contains(@class, 'display-flex') and"
                                      " contains(@class, 'align-items-center')]/"
                                      "span[text()='Connect'])[1]"))
            return True
        except NoSuchElementException:
            return False

    def generate_message(self,message:str):
        """
        Extracts the first name from the LinkedIn profile page,
        then assembles the personalized message to send. Allows the
        user the put [FULL NAME] and [FIRST NAME] in their message to instruct the
        program to automatically insert the profile's name.

        Returns: A String representing the personalized connection message.
        """
        full_name = self.driver.find_element(By.XPATH,
                                             ('(//h1[@class="text-heading-xlarge inline t-24'
                                              ' v-align-middle break-words"])[1]')).text
        name_list = full_name.split(" ")
        first = name_list[0]
        if first.lower() not in ['dr.', 'mr.' 'mrs.',
                                 'ms.', 'dr', 'mr', 'mrs' 'ms']:
            first_name = name_list[0]
        else:
            first_name = name_list[1]

        msg = message.replace('FULLNAME', full_name)
        msg = msg.replace('FIRSTNAME', first_name)
        return msg.strip()

    def send_msg_to_friend(self,message:str):
        msg_button = self.driver.find_element(By.XPATH,("(//button[contains(@aria-label,'Message') and contains(@class, 'pvs-profile-actions__action')])"))
        msg_button.click()
        time.sleep(random.uniform(3, 5))
        msg_box = self.driver.find_element(By.XPATH, "//div[@contenteditable='true']/p")
        msg_box.click()
        last_msg = self.find_last_message()

        if last_msg == message:
            print(Fore.RED + f'Message already sent:{last_msg}' +  Style.RESET_ALL)
            return

        time.sleep(random.uniform(3, 5))
        msg_box.send_keys(message)
        send_button =  self.driver.find_element(By.XPATH, ("(//button[contains(@class,'msg-form__send-button') and contains(@type, 'submit')])"))
        time.sleep(random.uniform(1, 3))
        send_button.click()
        time.sleep(random.uniform(1, 3))
        print(Fore.BLUE + f'Message successfully sent:{message}'+ Style.RESET_ALL)

    def send_single_request(self, url: str, message: str):
        try:
            print(Fore.BLACK + "="*30 + " Sending Request "+ "="*30 + Style.RESET_ALL)
            self.open_linkedin_url(url)

            msg = self.generate_message(message)
            print(Fore.BLUE + "Generating message:", msg + Style.RESET_ALL)

            while self.is_msg_box_exist():
                print(Fore.YELLOW + "Message box exists, Closing it now" + Style.RESET_ALL)
                self.close_msg_box()

            if self.is_friend():
                print(Fore.GREEN + "Sending message to friend" + Style.RESET_ALL)
                self.send_msg_to_friend(msg)
                return

            if self.is_pending():
                print(Fore.YELLOW + 'Connection request is pending:', url + Style.RESET_ALL)
                return

            if self.has_hidden_connect_button():
                print(Fore.GREEN + "Taking more than connect action" + Style.RESET_ALL)
                self.more_then_connect(msg)
            else:
                print(Fore.GREEN + "Sending connection request" + Style.RESET_ALL)
                self.send_connection_request(msg)
        except Exception as e:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
        finally:
            time.sleep(random.uniform(1, 3))

    def send_multi_request(self, url_list: List[str], message: str):
        try:
            for url in url_list:
                self.send_single_request(url,message)
        except Exception as e:
            print(Fore.RED + f'Error: {e}' + Style.RESET_ALL)
        finally:
            self.close_driver()

    def is_msg_box_exist(self):
        try:
            self.driver.find_element(By.XPATH,
                                                '(//button[contains(@class,"msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted")])')
            return True
        except NoSuchElementException:
            return False
    def close_msg_box(self):
        try:
            while True:
                self.medium_wait()
                if self.is_msg_box_exist():
                    print(Fore.GREEN + "Locating and clicking the 'Close' button" + Style.RESET_ALL)
                    close_button = self.driver.find_element(By.XPATH,
                                                            '(//button[contains(@class, "msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted")])')
                    close_button.click()
                else:
                    break
                self.short_wait()
        except NoSuchElementException:
            print(Fore.RED + "Failed to close the message box" + Style.RESET_ALL)

    def find_last_message(self):
        try:
            messages = self.driver.find_elements(By.CSS_SELECTOR,'.msg-s-event__content')
            if messages:
                last_message = messages[-1].find_element(By.TAG_NAME, 'p').text
                return last_message.strip()
        except NoSuchElementException:
            return False

    def close_driver(self):
        self.driver.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()