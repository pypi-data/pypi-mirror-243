import os
import csv
import json
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import logging
import ctypes
from psycopg2 import Error
from python.xPostgreSQL import Config as PostgreSQLConfig
from python.xMySQL import Config as MySQLConfig
from python.xConfigparser import Config as Config
from colorama import init, Fore, Back, Style

class DatabaseConnector:
    def __init__(self, db, host, user, pw, port, schemas):
        self.db = db
        self.host = host
        self.user = user
        self.pw = pw
        self.port = port
        self.schemas = schemas

    def connectPostgreSQL(self,db,host,user,pw,port,schemas):
        try:
            # PostgreSQLConfigクラスを使用してデータベースに接続
            connection = PostgreSQLConfig(db, host, user, pw, port, schemas)
            return connection
        except (Exception, Error) as error:
            # データベースへの接続中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"データベースへの接続エラー: {error}")
        
    def connectMySQL(self,db,host,user,pw):
        try:
            # PostgreSQLConfigクラスを使用してデータベースに接続
            connection = MySQLConfig(db, host, user, pw)
            return connection
        except (Exception, Error) as error:
            # データベースへの接続中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"データベースへの接続エラー: {error}")

class EmailNotifier:
    def __init__(self, smtp_server,smtp_port,sender):
        self.smtp_server=smtp_server
        self.smtp_port=smtp_port
        self.sender = sender

    def get_files_in_folders(folder_paths):
        file_paths = []
        file_names = []
        for folder_path in folder_paths:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_paths.append(os.path.join(root, file))
                    file_names.append(file)
        return file_paths, file_names


    def send_email(self,subject,header,body,footer,recipients,recipients_cc,sender):
        try:
            # Email details
            if self.smtp_server != None:
                smtp_server = self.smtp_server
            else:
                smtp_server = 'mrelay.noc.sony.co.jp'
            if self.smtp_port != None:    
                smtp_port = self.smtp_port
            else:
                smtp_port = '25'

            # Create a MIME text object
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ';'.join(recipients)
            if recipients_cc!='':
                msg['CC'] = ';'.join(recipients_cc)

            table_html = ''
            if body != '':
                table_html = body
            
            # Create the email body as HTML
            message = header
            message += f'<html><body>{table_html}</body></html>'
            message += footer

            # Attach the email body
            msg.attach(MIMEText(message, 'html'))

            # Connect to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                try:    
                    server.sendmail(sender, recipients, msg.as_string())
                    return 1
                except Exception as e:
                    print('An error occurred:', str(e))
                    return 0
                finally:
                    # Disconnect from the SMTP server
                    server.quit()
        except Exception as e:
            # Email通知の送信中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"Email通知の送信エラー: {e}")


class Template:
    def __init__(self,config_file):
        # Configクラスを使用して設定ファイルから設定を読み込む
        self.db = None
        self.host = None
        self.user = None
        self.pw = None
        self.port = None
        self.schemas = None
        self.log = None
        self.console_title = None
        self.smtp_server = None
        self.smtp_port = None
        self.sender = None

        
        try:
            self.configuration = Config(config_file)
            try:
                self.db = self.configuration.get('DB', 'db')
            except Exception as e:
                pass
            self.host = self.configuration.get('DB', 'host')
            self.user = self.configuration.get('DB', 'user')
            self.pw = self.configuration.get('DB', 'pw')
            self.port = self.configuration.get('DB', 'port')
            self.schemas = self.configuration.get('DB', 'schemas')
        except Exception as e:
            pass

        try:
            self.smtp_server = self.configuration.get('EMAIL', 'smtp_server')
            self.smtp_port = self.configuration.get('EMAIL', 'smtp_port')
        except Exception as e:
            pass

        try:
            self.sender = self.configuration.get('EMAIL', 'sender')
        except Exception as e:
            pass
            
        try:
            self.log = self.configuration.get('PARAM', 'log')
        except Exception as e:
            pass

        try:
            self.console_title = self.configuration.get('PARAM', 'console_title')
        except Exception as e:
            pass
        

        # DatabaseConnectorおよびEmailNotifierの初期化
        self.database_connector = DatabaseConnector(
            self.db,
            self.host,
            self.user,
            self.pw,
            self.port,
            self.schemas
        )
        self.email_notifier = EmailNotifier(
            self.smtp_server,
            self.smtp_port,
            self.sender
        )

        # その他の変数の初期化...
        self.console_title = self.console_title

        console_handle = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.kernel32.SetConsoleTitleW(self.console_title)

        init(autoreset=True)        
        if self.log:                                    # autoreset=Trueを設定して、Coloramaのテキストリセットを有効にします。
            logging.basicConfig(filename=self.log, level=logging.INFO, encoding="utf-8")

    def config(self,section,value):
        return self.configuration.get(section, value)

    def load_localization(self,language_code):
        with open(f'{language_code}.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def list_files_in_folder(self,folder_path):
        filename_array = []
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, filename)):
                    filename_array.append(filename)
        return filename_array

    def read_csv_file(self,file_path):
        data = []
        try:
            with open(file_path, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    data.append(row)

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return data

    def move_directory(self, source_file_path, destination_path, filename):
        if os.path.exists(destination_path+filename):
            shutil.rmtree(destination_path)  # Remove the destination directory if it exists
        #os.makedirs(destination)  # Ensure the destination directory exists
        shutil.move(source_file_path, destination_path)  # Move the entire directory

    def delete_directory(self,folder_path):
        try:
            # Use shutil.rmtree to delete the folder and its contents
            shutil.rmtree(folder_path)
            print(f"Folder at {folder_path} and its contents have been deleted.")
        except FileNotFoundError:
            print(f"Folder at {folder_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def export_to_csv(self,data_table,file_path,message):
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            
            # Write the header row
            header = [data_table.heading(column)["text"] for column in data_table["columns"]]
            writer.writerow(header)

            # Write the data rows
            for row_id in data_table.get_children():
                row = [data_table.item(row_id, "values")[i] for i in range(len(header))]
                writer.writerow(row)

        messagebox.showinfo("INFO", message)


    def db_fetchall(self,db,host,user,pw,port,schemas,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL2(db,host,user,pw,port,schemas)
            # クエリの実行
            return db_connection.fetchall(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def db_commit(self,db,host,user,pw,port,schemas,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL2(db,host,user,pw,port,schemas)
            # クエリの実行
            db_connection.commit(query)
            return "OK"
        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            return error

    def db_commit_values(self,db,host,user,pw,port,schemas,query,values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL2(db,host,user,pw,port,schemas)
            # クエリの実行
            db_connection.commit_values(query,values)
            return "OK"
        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            return error

    def db_commit_many(self,db,host,user,pw,port,schemas, query, values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL2(db,host,user,pw,port,schemas)
            # クエリの実行
            db_connection.commit_many(query, values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_fetchall(self,db,host,user,pw,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(db,host,user,pw)
            # クエリの実行
            return db_connection.fetchall(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_commit(self,db,host,user,pw,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(db,host,user,pw)
            # クエリの実行
            db_connection.commit(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_commit_values(self,db,host,user,pw,query,values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(db,host,user,pw)
            # クエリの実行
            db_connection.commit_values(query,values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def mySQL_commit_many(self, db,host,user,pw,query, values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL(db,host,user,pw)
            # クエリの実行
            db_connection.commit_many(query, values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("xTemplate Error:", error)
            self.handle_error(error)

    def run_interval(self):
        while True:
            print("システムを起動しています")
            if not self.in_process_flag:
                self.in_process_flag = True
                try:
                    self.main()
                finally:
                    self.in_process_flag = False
            interval = int(self.interval)
            time.sleep(interval)
 
    def handle_error(self, error):
        print("xTemplate Error:", error)
        logging.basicConfig(filename="error.log", level=logging.ERROR)
        # 現在の日時を取得
        now = datetime.datetime.now()
        # エラーログを記録
        logging.error(now.strftime("%Y-%m-%d %H:%M:%S") + " " + str(error))

    def print(self, OKNG,info):
        now = datetime.datetime.now()
        if OKNG == "OK":
            # OKの場合のメッセージ
            message = f" {Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}{now.strftime('%Y-%m-%d %H:%M:%S')}{Back.BLACK} {info} {Style.NORMAL}"
        else:
            # NGの場合のメッセージ
            message = f" {now.strftime('%Y-%m-%d %H:%M:%S')}{Fore.WHITE}{Back.RED}{Style.BRIGHT} {info} {Style.NORMAL}"

        print(message)

    def logging_date(self,info):
        now = datetime.datetime.now()
        log_message = f" {now.strftime('%Y-%m-%d %H:%M:%S')} {info}"
        logging.info(log_message)

    def logging(self,info):
        log_message = f" {info}"
        logging.info(log_message)

    def send_email(self, message):
        # Extract message components from the dictionary
        message_body = message.get("message_body")
        recipient = message.get("recipient")
        recipient_cc = message.get("recipient_cc")
        subject = message.get("subject")
        header = message.get("header")
        header2 = message.get("header2")
        footer = message.get("footer")
        footer2 = message.get("footer2")
        try:
            sender = message.get("sender")
        except Exception as error:
            pass

        recipient = recipient.split(';')
        recipient_cc = recipient_cc.split(';')
        message_header = f"{header}<br><br>"
        message_header += f"<font style='color:blue;font-weight:bold;font-size:18px'>{header2}</font><br><br>"
        message_footer = f"<br><br>{footer}<br><br>{footer2}"
        # Email通知の送信
        if sender:
            self.email_notifier.send_email2(subject, message_header,message_body, message_footer, recipient, recipient_cc, sender)
        else:
            self.email_notifier.send_email(subject, message_header,message_body, message_footer, recipient, recipient_cc)

    def set_window_position(self,root,window,width,height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        # Set the window size and position for the master window
        window.geometry(f"{width}x{height}+{x}+{y}")

    def fix_window_position(self,window, root):
        window.update_idletasks()
        window_width, window_height = window.winfo_width(), window.winfo_height()
        master_width, master_height = root.winfo_width(), root.winfo_height()
        center_x = root.winfo_x() + (master_width - window_width) // 2
        center_y = root.winfo_y() + (master_height - window_height) // 2
        window.geometry(f"+{center_x}+{center_y}")

    def create_label_and_entry(self, frame, label_text, row, column, width, fontsize):
        label = ttk.Label(frame, text=label_text, font=("Helvetica", fontsize), justify="right")
        label.grid(row=row, column=column, padx=1, sticky="e")

        entry = ttk.Entry(frame, width=width, font=("Helvetica", fontsize), justify="center")
        entry.grid(row=row, column=column + 1, padx=1)

        return label, entry

    def create_button(self, frame, text, command, style, image, row, column, rowspan=1, padx=(10, 0), pady=(1, 1), sticky="n"):
        button = ttk.Button(frame, text=text, command=command, style=style)
        button.grid(row=row, column=column, rowspan=rowspan, pady=pady, padx=padx, sticky=sticky)
        button.config(image=image, compound=tk.LEFT)
        return button