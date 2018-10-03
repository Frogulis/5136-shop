class UserInterface:
	"""User interface boundary class

	Users of this class only need to worry about these methods:

	displayList(title, list_items, option_string, [aux])
		title: the title of the page overall
		list_items: the list of items in the format (item title, item desc)
		aux: auxiliary field for whatever you like, displayed near bottom
		option_string: available options to display for this page
		single_input: the response from the UI will be placed here
	displayForm(title, fields, [aux]):
		title: the title of the form overall
		fields: 'questions' to pose to the user of form (question/field name, expected type)
		aux: auxiliary field for whatever you like, displayed near bottom
		inputs: list of inputs given, matching order of 'fields'
	displayItem(title, list_items, option_string, [aux]):
		title: the title of the page overall
		list_items: the list of items in format (item title, item desc)
		aux: auxiliary field for whatever you like, displayed near bottom
		option_string: available options to display for this page
		single_input: the response from the UI will be placed here
	displayConfirm(title, msg, [aux]):
		title: the title of the confirmation dialog
		msg: the message to display with the confirmation
		aux: auxiliary field for whatever you like, displayed near bottom
		response: the response from the UI will be placed here
	displayError(msg):
		msg: the error message to display

	writeLine(s)
	This will write a string to the output. Use sparingly, only when the prefab interfaces
	are inadequate.
	
	"""

	@classmethod
	def writeLine(c, s):
		c._printWhitespace(s)

	@classmethod
	def _displayList(c, title, list_items, option_string, aux=None):
		c._printWhitespace(title)
		for item in list_items:
			c._printWhitespace(item[0], 2)
			c._printWhitespace(item[1], 4)
		if aux is not None:
			c._printWhitespace(aux, 2)
		c._printWhitespace(option_string)
		i = input('Please input option: ')
		return i

	@classmethod
	def _displayConfirm(c, title, msg, aux=None):
		c._printWhitespace(title)
		c._printWhitespace(msg, 2)
		if aux is not None:
			c._printWhitespace(aux, 2)
		i = input('y/n or blank to cancel: ')
		return i

	@classmethod
	def _displayItem(c, title, list_items, option_string, aux=None):
		return c._displayList(title, list_items, option_string, aux)

	@classmethod
	def _displayForm(c, title, fields, aux=None):
		c._printWhitespace(title)
		inputs = []
		for item in fields:
			c._printWhitespace(item[0], 2)
			inputs.append(input())
		if aux is not None:
			c._printWhitespace(aux, 2)
		return inputs

	@classmethod
	def _displayError(c, string):
		print("Error: ", string)
		return None

	@classmethod
	def _printWhitespace(c, s, no_spaces=0, line_end='\n'):
		for i in range(no_spaces):
			print(' ', end='')
		print(s, end=line_end)

if __name__ == '__main__':
	#testing
	t1 = "A title"
	t2 = "A veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\
	eeeeeery long tiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiitle"
	li1 = [('Banana', 'Unit: ea, Source: QLD, Expiry date: 22/22/22, Price: $1'),
			('Apple', 'Unit: ea, Source: SA, Expiry date: 22/22/22, Price: $1.50'),
			('Potato', 'Unit: kg, Source: VIC, Expiry date: 22/22/22, Price: $10'),
			('Marijuana', 'Unit: kg, Source: Himalayas, Expiry date: 22/22/22, Price: $5000')]
	li2 = [('Banalongboynananananananananananananananananananananananananana\
		nananananananana', 'Unit: ea, Source: QLD, Expiry date: 22/22/22, Price: $1'),
			('Apple', 'Unit: ea, Source: SA, Expiry date: 22/22/22, Price: $1.50'),
			('Potato', 'Unit: kg, Source: VIC, Expiry date: 22/22/22, Price: $10')]
	f1 = [('Name', 'string'), ('Address', 'string'), ('Age', 'int')]
	f2 = [('thing', 'string') for _ in range(10)]
	o1 = 'X to exit, C to continue, W to whatever'
	displayList(t1, li1, o1)
	displayList(t2, li2, o1)
	displayList(t1, li1, o1, 'some aux string')
	