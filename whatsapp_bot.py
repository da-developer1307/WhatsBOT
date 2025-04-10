from datetime import time
import os
import re
# import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import requests
import threading
# import base64
# from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
# from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import pyqtSignal, QObject
from os import path, kill
from signal import SIGTERM
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess
from time import sleep
from selenium.webdriver.common.keys import Keys
from random import randint
# from PIL import Image
# import win32clipboard as clipboard
# from PyQt6.QtWidgets import QApplication

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")   
    return os.path.join(base_path, relative_path)


class WhatsAppBot(QObject):
    login_checked = pyqtSignal(bool)  # Signal to notify when login status is checked
    driver = None
    log_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def kill_existing_chrome(self):
        """Terminate only background Chrome or ChromeDriver processes likely related to Selenium."""
        print("kill_existing_chrome: Terminating any background Chrome or ChromeDriver processes...")

        for process in process_iter(['pid', 'name', 'cmdline']):
            try:
                process_name = process.info['name'].lower()
                cmdline = process.info.get('cmdline', [])

                # Check if the process is Chrome or ChromeDriver
                if 'chrome' in process_name or 'chromedriver' in process_name:
                    # Look for Selenium-related flags in cmdline
                    if '--remote-debugging-port' in ' '.join(cmdline) or 'chromedriver' in process_name:
                        kill(process.info['pid'], SIGTERM)
                        print(f"kill_existing_chrome: Terminated {process_name} (PID: {process.info['pid']})")
                    else:
                        print(f"kill_existing_chrome: Skipped {process_name} (PID: {process.info['pid']}) - Not Selenium-related")
            except (NoSuchProcess, AccessDenied, ZombieProcess) as e:
                print(f"kill_existing_chrome: Error processing PID {process.info.get('pid')}: {e}")



    def start_driver(self, isHeadless):
        """Start the Chrome driver after killing existing processes."""
        # First, kill any running Chrome processes
        self.kill_existing_chrome()

        """Start the Chrome driver."""
        print("start_driver: Starting the Chrome driver...")
        options = Options()

        user_data_dir = path.join(path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'WhatsBot')
        options.add_argument(f"user-data-dir={user_data_dir}")

        if isHeadless:
            options.add_argument("--headless")  # Run Chrome in headless mode
            options.add_argument("--no-sandbox")  # Required for headless mode in some environments
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-position=-2400,-2400")
        else:
            options.add_argument("--start-maximized")
            # options.add_argument("--window-position=-2400,-2400")

        service = Service(executable_path=resource_path("chromedriver.exe"))
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(30)
        print("start_driver: Chrome driver started.")

    # The rest of your code follows unchanged
    def open_whatsapp_web(self):
        """Open WhatsApp Web."""
        if self.driver is None:
            print("open_whatsapp_web: Driver not found. Starting the driver...")
            self.start_driver()

        print("open_whatsapp_web: Opening WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]'))  # Wait for the app to load
        )

    def check_login_status(self):
        """Check if the user is logged in to WhatsApp Web."""
        try:
            print("check_login_status: Checking if user is logged in...")
            WebDriverWait(self.driver, 12).until(
                EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan this QR code to link a device!']"))  # QR code element
            )
            print("check_login_status: User is not logged in.")
            return False  # User is not logged in
        except TimeoutException:
            print("check_login_status: User is logged in.")
            return True  # User is logged in

    def perform_login_check(self):
        """Perform the login check and emit signal."""
        login_status = self.check_login_status()
        self.close()
        self.login_checked.emit(login_status)

    def run_login_check(self, isHeadless):
        """Run the login check process step by step."""
        self.start_driver(isHeadless)           # Start the driver
        self.open_whatsapp_web()      # Open WhatsApp Web
        self.perform_login_check()     # Perform the login check

    def run_message_campaign(self, isHeadless ,contacts):
        """Run the message campaign process step by step."""

        
        contact_list = [contact_info["contact"] for contact_info in contacts]
        success_count=0
        failure_cpunt=0
        self.start_driver(isHeadless)           # Start the driver
        self.open_whatsapp_web()      # Open WhatsApp Web
        self.send_message(contacts)
        succes_count,failure_count =self.count_valid_invalid(contact_list)     # Send the message
        return succes_count,failure_count

        sleep(5)

    def run_media_campaign(self, isHeadless ,contacts):
        """Run the message campaign process step by step."""
        contact_list = [contact_info["contact"] for contact_info in contacts]
        success_count=0
        failure_cpunt=0        
        self.start_driver(isHeadless)           # Start the driver
        self.open_whatsapp_web()      # Open WhatsApp Web
        self.send_media(contacts)
        succes_count,failure_count =self.count_valid_invalid(contact_list)     # Send the media
        return succes_count,failure_count
        sleep(5)

    def run_media_and_message_campaign(self, isHeadless ,contacts):
        """Run the message campaign process step by step."""
        contact_list = [contact_info["contact"] for contact_info in contacts]
        success_count=0
        failure_cpunt=0        
        self.start_driver(isHeadless)           # Start the driver
        self.open_whatsapp_web()      # Open WhatsApp Web
        self.send_media_and_message(contacts)     # Send the media
        succes_count,failure_count =self.count_valid_invalid(contact_list)
        return succes_count,failure_count
        sleep(5)

    def close(self):
        """Close the browser."""
        if self.driver:
            print("close: Closing the browser...")
            self.driver.quit()
            self.driver = None
            print("close: Browser closed.")

    def perform_login(self, isHeadless):
        """Perform the login process with improved QR code handling."""
        try:
            options = Options()
            user_data_dir = path.join(path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'WhatsBot')
            options.add_argument(f"user-data-dir={user_data_dir}")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")

            if isHeadless:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-position=-2400,-2400")
            else:
                options.add_argument("--start-maximized")

            service = Service(executable_path=resource_path("chromedriver.exe"))
            self.driver = webdriver.Chrome(service=service, options=options)

            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

            self.driver.get("https://web.whatsapp.com")

            # Wait for QR code to be fully loaded
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, 'canvas'))
            )
            
            def check_window():
                while True:
                    try:
                        self.driver.current_window_handle
                        print("Browser window is still open")
                        sleep(1)
                    except:
                        # Window was closed
                        print("Browser window was closed")
                        self.login_checked.emit(True)
                        
                        # Close the driver
                        self.close()
                        break

            window_check_thread = threading.Thread(target=check_window)
            window_check_thread.daemon = True
            window_check_thread.start()

            # Bring window to foreground if not headless
            if not isHeadless:
                self.driver.execute_script("window.focus();")

            print("Please scan the QR code to login.")

        except Exception as e:
            print(f"Error in perform_login: {str(e)}")
            self.close()
            self.login_checked.emit(False)





    def perform_logout(self):
        """Delete the WhatsBot user data directory to logout the user."""
        try:
            import shutil
            from os import path
            
            # Get the path to the WhatsBot user data directory
            user_data_dir = path.join(path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'WhatsBot')
            
            # Check if the directory exists
            if path.exists(user_data_dir):
                # Delete the directory and all its contents
                shutil.rmtree(user_data_dir)
                print(f"perform_logout: Successfully deleted user data directory at {user_data_dir}")
                return True
            else:
                print("perform_logout: User data directory not found. User might already be logged out.")
                return False
                
        except Exception as e:
            print(f"perform_logout: Error while deleting user data: {str(e)}")
            return False

    def on_dialog_closed(self):
        """Function to call when the dialog is closed."""
        print("Dialog closed. You can add more functionality here.")
        # Add any additional code you want to execute when the dialog is closed
        self.perform_login_check()
        self.close()

    def is_driver_closed(self):
        """Check if the driver is closed."""
        if self.driver:
            try:
                self.driver.current_window_handle
                return False
            except WebDriverException:
                return True
            
    def send_media_and_message(self, contacts):
        """Send media and message to specified contacts."""
        """Send a message to specified contacts."""
        contact_list = [contact_info["contact"] for contact_info in contacts]
        valid, invalid = self.count_valid_invalid(contact_list)
        print(f"Valid Numbers: {valid}")
        print(f"Invalid Numbers: {invalid}")
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="chats-filled"]'))
            )
        except:
            print("No chat icon found")
            return
        k=0
        c=0
        t=0
        
        for index, contact_info in enumerate(contacts):

            t=(t+1)
            if (t%(100 +k )) == 0:
                k=(k+10)%40
                sleep(randint(300,600))

            contact = contact_info["contact"]
            message = contact_info["message"]
            media = contact_info["media"]

            if self.is_invalid(contact):
                continue            
            c = ( c + 1 ) % 10
            
            # Determine the heading based on the value of c
            if c == 1:
                heading = "Hey...did Jethalal inform you about this? Or you don't know about this yet???"
            elif c == 2:
                heading = "Imagine having access to something that completely revolutionizes how you [do a task]—sounds intriguing, right?"
            elif c == 6:
                heading = "What if I told you there exists this thing that you had never thought of? Yes, my dear..."
            elif c == 8:
                heading = "Sorry yrr, I know you've been waiting for this, and we could only tell you that we've done it for you..."
            elif c == 0:
                heading = "Roses are red, violets are blue... Only God knew that we would make this incredible product for you."
            elif c == 5:
                heading = "Hey… did Raj tell you about this? Or are you still in the dark?? 👀"    
            elif c == 3:
                heading = "Wait… you haven’t heard about this yet? 😳 Trust me, you NEED to know!"
            elif c == 7:
                heading = "Shocking! 😱 People are already taking advantage of this… and you?"
            elif c == 4:
                heading = "Guess what? 🧐 Everyone’s talking about this… but do YOU know yet?"
            elif c == 9:
                heading = "Psst… someone just told me something BIG! 🤯 Should I share it with you?"                
                       
            try:
                actions = ActionChains(self.driver)
                actions.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
                sleep(randint(1, 3))

                print(f"Attempting to send media and message to {contact}...")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Sending to: {contact}")

                # Open new chat window
                actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
                sleep(randint(1, 3))
                actions.send_keys(contact).perform()
                sleep(randint(1, 3))
                actions.send_keys(Keys.ENTER).perform()

                # Step 1: Click the attachment button (paperclip icon)
                print("Clicking attachment button...")
                attachment_button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="plus"]'))
                )
                attachment_button.click()

                # Step 2: Locate the file input element for image/video upload
                print("Locating the file input element for media upload...")
                file_input = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//input[contains(@accept, "image/") or contains(@accept, "video/")]'))
                )

                # Step 3: Send the file path directly to the file input
                print(f"Uploading file: {media}")
                file_input.send_keys(media)  # Provide the absolute file path of the media file
                sleep(randint(1, 5))  # Ensure media is uploaded before proceeding
                

                # Send the heading and original message
                actions.send_keys(heading).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                sleep(randint(1, 3))

                # Add message text
                lines = message.split('\n')
                for line in lines:
                    actions.send_keys(line).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                sleep(randint(1, 3))
                actions.send_keys(Keys.ENTER).perform()

                print(f"Media and message sent to {contact}.")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Media and message sent to {contact} successfully.")

                sleep(randint(1, 2))

                # Take longer breaks after every 15 messages
                if (index + 1) % 15 == 0:
                    long_sleep = randint(20, 25)
                    print(f"Taking a longer break of {long_sleep} seconds...")
                    self.log_message.emit(f"[{index + 1}/{len(contacts)}] Taking a longer break of {long_sleep} seconds...")
                    sleep(long_sleep)

            except (TimeoutException, Exception) as e:
                print(f"An error occurred while sending media and message to {contact}: {str(e)}")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Failed to send media and message to {contact}")



            
    def send_media(self, contacts):
        """Send media to specified contacts."""
        """Send a message to specified contacts."""
        contact_list = [contact_info["contact"] for contact_info in contacts]
        valid, invalid = self.count_valid_invalid(contact_list)
        print(f"Valid Numbers: {valid}")
        print(f"Invalid Numbers: {invalid}")
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="chats-filled"]'))
            )
        except:
            print("No chat icon found")
            return
        k=0
        c=0
        t=0
      
        for index, contact_info in enumerate(contacts):

            t=(t+1)
            if (t%(100 +k )) == 0:
                k=(k+10)%40
                sleep(randint(300,600))

            contact = contact_info["contact"]
            media = contact_info["media"]
            if self.is_invalid(contact):
                continue            

            
            try:
                actions = ActionChains(self.driver)

                actions.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
                sleep(randint(1, 3))
                
                print(f"Attempting to send media to {contact}...")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Sending to: {contact}")

                # Open new chat window
                actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
                sleep(randint(1, 3))
                actions.send_keys(contact).perform()
                sleep(randint(1, 3))
                actions.send_keys(Keys.ENTER).perform()

                # Step 1: Click the attachment button (paperclip icon)
                print("Clicking attachment button...")
                attachment_button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="plus"]'))
                )
                attachment_button.click()

                # Step 2: Locate the correct file input element for image/video upload
                print("Locating the file input element for media upload...")
                file_input = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//input[contains(@accept, "image/") or contains(@accept, "video/")]'))
                )

                # Step 3: Send the file path directly to the file input
                print(f"Uploading file: {media}")
                file_input.send_keys(media)  # Provide the absolute file path of the media file
                sleep(randint(1, 5))  # Optional delay to ensure the file is uploaded

                # Send the media
                actions.send_keys(Keys.ENTER).perform()

                print(f"Media sent to {contact}.")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Media sent to {contact} successfully.")

                sleep(randint(1, 2))

                # Take longer breaks after every 15 messages
                if (index + 1) % 15 == 0:
                    long_sleep = randint(20, 25)
                    print(f"Taking a longer break of {long_sleep} seconds...")
                    self.log_message.emit(f"[{index + 1}/{len(contacts)}] Taking a longer break of {long_sleep} seconds...")
                    sleep(long_sleep)

            except (TimeoutException, Exception) as e:
                print(f"An error occurred while sending media to {contact}: {str(e)}")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Failed sending media to {contact}")

    
        
    def count_valid_invalid(self,numbers):
         pattern = re.compile(r"^(?:\+91|91)?[6789]\d{9}$")
         valid_count = sum(1 for num in numbers if pattern.match(num))
         invalid_count = len(numbers) - valid_count
         return valid_count, invalid_count
    
    

    def is_invalid(self, number):
         pattern = re.compile(r"^(?:\+91|91)?[6789]\d{9}$")  # Matches valid Indian mobile numbers
         valid = int(bool(pattern.match(number)))  # 1 if valid, 0 otherwise  # 1 if invalid, 0 otherwise
         invalid=1-valid
         return invalid
   
    
    def send_message(self, contacts):
        """Send a message to specified contacts."""
        contact_list = [contact_info["contact"] for contact_info in contacts]
        valid, invalid = self.count_valid_invalid(contact_list)
        print(f"Valid Numbers: {valid}")
        print(f"Invalid Numbers: {invalid}")
       
        
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="chats-filled"]'))
            )
        except:
            print("No chat icon found")
            return
        k=0
        c=0
        t=0
        for index, contact_info in enumerate(contacts):

            t=(t+1)
            if (t%(100 +k )) == 0:
                k=(k+10)%40
                sleep(randint(300,600))

            contact = contact_info["contact"]
            message = contact_info["message"]
            if self.is_invalid(contact):
                continue            
            c = ( c + 1 ) % 10
            
            # Determine the heading based on the value of c
            if c == 1:
                heading = "Hey...did Jethalal inform you about this? Or you don't know about this yet???"
            elif c == 2:
                heading = "Imagine having access to something that completely revolutionizes how you [do a task]—sounds intriguing, right?"
            elif c == 6:
                heading = "What if I told you there exists this thing that you had never thought of? Yes, my dear..."
            elif c == 8:
                heading = "Sorry yrr, I know you've been waiting for this, and we could only tell you that we've done it for you..."
            elif c == 0:
                heading = "Roses are red, violets are blue... Only God knew that we would make this incredible product for you."
            elif c == 5:
                heading = "Hey… did Raj tell you about this? Or are you still in the dark?? 👀"    
            elif c == 3:
                heading = "Wait… you haven’t heard about this yet? 😳 Trust me, you NEED to know!"
            elif c == 7:
                heading = "Shocking! 😱 People are already taking advantage of this… and you?"
            elif c == 4:
                heading = "Guess what? 🧐 Everyone’s talking about this… but do YOU know yet?"
            elif c == 9:
                heading = "Psst… someone just told me something BIG! 🤯 Should I share it with you?"  
            try:
                actions = ActionChains(self.driver)
                actions.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()
                sleep(randint(3, 5))

                print(f"Attempting to send message to {contact}...")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Sending: {contact}")

                actions.key_down(Keys.ALT).send_keys('k').key_up(Keys.ALT).perform()
                sleep(randint(3, 6))              
                actions.send_keys(contact).perform()
                sleep(randint(1,3))
                actions.send_keys(Keys.ENTER).perform()
                sleep(randint(2, 5))
                

                

                # Send the heading and original message
                actions.send_keys(heading).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                sleep(randint(1, 3))

                for line in message.split('\n'):
                    actions.send_keys(line).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                   
                
                sleep(randint(1, 3))
                sleep(randint(1, 3))
                actions.send_keys(Keys.ENTER).perform()
                sleep(randint(2, 5))

             
                print(f"Message sent to {contact}.")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Message sent to {contact} successfully.")


                # Optional: Take a longer break after every 15 messages
                if (index + 1) % 15 == 0:
                    long_sleep = randint(20, 25)
                    print(f"Taking a longer break of {long_sleep} seconds...")
                    self.log_message.emit(f"[{index + 1}/{len(contacts)}] Taking a longer break of {long_sleep} seconds...")
                    sleep(long_sleep)

                        
               

                
            except Exception as e:
                print(f"An error occurred while sending a message to {contact}: {e}")
                self.log_message.emit(f"[{index + 1}/{len(contacts)}] Failed to send message to {contact}")
                

        



        

    def run_in_thread(self, contacts, message):
        """Run the send_message function in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self.send_message, args=(contacts, message))
        self.thread.start()

    def stop(self):
        """Stop the bot."""
        self.running = False
        if self.thread:
            self.thread.join()
        self.close()
