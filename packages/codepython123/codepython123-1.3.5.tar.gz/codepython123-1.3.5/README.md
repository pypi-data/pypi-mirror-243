use the library in other Python scripts. 
Create a new Python script in a different directory and 
import and use the send function from the library

```
from python.xTemplate import Template as template

self.template = template()

self.template.send_email(table_html)

[Email]
smtp_server='mrelay.noc.sony.co.jp'
smtp_port=25
sender='SCK-VOS_MAP_SYSTEM@sony.com'


python setup.py sdist bdist_wheel

twine upload dist/*


def db_commit_many(self, params):
    try:
        db_connection = self.database_connector.connectPostgreSQL(**params)
        db_connection.commit_many(params['query'], params['values'])

    except Exception as error:
        self.handle_error(error)

# Example of using the function
self.db_params = {
            'database' : 'office',
            'host' : '43.24.188.114',
            'user' : 'office',
            'password' : 'office',
            'port' : '5432',
            'query': None,
            'values': None
        }

def getUser(self):
        query = f"SELECT user_id FROM office.tm_user WHERE user_id = '{self.globalid}' "  
        return self.template.db_fetchall(self.db_params,query)



 def send_input(self):
        body = self.send_message()
        recipient = {'recipient':f'{self.recipient_entry.get("1.0", "end-1c")}'}
        self.email_message.update(recipient)
        subject = {'subject':f'{self.title_entry.get("1.0", "end-1c")}'}
        self.email_message.update(subject)
        message_body = {'body':body}
        self.email_message.update(message_body)

        self.template.send_email(self.email_message)
        pass

    def send_message(self):
        self.email_message = {
                "recipient": "",
                "recipient_cc": "",
                "subject": "",
                "header": "",
                "body": "",
                "footer":"",
                "sender" : self.sender,
                "smtp_server" : 'mrelay.noc.sony.co.jp',
                "smtp_port" : 25
            }
```

