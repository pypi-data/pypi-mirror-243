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


pip install Pillow
pip install psycopg2
pip install pysonPostgreSQL
pip install xMySQL
pip install xOracle
pip install xConfigparser
pip install psycopg2-binary python-dotenv mysql-connector colorama
pip install sqlalchemy
pip install cx_Oracle
```

