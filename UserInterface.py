class UserInterface:
	@classmethod
	def writeLine(c, s):
		c._printWhitespace(s)

	@classmethod
	def display(c, request):
		t = request.getField('type')
		if t == 'LIST_DISPLAY':
			return c._displayList(request)
		elif t == 'CONFIRM_DISPLAY':
			return c._displayConfirm(request)
		elif t == 'FORM_DISPLAY':
			return c._displayForm(request)
		elif t == 'ITEM_DISPLAY':
			return c._displayItem(request)
		else:
			return c._displayError(request)

	@classmethod
	def _displayList(c, request):
		c._printWhitespace(request.getField('title'))
		for item in request.getField('list_items'):
			c._printWhitespace(item[0], 2)
			c._printWhitespace(item[1], 4)
		if request.getField('aux') is not None:
			c._printWhitespace(request.getField('aux'), 2)
		c._printWhitespace(request.getField('option_string'))
		i = input('Please input option: ')
		request.setField('single_input', i)
		return request

	@classmethod
	def _displayConfirm(c, request):
		c._printWhitespace(request.getField('title'))
		c._printWhitespace(request.getField('msg'), 2)
		if request.getField('aux') is not None:
			c._printWhitespace(request.getField('aux'), 2)
		i = input('y/n or blank to cancel: ')
		request.setField('response', i)
		return request

	@classmethod
	def _displayItem(c, request):
		return c._displayList(request)

	@classmethod
	def _displayForm(c, request):
		c._printWhitespace(request.getField('title'))
		inputs = []
		for item in request.getField('fields'):
			c._printWhitespace(item[0], 2)
			inputs.append(input())
		request.setField('inputs', inputs)
		if request.getField('aux') is not None:
			c._printWhitespace(request.getField('aux'), 2)
		return request

	@classmethod
	def _displayError(c, request):
		print("Couldn't display request of type ", request.getField('type'))
		return request

	@classmethod
	def _printWhitespace(c, s, no_spaces=0, line_end='\n'):
		for i in range(no_spaces):
			print(' ', end='')
		print(s)