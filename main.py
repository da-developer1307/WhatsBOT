import os
import sys
# import time
from pandas import read_csv, read_excel
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QHeaderView, 
    QMenu, QTextEdit, QMenuBar, QMessageBox, QFileDialog, QComboBox, QTableWidgetItem, QStackedWidget, QCheckBox)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal, QSettings, pyqtSlot
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
import requests
import base64
import datetime
import pandas as pd
import gspread
from PyQt6.QtWidgets import QFileDialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")   
    return os.path.join(base_path, relative_path)
whatsapp_bot_path = resource_path("whatsapp_bot.py")
exec(open(whatsapp_bot_path, encoding="utf-8").read(), globals())
from whatsapp_bot import WhatsAppBot

class AuthWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("WhatsBot")
        self.setFixedSize(QSize(400, 500))

        self.firebase_web_api_key = "AIzaSyBOOZEzlSCj8y6xzMQ8t7LaMxiTu-1xjt0"
        
        # Initialize Firebase
        try:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": "whatsbotmarketing",
                "private_key_id": "4f09bc400780f2781ab3850d736928e811e22973",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDM+9Umnu5FycuI\nkWFAW7XKpWQblLVC+p1Cf4robrtAVBFHzPrRnH7odkr9mARGoeQL57FJ+wUxT+mx\n+zQKqS6NWie0h7HIsDc0AEWGJaZOKbJcf2TtWsziu2uYNdLH2QSHfcY0CafcZAYF\ndHhh4DdxgnanHDyeMUTpazqT2CC9Ntcm4comiYJPztn2m7KvMPJHbUjJCC+38POO\nfFgrWr4RRzb+Ld9uVc2cey9Scox6WcJftIf4BldaM0XGfz7QdJa+mzx8m6Jf1Cx1\nHSgPaRR+qHh+Kb2evWUKGcHU/s7zyw2N1p5CINa9+xCPfpt/+7088MRamQF5OXDj\nTC/TsJbLAgMBAAECggEADmKT6Z3DUewgl55q3pXbsvNwDDbKO6o+aVbDBvRnuVLM\n/abHE/kGt5s+6v9ajsxjURSQOVq02Wo8F7dDG9vAk783xHBgtm6WCSpbDALODMkv\nUP9zCUHTLrbWt6al+qFiXdHNRtnwnkOktTL1vxn5j20yP3WjVA9YFdtmZSQIiXlU\nq4CRKo1w9h0PypJ8ibLUmpAvWXIMOY/PX6QnQu16qJjun6AatszV/onPSrvaCvvI\nkLXR6ySO3GY9qGmlsHuFg/XDpPNtwOoCZ67tUQZC6ntfpfKrWR/bROXX7Lg1IwK5\nMaTZJUHCax8blnKnW3S6b7R69REYGS2K3keVEpcWgQKBgQD4eieu7rjC3w66eppZ\nlv3wDN8F+GOViz59Jw9eUEb5OomLC1/yvFIcFXzBZPpq6+KTiJksud/JhIpGbtQR\nFvlyejgiCJ8GSYITgtqbUnRRZ1ak2wZRcN6lahy/OEEteIu+pO2Fi/oBCAwEO+Op\neho/F1GoUZK1fQ12qxCK7e5ogQKBgQDTMJPigpUYfNsRnfZbneqmRXVuZCwX31fb\nc8f9PMUHo3iN/7ux4l0Udvb66I2/7x+a3yzMo11MM6/EOHi3EF4KKZ3W+nszv20y\nTI2xnfdoyxoVPsL7Ar+QpoD6C8nzDTX20oguhBkas46xxTBv7yW2fXrRZhkqmbKJ\n0dOSvfN5SwKBgQCbmGrnKUf7h5CCh6nF9j5YJsc1xuAdUg+0cVQ3XA/Fm7lrn5ja\nuMC2I2J2/FOvxrygZEZ+8npHh77K8jXL6dYUsKIb9cgXOMrCiwt3ff+mxg5Et37S\nWtqhPLx5pbFy1uyzWjX+jbPlF3Pm5tXeV769yU1yGHrFOWTH7cEzLmE/gQKBgHqj\n2R1Oy5pe1zDR1IC7ocpQx7MFhP2P+4s7H0YWBi07ZwS/H5ZbZ8Y8l4x5g+eTy3y6\nYV+s9r8LvORsDt3wKUwpgrmW1/jjD1yITDh7DXPTjiAMRFpT7D7qEjgipHH6l/3v\noJmyqIlzAEiHxGscK4BgOfRkH/U3MBEMwpqSqFMlAoGAehvrYvxtNN0h9DMStc/l\nPxgEGyA8MykWAeA7l+AWuGPdm0fSn7vdCijfbAwi6YagDSSpBuCCups9gG41NGqz\nFCduMg4b58kNq0PRiswhfuyjns426gUfoHf6OkTOZ+4+E+Cpdj+xwOJ7bN9P0siu\nIS0o9gahBIOUqKMJFQhku3Y=\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-aadja@whatsbotmarketing.iam.gserviceaccount.com",
                "client_id": "106341717945296508023",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-aadja%40whatsbotmarketing.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            })
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase initialization error: {str(e)}")
        
        # Create stacked widget for login/register pages
        self.stacked_widget = QStackedWidget()
        self.login_page = self.create_login_page()
        self.register_page = self.create_register_page()
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        
        # Apply styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1f1f1f;
                color: #ffffff;
            }
            QPushButton {
                background-color: #181818;
                color: #ffffff;
                border: 1px solid #313131;
                border-radius: 8px;
                padding: 8px 32px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #313131;
            }
            QLineEdit {
                background-color: #313131;
                border: 1px solid #313131;
                border-radius: 8px;
                padding: 8px;
                margin: 5px 0px;
                min-width: 250px;
            }
            QLabel {
                font-size: 14px;
                margin: 5px 0px;
            }
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                margin: 20px 0px;
            }
            #switchButton {
                background-color: transparent;
                border: none;
                color: #4a9eff;
                text-decoration: underline;
            }
            #errorLabel {
                color: #ff4a4a;
            }
        """)

    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("Welcome Back")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Email field
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Email")
        # self.login_email.setText("me.devarshukani@gmail.com")
        
        # Password field
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        # self.login_password.setText("123456")
        
        # Error label
        self.login_error = QLabel("")
        self.login_error.setObjectName("errorLabel")
        self.login_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        
        # Switch to register
        switch_btn = QPushButton("Don't have an account? Register")
        switch_btn.setObjectName("switchButton")
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        layout.addWidget(title)
        layout.addWidget(self.login_email)
        layout.addWidget(self.login_password)
        layout.addWidget(self.login_error)
        layout.addWidget(login_btn)
        layout.addWidget(switch_btn)
        page.setLayout(layout)
        return page

    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("Create Account")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Email field
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Email")
        
        # Password fields
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Password")
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.register_confirm_password = QLineEdit()
        self.register_confirm_password.setPlaceholderText("Confirm Password")
        self.register_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Error label
        self.register_error = QLabel("")
        self.register_error.setObjectName("errorLabel")
        self.register_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Register button
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)
        
        # Switch to login
        switch_btn = QPushButton("Already have an account? Login")
        switch_btn.setObjectName("switchButton")
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        layout.addWidget(title)
        layout.addWidget(self.register_email)
        layout.addWidget(self.register_password)
        layout.addWidget(self.register_confirm_password)
        layout.addWidget(self.register_error)
        layout.addWidget(register_btn)
        layout.addWidget(switch_btn)
        page.setLayout(layout)
        return page

    def handle_login(self):
        email = self.login_email.text()
        password = self.login_password.text()

        if not email or not password:
            self.login_error.setText("Please fill in all fields")
            return

        try:
            # Use Firebase REST API to authenticate the user
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.firebase_web_api_key}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            response = requests.post(url, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                # Successful login
                user_id = response_data['localId']
                id_token = response_data['idToken']
                
                # Save the user state using QSettings
                settings = QSettings("WhatsBot", "App")
                settings.setValue("user_id", user_id)
                settings.setValue("id_token", id_token)

                print("Login successful!")
                print(f"User ID: {user_id}")
                print(f"ID Token: {id_token}")

                # Hide the login window and show the main window
                self.hide()
                self.main_window = MainWindow()
                icon_pat=resource_path("whatsapp.png")
                self.main_window.setWindowIcon(QIcon(icon_pat))
                self.main_window.show()

            else:
                # Login failed
                error_message = response_data.get("error", {}).get("message", "Unknown error")
                self.login_error.setText(f"Login failed: {error_message}")
                print(f"Login error: {error_message}")

        except Exception as e:
            self.login_error.setText("An error occurred during login")
            print(f"Login exception: {str(e)}")

    def handle_register(self):
        email = self.register_email.text()
        password = self.register_password.text()
        confirm_password = self.register_confirm_password.text()

        if not email or not password or not confirm_password:
            self.register_error.setText("Please fill in all fields")
            return

        if password != confirm_password:
            self.register_error.setText("Passwords do not match")
            return

        try:
            # Create user in Firebase Auth
            user = auth.create_user(
                email=email,
                password=password
            )

            # Generate trial subscription details
            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(weeks=1)

            subscription_data = {
                "uid": user.uid,
                "start": start_time,
                "end": end_time
            }

            user_data = {
                "email": email,
                "uid": user.uid,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "custom_subscription_monthly": None,
                "custom_subscription_quaterly": None,
                "custom_subscription_biannual": None,
                "custom_subscription_annual": None,
                "custom_subscription_lifetime": None
            }

            # Add subscription data to Firestore
            db = firestore.client()
            db.collection("UserSubscription").add(subscription_data)
            db.collection("Users").document(user.uid).set(user_data)

            # Show success message and switch to login
            QMessageBox.information(self, "Success", "Registration successful! Please login.")
            self.stacked_widget.setCurrentIndex(0)

        except Exception as e:
            self.register_error.setText("Registration failed")
            print(f"Registration error: {str(e)}")



isUserLoggedIn = False
isUserLoggedInChecked = False

# class Worker(QThread):
#     """Worker thread to handle WhatsApp bot operations."""
#     message_sent = pyqtSignal(str)

#     def __init__(self, contacts, message):
#         super().__init__()
#         self.contacts = contacts
#         self.message = message
#         self.whatsapp_bot = WhatsAppBot()

#     def run(self):
#         """Run the WhatsApp messaging process."""
#         try:
#             self.sleep(1)  # Sleep to avoid sending too quickly
#             self.whatsapp_bot.open_whatsapp_web()
#             for contact in self.contacts:
#                 self.whatsapp_bot.send_message([contact], self.message)
#                 self.message_sent.emit(f"Message sent to {contact}")
#                 self.sleep(2)  # Sleep to avoid sending too quickly
#         except Exception as e:
#             self.message_sent.emit(f"Error: {str(e)}")
#         finally:
#             self.whatsapp_bot.close()

class WorkerCheckLogin(QThread):
    finished = pyqtSignal(str)

    def run(self):
        bot = WhatsAppBot()

        def handle_login_status(is_logged_in):
            global isUserLoggedIn, isUserLoggedInChecked
            isUserLoggedInChecked = True
            if is_logged_in:
                isUserLoggedIn = True
                self.finished.emit("Logged In")
            else:
                isUserLoggedIn = False
                self.finished.emit("Logged Off")

        # Connect the signal to the slot function
        bot.login_checked.connect(handle_login_status)

        bot.run_login_check(isHeadless=True)  # Call the login check method

class WorkerLogin(QThread):
    finished = pyqtSignal(str)
    update_button_text = pyqtSignal(str)  

    def __init__(self):
        super().__init__()
        self.bot = None

    def run(self):
        try:
            self.bot = WhatsAppBot()

            # Connect the signal to the slot
            print("Connecting login_checked signal to handle_login_status")
            self.bot.login_checked.connect(self.handle_login_status)

            # Perform login
            print("Starting login process")
            self.bot.perform_login(isHeadless=False)

            # Keep the thread running until the login process is complete
            # while not self.bot.is_driver_closed():
            #     QThread.msleep(100)  # Sleep for 100ms to prevent high CPU usage

        except Exception as e:
            print(f"Error in WorkerLogin: {str(e)}")
            self.finished.emit(f"Error during login: {str(e)}")

    def stop(self):
        if self.bot:
            self.bot.close()

    def handle_login_status(self, status):
        print(f"Handling login status: {status}")
        global isUserLoggedIn, isUserLoggedInChecked
        isUserLoggedIn = status
        isUserLoggedInChecked = True

        self.update_button_text.emit("Verifiying...")






class WorkerLogout(QThread):
    finished = pyqtSignal(str)

    def run(self):
        try:
            bot = WhatsAppBot()
            response = bot.perform_logout()
            if response:
                global isUserLoggedIn, isUserLoggedInChecked
                isUserLoggedIn = False
                isUserLoggedInChecked = True
                self.finished.emit("Logged out successfully")
            else:
                self.finished.emit("Logout failed")
        except Exception as e:
            self.finished.emit(f"Error during logout: {str(e)}")



class WorkerMessageCampaign(QThread):
    finishedMessageCampaign = pyqtSignal(str)

    def __init__(self, contacts):
        super().__init__()
        self.contacts = contacts
        # self.message = message
        self.whatsapp_bot = WhatsAppBot()

    def run(self):
        """Run the WhatsApp messaging process."""
        try:
             success_count, failure_count = self.whatsapp_bot.run_message_campaign(True, self.contacts)
             result_message = f"Campaign finished successfully.\nMessages Sent: {success_count}\nFailed: {failure_count}"
             self.finishedMessageCampaign.emit(result_message)
        except Exception as e:
             self.whatsapp_bot.log_message.emit(f"Error during Campaign")
             print(f"Error during Campaign: {str(e)}")
             success_count, failure_count = 0, 0
        finally:
             self.whatsapp_bot.close()

             result_message = f"Campaign finished successfully.\nMessages Sent: {success_count}\nFailed: {failure_count}"
             self.finishedMessageCampaign.emit(result_message)


class WorkerMediaCampaign(QThread):
    finishedMediaCampaign = pyqtSignal(str)

    def __init__(self, contacts):
        super().__init__()
        self.contacts = contacts
        # self.media = media
        self.whatsapp_bot = WhatsAppBot()

    def run(self):
        """Run the WhatsApp media campaign process."""
        try:
             success_count, failure_count =self.whatsapp_bot.run_media_campaign(True, self.contacts)
             result_message = f"Campaign finished successfully.\nMessages Sent: {success_count}\nFailed: {failure_count}"
             self.finishedMediaCampaign.emit(result_message)            
        except Exception as e:
             self.whatsapp_bot.log_message.emit(f"Error during Campaign")
             print(f"Error during Campaign: {str(e)}")
             success_count, failure_count = 0, 0
        finally:
             self.whatsapp_bot.close()

             result_message = f"Campaign finished successfully.\nMessages Sent: {success_count}\nFailed: {failure_count}"
             self.finishedMediaCampaign.emit(result_message)            
            

class WorkerMediaAndMessageCampaign(QThread):
    finishedMediaAndMessageCampaign = pyqtSignal(str)

    def __init__(self, contacts):
        super().__init__()
        self.contacts = contacts
        # self.media = media
        # self.message = message
        self.whatsapp_bot = WhatsAppBot()

    def run(self):
        """Run the WhatsApp media campaign process."""
        try:
             
             success_count, failure_count =self.whatsapp_bot.run_media_and_message_campaign(True, self.contacts)
             result_message = f"Campaign finished successfully.\nMessages Sent: {success_count}\nFailed: {failure_count}"
             self.finishedMediaAndMessageCampaign.emit("Campaign finished successfully")
        except Exception as e:
             self.whatsapp_bot.log_message.emit(f"Error during Campaign")
             print(f"Error during Campaign: {str(e)}")
             success_count, failure_count = 0, 0
        finally:
             self.whatsapp_bot.close()

             result_message = f"Campaign finished successfully.\nMessages Sent: {success_count}\nFailed: {failure_count}"
             self.finishedMediaAndMessageCampaign.emit(result_message)  

class CustomHeader(QHeaderView):
    def __init__(self, orientation, main_window, parent=None):
        super().__init__(orientation, parent)
        self.main_window = main_window  # Store reference to MainWindow
        self.setSectionsClickable(True)
        self.styleSheet = """
            QHeaderView::section {
                background-color: #1f1f1f;
                color: #ffffff;
                padding: 4px;
                border: none;
            }
            QHeaderView::section:hover {
                background-color: #313131;
            }
            QAction {
                background-color: #313131;
                color: #ffffff;
                padding: 8px;
            }
            QAction:hover {
                background-color: #1f1f1f;
            }
        """
        self.setStyleSheet(self.styleSheet)
    
    def contextMenuEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index >= 0:
            context_menu = QMenu(self)

            set_as_name_action = QAction(f"Set as Name", self)
            set_as_name_action.triggered.connect(lambda: self.set_as_variable(index, "Name"))

            set_as_contact_action = QAction(f"Set as Contact", self)
            set_as_contact_action.triggered.connect(lambda: self.set_as_variable(index, "Contact"))

            set_as_var1_action = QAction(f"Set as Variable 1", self)
            set_as_var1_action.triggered.connect(lambda: self.set_as_variable(index, "Variable 1"))

            set_as_var2_action = QAction(f"Set as Variable 2", self)
            set_as_var2_action.triggered.connect(lambda: self.set_as_variable(index, "Variable 2"))

            set_as_var3_action = QAction(f"Set as Variable 3", self)
            set_as_var3_action.triggered.connect(lambda: self.set_as_variable(index, "Variable 3"))

            context_menu.addAction(set_as_contact_action)
            context_menu.addAction(set_as_name_action)
            context_menu.addAction(set_as_var1_action)
            context_menu.addAction(set_as_var2_action)
            context_menu.addAction(set_as_var3_action)

            context_menu.exec(event.globalPos())

    def set_as_variable(self, index, variable_name):
        """Updates the text fields in MainWindow based on the variable selected."""

        column_name = self.main_window.csv_table.horizontalHeaderItem(index).text()

        # Use setCurrentText for QComboBox objects
        if variable_name == "Name":
            self.main_window.name_variable.setCurrentText(f"{column_name}")
        elif variable_name == "Contact":
            self.main_window.contact_variable.setCurrentText(f"{column_name}")
        elif variable_name == "Variable 1":
            self.main_window.var1_variable.setCurrentText(f"{column_name}")
        elif variable_name == "Variable 2":
            self.main_window.var2_variable.setCurrentText(f"{column_name}")
        elif variable_name == "Variable 3":
            self.main_window.var3_variable.setCurrentText(f"{column_name}")

        print(f"Column {index + 1} set as {variable_name}")


class PaymentWindow(QWidget):
    payment_successful = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Subscribe to WhatsBot")
        self.setFixedSize(QSize(400, 500))
        
        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("Choose Your Subscription Plan")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Plan dropdown
        self.plan_dropdown = QComboBox()

        # Error label
        self.payment_error = QLabel("")
        self.payment_error.setObjectName("errorLabel")
        self.payment_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subscribe button
        subscribe_btn = QPushButton("Subscribe")
        subscribe_btn.clicked.connect(self.handle_payment)
        
        # Back button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("switchButton")
        back_btn.clicked.connect(self.close)
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.plan_dropdown)
        layout.addWidget(self.payment_error)
        layout.addWidget(subscribe_btn)
        layout.addWidget(back_btn)
        self.setLayout(layout)
        
        # Apply styling
        self.setStyleSheet(""" /* Add your styles here */ """)

        # Razorpay Keys
        self.testKeyID = "rzp_live_Nz0hiAdGnWt3qX"
        self.testKeySecret = "MEGnwjWxicOdfdrsfhkqOiZA"
        self.base_url = "https://api.razorpay.com/v1"

        # Initialize Firebase Admin SDK
        if not firebase_admin._apps:
            cred = credentials.Certificate("path/to/your/firebase/credentials.json")
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()  # Firestore client

        # Fetch user data and initialize the dropdown
        self.initialize_subscription_plans()


    def initialize_subscription_plans(self):
        """Fetch user data and populate the subscription dropdown."""
        user_id = QSettings("WhatsBot", "App").value("user_id")
        user_ref = self.db.collection("Users").document(user_id)
        user_data = user_ref.get().to_dict()

        if not user_data:
            QMessageBox.warning(self, "Error", "User data not found.")
            return

        # Default prices
        default_prices = {
            "monthly": 362,
            "annual": 3814,
            "lifetime": 17376
        }

        # Fetch custom prices or fallback to default prices
        monthly_price = user_data.get("custom_subscription_monthly", default_prices["monthly"])
        annual_price = user_data.get("custom_subscription_annual", default_prices["annual"])
        lifetime_price = user_data.get("custom_subscription_lifetime", default_prices["lifetime"])

        # Create dropdown options
        self.plan_dropdown.addItems([
            f"Monthly - ₹{monthly_price if monthly_price else default_prices['monthly']}",
            f"Yearly (Recommended) - ₹{annual_price if annual_price else default_prices['annual']}",
            f"Lifetime (Best Deal) - ₹{lifetime_price if lifetime_price else default_prices['lifetime']}"
        ])


    def handle_payment(self):
        print("Handling payment...")
        selected_plan = self.plan_dropdown.currentText()
        if "Monthly" in selected_plan:
            amount = int(selected_plan.split("₹")[1]) * 100  # Convert to paise
        elif "Yearly" in selected_plan:
            amount = int(selected_plan.split("₹")[1]) * 100  # Convert to paise
        else:  # Lifetime plan
            amount = int(selected_plan.split("₹")[1]) * 100  # Convert to paise

        try:
            # Step 1: Create Razorpay Order
            order_id = self.create_order(amount)
            if not order_id:
                print("Failed to create order")
                QMessageBox.warning(self, "Error", "Failed to create Razorpay order.")
                return

            print(f"Order ID: {order_id}")

            # Step 2: Launch Razorpay Checkout
            print("Launching Razorpay Checkout...")
            self.open_checkout(order_id, amount)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def open_checkout(self, order_id, amount):
        """Launch Razorpay Checkout securely."""
        # Use an environment variable or secure backend to fetch Razorpay key
        razorpay_key = self.testKeyID

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        </head>
        <body>
            <script>
                new QWebChannel(qt.webChannelTransport, function(channel) {{
                    window.qt_channel = channel.objects.qt_channel;

                    var options = {{
                        "key": "{razorpay_key}",
                        "amount": "{amount}",
                        "currency": "INR",
                        "name": "WhatsBot",
                        "description": "WhatsBot Subscription Payment",
                        "image": "https://your-logo-url.com/logo.png",
                        "order_id": "{order_id}",
                        "handler": function (response) {{
                            // Send success response to Python
                            qt_channel.sendMessage(JSON.stringify({{
                                "status": "success",
                                "payment_id": response.razorpay_payment_id,
                                "order_id": response.razorpay_order_id,
                                "amount": {amount}
                            }}));
                        }},
                        "theme": {{
                            "color": "#1f1f1f"
                        }},
                        "modal": {{
                            "ondismiss": function() {{
                                // Send failure response to Python
                                qt_channel.sendMessage(JSON.stringify({{
                                    "status": "failure",
                                    "reason": "Payment canceled by user",
                                }}));
                            }}
                        }}
                    }};
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }});
            </script>
        </body>
        </html>
        """

        # Load the HTML directly into QWebEngineView
        self.webview = QWebEngineView()
        self.webview.setWindowTitle("WhatsBot Payment")
        self.webview.setWindowIcon(QIcon(resource_path("whatsapp.png")))
        self.webview.setFixedSize(QSize(1200, 800))
        self.webview.setHtml(html_template)

        # Setup QWebChannel for communication
        self.channel = QWebChannel()
        self.channel.registerObject("qt_channel", self)
        self.webview.page().setWebChannel(self.channel)

        self.webview.show()



    @pyqtSlot(str)
    def sendMessage(self, message):
        """Handle messages from the Razorpay checkout page."""
        response = json.loads(message)

        if response["status"] == "success":
            payment_id = response["payment_id"]
            order_id = response["order_id"]
            amount = response["amount"]
            print(f"Payment successful! Payment ID: {payment_id}, Order ID: {order_id}")
            
            # Calculate end date based on selected plan
            selected_plan = self.plan_dropdown.currentText()
            if "Monthly" in selected_plan:
                end_date = datetime.datetime.now() + datetime.timedelta(days=30)
            elif "Yearly" in selected_plan:
                end_date = datetime.datetime.now() + datetime.timedelta(days=365)
            else:  # Lifetime plan
                end_date = datetime.datetime.now() + datetime.timedelta(days=365*100)

            # Create Firestore entry for successful payment
            payment_data = {
                "payment_id": payment_id,
                "order_id": order_id,
                "amount": amount,
                "start": firestore.SERVER_TIMESTAMP,
                "end": end_date,
                "uid": QSettings("WhatsBot", "App").value("user_id"),
                "createdAt": firestore.SERVER_TIMESTAMP  # Add a timestamp
            }

            # Reference to Firestore collection
            payment_ref = self.db.collection("UserSubscription").add(payment_data)
            print(f"Payment entry created")

            self.close()
            self.payment_successful.emit()

        elif response["status"] == "failure":
            reason = response.get("reason", "Unknown error")
            print(f"Payment failed. Reason: {reason}")

        # Close the webview after handling the response
        self.webview.close()
    
    def display_campaign_result(self, message):
         """Display the final campaign message with success and failure counts."""
         print(message)  # Print to console
         self.log_label.setText(message)  # If using QLabel
         self.log_text_edit.append(message)  # If using QTextEdit

    
    def create_order(self, amount):
        """Create an order using Razorpay API."""
        print("Creating order...")
        url = f"{self.base_url}/orders"
        auth = f"{self.testKeyID}:{self.testKeySecret}"
        headers = {
            "Authorization": "Basic " + base64.b64encode(auth.encode()).decode(),
            "Content-Type": "application/json",
        }
        data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_rcptid_11",
            "payment_capture": 1  # Auto capture
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            response_data = response.json()
            print(f"Order created: {response_data.get('id')}")
            return response_data.get("id")
        else:
            print(f"Error creating order: {response.status_code}, {response.text}")
            return None



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set fixed-size window
        self.setWindowTitle("WhatsBot")
        self.setFixedSize(QSize(1100, 800))  # Width x Height

        try:
            # Make sure Firebase is initialized if not already done
            if not firebase_admin._apps:
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": "whatsbotmarketing",
                    "private_key_id": "4f09bc400780f2781ab3850d736928e811e22973",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDM+9Umnu5FycuI\nkWFAW7XKpWQblLVC+p1Cf4robrtAVBFHzPrRnH7odkr9mARGoeQL57FJ+wUxT+mx\n+zQKqS6NWie0h7HIsDc0AEWGJaZOKbJcf2TtWsziu2uYNdLH2QSHfcY0CafcZAYF\ndHhh4DdxgnanHDyeMUTpazqT2CC9Ntcm4comiYJPztn2m7KvMPJHbUjJCC+38POO\nfFgrWr4RRzb+Ld9uVc2cey9Scox6WcJftIf4BldaM0XGfz7QdJa+mzx8m6Jf1Cx1\nHSgPaRR+qHh+Kb2evWUKGcHU/s7zyw2N1p5CINa9+xCPfpt/+7088MRamQF5OXDj\nTC/TsJbLAgMBAAECggEADmKT6Z3DUewgl55q3pXbsvNwDDbKO6o+aVbDBvRnuVLM\n/abHE/kGt5s+6v9ajsxjURSQOVq02Wo8F7dDG9vAk783xHBgtm6WCSpbDALODMkv\nUP9zCUHTLrbWt6al+qFiXdHNRtnwnkOktTL1vxn5j20yP3WjVA9YFdtmZSQIiXlU\nq4CRKo1w9h0PypJ8ibLUmpAvWXIMOY/PX6QnQu16qJjun6AatszV/onPSrvaCvvI\nkLXR6ySO3GY9qGmlsHuFg/XDpPNtwOoCZ67tUQZC6ntfpfKrWR/bROXX7Lg1IwK5\nMaTZJUHCax8blnKnW3S6b7R69REYGS2K3keVEpcWgQKBgQD4eieu7rjC3w66eppZ\nlv3wDN8F+GOViz59Jw9eUEb5OomLC1/yvFIcFXzBZPpq6+KTiJksud/JhIpGbtQR\nFvlyejgiCJ8GSYITgtqbUnRRZ1ak2wZRcN6lahy/OEEteIu+pO2Fi/oBCAwEO+Op\neho/F1GoUZK1fQ12qxCK7e5ogQKBgQDTMJPigpUYfNsRnfZbneqmRXVuZCwX31fb\nc8f9PMUHo3iN/7ux4l0Udvb66I2/7x+a3yzMo11MM6/EOHi3EF4KKZ3W+nszv20y\nTI2xnfdoyxoVPsL7Ar+QpoD6C8nzDTX20oguhBkas46xxTBv7yW2fXrRZhkqmbKJ\n0dOSvfN5SwKBgQCbmGrnKUf7h5CCh6nF9j5YJsc1xuAdUg+0cVQ3XA/Fm7lrn5ja\nuMC2I2J2/FOvxrygZEZ+8npHh77K8jXL6dYUsKIb9cgXOMrCiwt3ff+mxg5Et37S\nWtqhPLx5pbFy1uyzWjX+jbPlF3Pm5tXeV769yU1yGHrFOWTH7cEzLmE/gQKBgHqj\n2R1Oy5pe1zDR1IC7ocpQx7MFhP2P+4s7H0YWBi07ZwS/H5ZbZ8Y8l4x5g+eTy3y6\nYV+s9r8LvORsDt3wKUwpgrmW1/jjD1yITDh7DXPTjiAMRFpT7D7qEjgipHH6l/3v\noJmyqIlzAEiHxGscK4BgOfRkH/U3MBEMwpqSqFMlAoGAehvrYvxtNN0h9DMStc/l\nPxgEGyA8MykWAeA7l+AWuGPdm0fSn7vdCijfbAwi6YagDSSpBuCCups9gG41NGqz\nFCduMg4b58kNq0PRiswhfuyjns426gUfoHf6OkTOZ+4+E+Cpdj+xwOJ7bN9P0siu\nIS0o9gahBIOUqKMJFQhku3Y=\n-----END PRIVATE KEY-----\n",
                    "client_email": "firebase-adminsdk-aadja@whatsbotmarketing.iam.gserviceaccount.com",
                    "client_id": "106341717945296508023",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-aadja%40whatsbotmarketing.iam.gserviceaccount.com",
                    "universe_domain": "googleapis.com"
                })
                firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase initialization error: {str(e)}")

        # Layout and widgets setup
        # layout = QVBoxLayout()
        # self.user_info_label = QLabel("Fetching user information...")
        # self.user_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # layout.addWidget(self.user_info_label)
        
        # central_widget = QWidget()
        # central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)

        self.worker = WorkerCheckLogin()
        self.worker.finished.connect(self.update_status)
        self.worker.start()

        self.setStyleSheet("""
            QWidget {
                background-color: #1f1f1f;
                color: #ffffff;
            }
            QPushButton {
                background-color: #181818;
                color: #ffffff;
                border: 1px solid #313131;
                border-radius: 8px;
                padding: 8px 32px;
            }
            QPushButton:hover {
                background-color: #313131;
            }
            QLineEdit {
                background-color: #313131;
                border: 1px solid #313131;
                border-radius: 8px;
                padding: 6px;
            }
            QTableWidget {
                background-color: #313131;
                border: 1px solid #313131;
                border-radius: 8px;
            }
            QComboBox {
                background-color: #313131;
                border: 1px solid #313131;
                border-radius: 8px;
                padding: 6px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #313131;
                border-left-style: solid;
            }
            QComboBox::down-arrow {
                image: url(resource_path"dropdown-arrow.png");
                padding-right: 8px;
                width: 8px;
                height: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #1f1f1f;  
                color: #ffffff;
                border: none;  
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                background-color: #1f1f1f;  
                color: #ffffff;
                border: none;  
                padding: 8px;  
                outline: none; 
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #313131; 
                border: none; 
                outline: none;
            }
            QTextEdit {
                background-color: #313131;
                border: 1px solid #313131;
                border-radius: 8px;
                padding: 6px;
            }
        """)

        self.whatsapp_bot = WhatsAppBot()
        self.text_contact = QLineEdit(self)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()  # Vertical layout to hold buttons and table
        central_widget.setLayout(main_layout)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Sidebar Buttons (Now in a horizontal layout)
        self.option1_btn = QPushButton("Initializing") 
        self.option1_btn.setIcon(QIcon(resource_path("whatsapp.png")))
        self.option1_btn.setIconSize(QSize(30, 30))
        self.option1_btn.setFixedHeight(50)
        self.option1_btn.setFixedWidth(150)
        self.option1_btn.clicked.connect(self.clickLoginLogout)

        self.subscribe_btn = QPushButton("Subscribe") 
        # self.subscribe_btn.setIconSize(QSize(30, 30))
        self.subscribe_btn.setFixedHeight(50)
        self.subscribe_btn.setFixedWidth(150)
        self.subscribe_btn.clicked.connect(self.initiate_payment)
        
        option2_btn = QPushButton("Reset Campaign")
        option2_btn.setFixedHeight(50)
        option2_btn.setFixedWidth(150)
        option2_btn.clicked.connect(self.reset_everything)

        # option3_btn = QPushButton("Settings")
        # option3_btn.setFixedHeight(50)
        # option3_btn.setFixedWidth(150)
        button_layout.addWidget(self.option1_btn)
        button_layout.addSpacing(8)
        button_layout.addWidget(self.subscribe_btn)
        button_layout.addStretch() 
        button_layout.addWidget(option2_btn)
        # button_layout.addWidget(option3_btn)

        # Add the horizontal button layout to the main layout
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(16)

        # Create a horizontal layout for sections
        section = QHBoxLayout()
        
        # Section 1 (Campaign Details)
        section1 = QVBoxLayout()
        section1.setAlignment(Qt.AlignmentFlag.AlignTop)

        section1_title = QLabel("Campaign Details")
        section1_title.setStyleSheet("font-size: 14px; font-weight: bold;")

        dropdown_layout = QHBoxLayout()
        dropdown_label = QLabel("Campaign Type")
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Only Message", "Only Media", "Message & Media"])
        
        # Connect the dropdown to the update method
        self.dropdown.currentIndexChanged.connect(self.update_fields_based_on_selection)

        dropdown_layout.addWidget(dropdown_label)
        dropdown_layout.addSpacing(8)
        dropdown_layout.addWidget(self.dropdown)

        import_media = QHBoxLayout()
        
        self.import_text_field_media = QLineEdit()
        self.import_text_field_media.setPlaceholderText("Select a Media file")
        self.import_text_field_media.setReadOnly(True)

        self.browse_btn_media = QPushButton("Browse")
        self.browse_btn_media.setEnabled(False)

        import_media.addWidget(self.import_text_field_media)
        import_media.addSpacing(8)
        import_media.addWidget(self.browse_btn_media)


        section1.addWidget(section1_title)
        # section1.addSpacing(8)
        section1.addLayout(dropdown_layout)
        section1.addSpacing(16)
        section1.addWidget(QLabel("Import Media"))
        section1.addLayout(import_media)

        text_message_label = QLabel("Message")

        # Multi-line text field
        self.text_message_field = QTextEdit()
        self.text_message_field.setPlaceholderText("Enter your campaign message here")


        # Dropdown to insert variables into the message field
        variable_dropdown_layout = QHBoxLayout()
        variable_dropdown_label = QLabel("Insert Variable:")
        self.variable_dropdown = QComboBox()
        self.variable_dropdown.addItems(["-- Select --", "{{name}}", "{{contact}}", "{{variable 1}}", "{{variable 2}}", "{{variable 3}}"])

        insert_variable_button = QPushButton("Insert")
        insert_variable_button.clicked.connect(self.insert_variable_in_message)

        variable_dropdown_layout.addWidget(variable_dropdown_label)
        variable_dropdown_layout.addWidget(self.variable_dropdown)
        variable_dropdown_layout.addWidget(insert_variable_button)

        section1.addSpacing(8)
        section1.addLayout(variable_dropdown_layout)
        
        section1.addSpacing(4)
        section1.addWidget(text_message_label)
        section1.addWidget(self.text_message_field)

        # Section 2 (Imported Data)
        section2 = QVBoxLayout()
        section2.setAlignment(Qt.AlignmentFlag.AlignTop)

        import_file = QHBoxLayout()
            

        self.import_text_field = QLineEdit()
        self.import_text_field.setPlaceholderText("Select a CSV file")
        self.import_text_field.setReadOnly(True)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.open_data_file_dialog)

        import_file.addWidget(self.import_text_field)
        import_file.addSpacing(8)
        import_file.addWidget(browse_btn)
        
        section2_title = QLabel("Leads Details")
        section2_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        section2.addWidget(section2_title)

        section2.addLayout(import_file)
        section2.addSpacing(16)
        section2.addWidget(QLabel("Imported Data"))

        # Create CSV Data Table and pass a reference to MainWindow
        self.csv_table = QTableWidget()
        header = CustomHeader(Qt.Orientation.Horizontal, self)  # Pass MainWindow reference
        self.csv_table.setHorizontalHeader(header)


        section2.addWidget(self.csv_table)

        # Add sections to the main section layout
        section.addLayout(section1, 1)  # 1 part
        section.addSpacing(16)
        section.addLayout(section2, 2)  # 2 parts

        main_layout.addLayout(section)

        variables_label = QHBoxLayout()

        name_label = QLabel("Name (Optional)")
        contact_label = QLabel("Contact (Required)")
        var1_label = QLabel("Variable 1 (Optional)")
        var2_label = QLabel("Variable 2 (Optional)")
        var3_label = QLabel("Variable 3 (Optional)")
        
        
        variables_label.addWidget(contact_label)
        variables_label.addSpacing(8)
        variables_label.addWidget(name_label)
        variables_label.addSpacing(8)
        variables_label.addWidget(var1_label)
        variables_label.addSpacing(8)
        variables_label.addWidget(var2_label)
        variables_label.addSpacing(8)
        variables_label.addWidget(var3_label)

        
        variables = QHBoxLayout()

        self.name_variable = QComboBox()
        self.name_variable.addItem("-- Select --")
        self.name_variable.setEnabled(False)  # Initially disabled until CSV is loaded

        self.contact_variable = QComboBox()
        self.contact_variable.addItem("-- Select --")
        self.contact_variable.setEnabled(False)

        self.var1_variable = QComboBox()
        self.var1_variable.addItem("-- Select --")
        self.var1_variable.setEnabled(False)

        self.var2_variable = QComboBox()
        self.var2_variable.addItem("-- Select --")
        self.var2_variable.setEnabled(False)

        self.var3_variable = QComboBox()
        self.var3_variable.addItem("-- Select --")
        self.var3_variable.setEnabled(False)

        
        variables.addWidget(self.contact_variable)
        variables.addSpacing(8)
        variables.addWidget(self.name_variable)
        variables.addSpacing(8)
        variables.addWidget(self.var1_variable)
        variables.addSpacing(8)
        variables.addWidget(self.var2_variable)
        variables.addSpacing(8)
        variables.addWidget(self.var3_variable)


        main_layout.addSpacing(8)

        variables_title = QLabel("Variables")
        variables_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(variables_title)
        main_layout.addWidget(QLabel("Select the columns to use as variables for the campaign message. Right-click on the column header to set a variable."))

        main_layout.addSpacing(8)
        main_layout.addLayout(variables_label)
        main_layout.addLayout(variables)

        main_layout.addSpacing(8)
        
        # Create horizontal layout for country code elements
        country_code_layout = QHBoxLayout()
        
        self.country_code_checkbox = QCheckBox("Country Code")
        self.country_code_checkbox.stateChanged.connect(self.on_country_code_changed)
        self.country_code_checkbox.setFixedHeight(40)
        
        self.note_text = QLineEdit()
        self.note_text.setPlaceholderText("Enter a Country Code") 
        self.note_text.setVisible(False)
        self.note_text.textChanged.connect(lambda text: self.note_text.setText(''.join(filter(str.isdigit, text))))
        self.note_text.setFixedWidth(150)
        
        # Add widgets to horizontal layout
        country_code_layout.addWidget(self.country_code_checkbox)
        country_code_layout.addWidget(self.note_text)
        country_code_layout.addStretch()
        
        # Add horizontal layout to main layout
        main_layout.addLayout(country_code_layout)

        bottom = QHBoxLayout()
        start_campaign_btn = QPushButton("Start Campaign")
        start_campaign_btn.setFixedHeight(50)
        start_campaign_btn.setFixedWidth(200)
        start_campaign_btn.setIcon(QIcon(resource_path("send.png")))
        start_campaign_btn.setIconSize(QSize(30, 30))
        start_campaign_btn.clicked.connect(self.start_campaign)

        bottom.addStretch()  # This spacer pushes the button to the right
        bottom.addWidget(start_campaign_btn)
        main_layout.addSpacing(32)
        main_layout.addLayout(bottom)

        self.log_display = QLabel(self)
        main_layout.addWidget(self.log_display)

        # Create Menu Bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # File Menu
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        # File -> Open option
        open_action = file_menu.addAction("Import Data")
        open_action.triggered.connect(self.open_data_file_dialog)

        # File -> Exit option
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        # Help Menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

        # Help -> View Help option
        # view_help_action = help_menu.addAction("View Help")

        # Help -> Check for Updates option
        check_updates_action = help_menu.addAction("Check for Updates")
        check_updates_action.triggered.connect(self.check_for_updates)

        # Help -> About option
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)
        
        #self.log
        self.log_label = QLabel(self)
        self.log_label.setText("Log Messages")
        self.layout().addWidget(self.log_label)
        
        #log text edit
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.layout().addWidget(self.log_text_edit)  # Ensure it's added to the UI

        settings = QSettings("WhatsBot", "App")
        user_id = settings.value("user_id", "")
        id_token = settings.value("id_token", "")

        if user_id and id_token:
            self.fetch_user_subscription(user_id)
        else:
            QMessageBox.warning(self, "Authentication", "No user is logged in. Please log in first.")

    def check_for_updates(self):
        QMessageBox.information(self, "WhatsBot Update", "There are no updates available at the moment.")

    def insert_variable_in_message(self):
        variable = self.variable_dropdown.currentText()
        if variable != "-- Select --":
            current_text = self.text_message_field.toPlainText()
            cursor = self.text_message_field.textCursor()
            cursor.insertText(variable)
            self.text_message_field.setTextCursor(cursor)

    
    def on_country_code_changed(self):
        if self.country_code_checkbox.isChecked():
            self.note_text.setVisible(True)
        else:
            self.note_text.setVisible(False)


    def fetch_user_subscription(self, user_id):
        try:
            # Fetch data from Firestore using user_id
            import datetime
            current_time = datetime.datetime.now()
            
            db = firestore.client()
            user_ref = db.collection("UserSubscription").where("uid", "==", user_id)
            docs = user_ref.get()

            for doc in docs:
                user_data = doc.to_dict()
                end_time = user_data.get('end').timestamp()
                
                if end_time > current_time.timestamp():
                    print(f"User data: {user_data}")
                    print(f"User ID: {user_id} found in Firestore with valid subscription.")
                    self.subscribe_btn.setVisible(False)

                    settings = QSettings("WhatsBot", "App")
                    settings.setValue("is_subscribed", True)

                    return True

            print(f"User ID: {user_id} not found or subscription expired.")
            self.subscribe_btn.setVisible(True)
            settings = QSettings("WhatsBot", "App")
            settings.setValue("is_subscribed", False)
            return False
                
        except Exception as e:
            print(f"Error fetching user data: {str(e)}")
            return False
        

    def show_about_dialog(self):
        about_dialog = QMessageBox()
        about_dialog.setWindowTitle("About WhatsBot")
        icon_path = resource_path("whatsapp.png")
        about_dialog.setWindowIcon(QIcon(icon_path))
        about_dialog.setText("WhatsBot - WhatsApp Marketing Automation Tool\n\nVisit Website for more information: \nhttps://indi.technology/ \n\nVersion 1.3.2\n\n© INDIRIDES TECHNOLOGY SERVICES PRIVATE LIMITED")
        about_dialog.exec()

    @pyqtSlot()
    def initiate_payment(self):
        # Payment window
        self.payment_window = PaymentWindow()
        self.payment_window.payment_successful.connect(self.hide_subscribe_button)
        self.payment_window.setWindowIcon(QIcon(resource_path("whatsapp.png")))
        self.payment_window.show()

    def hide_subscribe_button(self):
        # Hide the subscribe button when payment is successful
        self.subscribe_btn.setVisible(False)

    def update_status(self, message):
        print("update_status: " + message)
        if isUserLoggedInChecked == True:
            if isUserLoggedIn == False:
                self.option1_btn.setText("Login")
                self.option1_btn.setStyleSheet("background-color: #0c180f; color: #ffffff;")
            else:
                self.option1_btn.setText("Logout")
                self.option1_btn.setStyleSheet("background-color: #271313; color: #ffffff;")

    def update_button_text(self, text):
        # Update the button text
        self.option1_btn.setText(text)
        self.worker.finished.disconnect(self.update_status)

        self.worker = WorkerCheckLogin()
        self.worker.finished.connect(self.update_status)
        self.worker.start()


    def clickLoginLogout(self):
        if isUserLoggedInChecked:
            if isUserLoggedIn:
                print("Logging out")
                self.worker_logout = WorkerLogout()
                self.worker_logout.finished.connect(self.update_status)
                self.worker_logout.start()


                # Implement logout functionality here
            else:
                print("Logging in")
                
                # Create and show login steps dialog
                steps_dialog = QMessageBox()
                steps_dialog.setWindowTitle("WhatsApp Login Steps")
                steps_dialog.setIcon(QMessageBox.Icon.Information)
                
                steps_text = """
                Follow these steps to login:
                
                1. A WhatsApp Web window will open
                2. Open WhatsApp on your phone
                3. Tap Menu or Settings and select WhatsApp Web/Desktop
                4. Point your phone camera to scan the QR code
                5. Keep your phone connected to the internet
                5. Wait till the chats are loaded in the WhatsApp Web window
                6. Close the Browser only after the chats are loaded
                7. Restart the Application
                
                Click OK when you're ready to proceed.
                """
                
                steps_dialog.setText(steps_text)
                steps_dialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                
                if steps_dialog.exec() == QMessageBox.StandardButton.Ok:
                    self.worker_login = WorkerLogin()
                    self.worker_login.finished.connect(self.update_status)
                    self.worker_login.update_button_text.connect(self.update_button_text)
                    self.worker_login.start()
        else:
            print("Checking login status")
            QMessageBox.information(self, "Initializing", "Please wait till we initialize the application.")



            # try:
            #     self.whatsapp_bot.open_whatsapp_web()
            # except Exception as e:
            #     self.whatsapp_bot.close()
            #     self.whatsapp_bot.open_whatsapp_web()

    def start_campaign(self):
        """Starts the campaign by sending messages and/or media to contacts."""
        
        if not isUserLoggedInChecked:
            QMessageBox.information(self, "Initializing", "Please wait till we initialize the application.")
            return
        if not isUserLoggedIn:
            QMessageBox.information(self, "WhatsApp Logged Out", "Please login to WhatsApp first.")
            return
        if self.csv_table.rowCount() == 0:
            QMessageBox.warning(self, "Input Error", "No contacts found in the table.")
            return
        if self.subscribe_btn.isVisible():
            QMessageBox.warning(self, "Subscription Required", "Please subscribe to use this feature.")
            return

        contact_column = self.contact_variable.currentText()
        if contact_column == "-- Select --":
            QMessageBox.warning(self, "Input Error", "Please select a contact column.")
            return

        contact_col_idx = -1
        for col in range(self.csv_table.columnCount()):
            if self.csv_table.horizontalHeaderItem(col).text() == contact_column:
                contact_col_idx = col
                break

        if contact_col_idx == -1:
            QMessageBox.warning(self, "Input Error", "Could not find selected contact column.")
            return

        # Check for unused variables in the message
        message_template = self.text_message_field.toPlainText()
        variables_selected_but_unused = []
        for col_name, dropdown in zip(
            ["{{name}}", "{{variable 1}}", "{{variable 2}}", "{{variable 3}}"],
            [self.name_variable, self.var1_variable, self.var2_variable, self.var3_variable]
        ):
            selected_col = dropdown.currentText()
            if selected_col != "-- Select --" and col_name not in message_template:
                variables_selected_but_unused.append(col_name)

        if variables_selected_but_unused:
            QMessageBox.warning(
                self,
                "Input Error",
                f"The following variables are selected in the dropdown but not used in the message template:\n"
                f"{', '.join(variables_selected_but_unused)}"
            )
            return

        contacts = []
        for row in range(self.csv_table.rowCount()):
            contact_item = self.csv_table.item(row, contact_col_idx)
            if contact_item:
                contact = contact_item.text().strip()
                if self.country_code_checkbox.isChecked() and self.note_text.text():
                    contact = self.note_text.text() + contact

                # Prepare the message with variable replacements
                message = message_template
                for col_name, dropdown in zip(
                    ["{{name}}", "{{variable 1}}", "{{variable 2}}", "{{variable 3}}"],
                    [self.name_variable, self.var1_variable, self.var2_variable, self.var3_variable]
                ):
                    selected_col = dropdown.currentText()
                    if selected_col != "-- Select --":
                        col_idx = next(
                            (col for col in range(self.csv_table.columnCount()) 
                            if self.csv_table.horizontalHeaderItem(col).text() == selected_col),
                            None
                        )
                        if col_idx is not None:
                            variable_item = self.csv_table.item(row, col_idx)
                            variable_value = variable_item.text().strip() if variable_item else ""
                            message = message.replace(col_name, variable_value)

                # Add media file path if applicable
                media = self.import_text_field_media.text() if self.dropdown.currentIndex() in [1, 2] else None
                contacts.append({"contact": contact, "message": message, "media": media})

        if not contacts:
            QMessageBox.warning(self, "Input Error", "No contacts found in the selected column.")
            return

        campaign_type = self.dropdown.currentIndex()
        if campaign_type == 0:  # Only Message
            self.log_display.setText("Starting message campaign")
            self.worker_message_campaign = WorkerMessageCampaign(contacts)
            self.worker_message_campaign.whatsapp_bot.log_message.connect(self.update_log)
            self.worker_message_campaign.finishedMessageCampaign.connect(self.display_message_status)
            self.worker_message_campaign.finishedMessageCampaign.connect(self.display_campaign_result)
            self.worker_message_campaign.start()
        elif campaign_type == 1:  # Only Media
            self.log_display.setText("Starting media campaign")
            self.worker_media_campaign = WorkerMediaCampaign(contacts)
            self.worker_media_campaign.whatsapp_bot.log_message.connect(self.update_log)
            self.worker_media_campaign.finishedMediaCampaign.connect(self.display_message_status)
            self.worker_media_campaign.start()
        elif campaign_type == 2:  # Message & Media
            self.log_display.setText("Starting message and media campaign")
            self.worker_media_and_message_campaign = WorkerMediaAndMessageCampaign(contacts)
            self.worker_media_and_message_campaign.whatsapp_bot.log_message.connect(self.update_log)
            self.worker_media_and_message_campaign.finishedMediaAndMessageCampaign.connect(self.display_message_status)
            self.worker_media_and_message_campaign.start()




    def update_log(self, message):
        """Update the log display with new messages."""
        self.log_display.setText(message)
        # Scroll to the bottom of the log
        # self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())

    def display_message_status(self, status):
        """Display status messages from the worker thread."""
        self.log_display.setText(status)
        # Scroll to the bottom of the log
        # self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())
    def display_campaign_result(self, message):
         """Display the final campaign message with success and failure counts."""
         print(message)  # Print to console
         self.log_label.setText(message)  # If using QLabel
         self.log_text_edit.append(message)  # If using QTextEdit


    
    def reset_everything(self):
        """Displays a confirmation dialog before resetting everything."""
        reply = QMessageBox.question(self, "Confirm Reset", 
                                    "Are you sure you want to reset everything?", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset the import text field and the table
            self.import_text_field.setText("")
            self.import_text_field_media.setText("")
            self.text_message_field.setText("")
            self.csv_table.setRowCount(0)
            self.csv_table.setColumnCount(0)
            self.dropdown.setCurrentIndex(0)
            self.name_variable.clear()
            self.contact_variable.clear()
            self.var1_variable.clear()
            self.var2_variable.clear()
            self.var3_variable.clear()
            self.name_variable.addItem("-- Select --")
            self.contact_variable.addItem("-- Select --")
            self.var1_variable.addItem("-- Select --")
            self.var2_variable.addItem("-- Select --")
            self.var3_variable.addItem("-- Select --")
            self.name_variable.setEnabled(False)
            self.contact_variable.setEnabled(False)
            self.var1_variable.setEnabled(False)
            self.var2_variable.setEnabled(False)
            self.var3_variable.setEnabled(False)
            self.import_text_field_media.setEnabled(False)
            self.browse_btn_media.setEnabled(False)
            self.text_message_field.setEnabled(True)



    def open_media_file_dialog(self):
        """Opens a file picker to select a Image/Videos file and display its contents."""
        file_path_media, _ = QFileDialog.getOpenFileName(self, "Open Media", "", "Media Files (*.jpg *.jpeg *.png)")
        if file_path_media:
            self.import_text_field_media.setText(file_path_media)

    def open_data_file_dialog(self):
        """Opens a file picker to select a CSV, Excel, or Google Spreadsheet file and converts it to CSV if needed."""
        
        file_path_data, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "Data Files (*.csv *.xlsx *.xls *.gsheet)")
        
        if file_path_data:
            self.import_text_field.setText(file_path_data)

            if file_path_data.endswith('.csv'):
                # Directly display CSV
                self.display_csv_data(file_path_data)

            elif file_path_data.endswith(('.xlsx', '.xls')):
                # Convert Excel to CSV and then display
                converted_csv = file_path_data.rsplit('.', 1)[0] + ".csv"
                df = pd.read_excel(file_path_data)
                df.to_csv(converted_csv, index=False)
                print(f"Converted Excel to CSV: {converted_csv}")
                self.display_csv_data(converted_csv)

            elif file_path_data.endswith('.gsheet') or file_path_data.startswith("http"):
                # Convert Google Spreadsheet to CSV
                converted_csv = "google_sheet_data.csv"  # Save as a temp CSV file
                gc = gspread.service_account(filename="path/to/service_account.json")
                spreadsheet = gc.open_by_url(file_path_data)  # Or use .open("Sheet Name")
                worksheet = spreadsheet.sheet1
                data = worksheet.get_all_records()
                df = pd.DataFrame(data)
                df.to_csv(converted_csv, index=False)
                print(f"Converted Google Spreadsheet to CSV: {converted_csv}")
                self.display_csv_data(converted_csv)

    def display_csv_data(self, file_path):
        """Loads CSV data and displays it in a QTableWidget."""
        df = read_csv(file_path)
        self.display_data(df)

    def display_excel_data(self, file_path):
        """Loads Excel data and displays it in a QTableWidget."""
        df = read_excel(file_path)
        self.display_data(df)

    def display_data(self, df):
        """Displays data from a DataFrame in a QTableWidget."""
        if not df.empty:
            self.csv_table.setRowCount(df.shape[0])
            self.csv_table.setColumnCount(df.shape[1])
            self.csv_table.setHorizontalHeaderLabels(df.columns)

            # Populate table with data
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    self.csv_table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

            # Enable and populate the variable dropdowns with table headers
            column_headers = df.columns.tolist()
            
            self.name_variable.clear()
            self.contact_variable.clear()
            self.var1_variable.clear()
            self.var2_variable.clear()
            self.var3_variable.clear()

            # Add "None" as the first item
            self.name_variable.addItem("-- Select --")
            self.contact_variable.addItem("-- Select --")
            self.var1_variable.addItem("-- Select --")
            self.var2_variable.addItem("-- Select --")
            self.var3_variable.addItem("-- Select --")

            # Populate dropdowns with column names
            self.name_variable.addItems(column_headers)
            self.contact_variable.addItems(column_headers)
            self.var1_variable.addItems(column_headers)
            self.var2_variable.addItems(column_headers)
            self.var3_variable.addItems(column_headers)

            # Enable the dropdowns once the data is loaded
            self.name_variable.setEnabled(True)
            self.contact_variable.setEnabled(True)
            self.var1_variable.setEnabled(True)
            self.var2_variable.setEnabled(True)
            self.var3_variable.setEnabled(True)


    def update_fields_based_on_selection(self, index):
        """Enables or disables fields based on the dropdown selection."""
        if index == 0:  # Only Message
            self.text_message_field.setEnabled(True)
            self.import_text_field_media.setEnabled(False)
            self.import_text_field_media.setText("")  # Clear the media field if disabled
            self.browse_btn_media.setEnabled(False)
            self.browse_btn_media.clicked.disconnect()  # Disconnect the signal
        elif index == 1:  # Only Media
            self.text_message_field.setEnabled(False)
            self.text_message_field.setText("")  # Clear the message field if disabled
            self.import_text_field_media.setEnabled(True)
            self.browse_btn_media.setEnabled(True)
            try: 
                self.browse_btn_media.clicked.disconnect()  # Disconnect the signal
            except TypeError:
                pass
            self.browse_btn_media.clicked.connect(self.open_media_file_dialog)
        else:  # Message & Media
            self.text_message_field.setEnabled(True)
            self.import_text_field_media.setEnabled(True)
            self.browse_btn_media.setEnabled(True)
            try:
                self.browse_btn_media.clicked.disconnect()  # Disconnect the signal
            except TypeError:
                pass
            self.browse_btn_media.clicked.connect(self.open_media_file_dialog)

    def closeEvent(self, event):
        # Confirmation dialog before closing
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Your custom code to execute on close
            self.on_exit()
            event.accept()  # Accept the event and close the window
        else:
            event.ignore()  # Ignore the close event

    def on_exit(self):
        # Custom code to execute before closing
        print("Executing custom code on exit...")
        # Example: Save application state, release resources, etc.
        # save_application_state()
        # release_resources()

# Application setup
# app = QApplication(sys.argv)

# window = MainWindow()
# window.setWindowIcon(QIcon(resource_path("whatsapp.png")))
# window.show()

# # Start the login check
# worker = WorkerCheckLogin()
# worker.finished.connect(window.update_status)
# worker.start()

app = QApplication(sys.argv)
auth_window = AuthWindow()
auth_window.setWindowIcon(QIcon(resource_path("whatsapp.png")))
auth_window.show()





sys.exit(app.exec())
