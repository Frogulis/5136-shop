class UserInterface:
	@classmethod
	def display(c, request):
		if request.getField('type') == 'LIST_DISPLAY':
			return c.displayList(request)
		else:
			return c.displayError(request)

	@classmethod
	def displayList(c, request):
		c._printWhitespace(request.getField('title'))
		for item in request.getField('list_items'):
			c._printWhitespace(item[0], 2)
			c._printWhitespace(item[1], 4)
		c._printWhitespace(request.getField('option_string'))
		i = input('Please input option')
		request.setField('single_input', i)
		return request


	@classmethod
	def displayError(c, request):
		print("Couldn't display request of type ", request.getField('type'))
		return request

	@classmethod
	def _printWhitespace(c, s, no_spaces=0, line_end='\n'):
		for i in range(no_spaces):
			print(' ', end='')
		print(s)