from collections import OrderedDict
import datetime
import os
import sys

# Import the Peewee ORM (Object Relational Mapping)
# It allows us to turn database tables intto Python objects and vice versa
from peewee import *

# Our database
db = SqliteDatabase('diary.db')

# This class extends the Peewee class "Model"
# It represents our database table
class Entry(Model):
		# Our attributes / fields
		content = TextField()
		timestamp = DateTimeField(default=datetime.datetime.now) # Gets the timestamp only for when the Entry is created

		# "Meta" class defines our attributes
		class Meta:
			database = db

def initialize():
	"""Create the database and the table if they don't exist."""
	db.connect()
	db.create_tables([Entry], safe=True)

def clear():
	"""Clears the screen."""
	os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
	"""Show the menu"""
	choice = None

	while choice != 'q':
		clear()
		print("Enter 'q' to quit.")
		# Output our menu options
		for key, value in menu_options.items():
			# ".__doc__" holds docstring of a function / method / class
			print('{}) {}'.format(key, value.__doc__))
		choice = input('Action: ').lower().strip()

		if choice in menu_options:
			clear()
			# Call the function the user selected
			menu_options[choice]()

def add_entry():
	"""Add an entry."""
	# "sys" will capture everything the user types until they enter the end of file (EOF) key sequence "Ctrl+Z"
	print('Enter your entry. Press "Ctrl+Z" when finished.')
	data = sys.stdin.read().strip() # Captures user input

	if data: # If we've got data
		# Prompt user to save input
		if input('Save entry? [Yn] ').lower() != 'n':
			Entry.create(content=data) # Creates a new entry
			print("Saved successfully!")

def view_entries(search_query=None):
	"""View previous entries."""
	# Get all the entries and order them by the timestamp so that newest ones come up first
	entries = Entry.select().order_by(Entry.timestamp.desc())

	# If we have a search query then we filter all the entries by the search query before we loop through them
	if search_query:
		# SQL equivalent:
		# SELECT * FROM entry WHERE content LIKE '%search_query'
		entries = entries.where(Entry.content.contains(search_query))

	# Prints out the entries
	for entry in entries:
		timestamp = entry.timestamp.strftime('%A %d %B, %Y %I:%M%p') # Get string for timestamp
		clear()
		print(timestamp)
		print('='*len(timestamp))
		print(entry.content)
		print("\n\n"+"="*len(timestamp))
		print("\n")
		print('N) next entry')
		print('d) delete entry')
		print('q) return to main menu')

		# Allows user to choose next action
		next_action = input("Action: {Ndq} ").lower().strip()
		if next_action == 'q':
			break # Returns to main menu
		elif next_action == 'd':
			delete_entry(entry)

def search_entries():
	"""Search entries for a string."""
	view_entries(input('Search query: '))

def delete_entry(entry):
	"""Delete an entry."""
	if input("Are you sure? [yN]").lower() == 'y':
		entry.delete_instance()
		print("Entry deleted.")

# OrderedDict remembers the order in which things were added
# Does this with a list of tuples
menu_options = OrderedDict([
	('a', add_entry),
	('v', view_entries),
	('s', search_entries),
])

# Makes sure code is only run when the script is executed and not when it's imported
if __name__ == '__main__':
	initialize()
	menu_loop()