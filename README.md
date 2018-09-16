Diary App created with Python using the Peewee ORM (Object Relational Mapping).

Project was created to demonstrate working with databases in Python.

To run the app simply open a command line in the same directory as the diary.py file. Type "python diary.py", and then write away at your diary.

Once you run the file, a "diary.db" file will be created in your project directory. This is a database file. You can use sqlite3 to look through the database. You may need to install sqlite3 with "pip install pysqlite3".

Commands to view entries with sqlite3:
  - sqlite3 diary.db
  - .tables
  - select * from entry;
