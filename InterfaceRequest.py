from UserInterface import UserInterface

class InterfaceRequest:
	"""Object representing a message passed between Controller and UserInterface
	
	~~~~~~~~~~~~~~~~~~~~~

	To use, ensure that you've run these imports:
	from InterfaceRequest import InterfaceRequest
	from UserInterface import UserInterface
	
	To create, use the relevant factory method. Types of InterfaceRequests and their fields are
	getLIST_DISPLAY(title, list_items, option_string, [aux])
		title: the title of the page overall
		list_items: the list of items in the format (item title, item desc)
		aux: auxiliary field for whatever you like, displayed near bottom
		option_string: available options to display for this page
		single_input: the response from the UI will be placed here
	getFORM_DISPLAY(title, fields, [aux]):
		title: the title of the form overall
		fields: 'questions' to pose to the user of form (question/field name, expected type)
		aux: auxiliary field for whatever you like, displayed near bottom
		inputs: list of inputs given, matching order of 'fields'
	getITEM_DISPLAY(title, list_items, option_string, [aux]):
		title: the title of the page overall
		list_items: the list of items in format (item title, item desc)
		aux: auxiliary field for whatever you like, displayed near bottom
		option_string: available options to display for this page
		single_input: the response from the UI will be placed here
	getCONFIRM_DISPLAY(title, msg, [aux]):
		title: the title of the confirmation dialog
		msg: the message to display with the confirmation
		aux: auxiliary field for whatever you like, displayed near bottom
		response: the response from the UI will be placed here

	Don't attempt to create your own InterfaceRequest(), as these methods will ensure they have the right
	fields!
	
	~~~~~~~~~~~~~~~~~~~~~
	
	Once you have created your object, you may modify it if needed through the getField and setField
	methods. These methods ensure that you only access and mutate fields that are actually present in
	that object. For example, attempting to set the 'inputs' field of a LIST_DISPLAY will result in a TypeError,
	as LIST_DISPLAYS have only a 'single_input', not an 'inputs' list.

	~~~~~~~~~~~~~~~~~~~~~

	Now that your InterfaceRequest is set up, you can display it and get the response back with a statement like:
	my_list_request = UserInterface.display(my_list_request)

	Assuming the object is properly set up, UserInterface will handle it and pass back the object with the user's
	response in the relevant field, which can be accessed like so:
	user_response = my_list_request.getField('single_input')
	
	"""
	def __init__(self, my_dict):
		self.d = my_dict

	def getField(self, field):
		self._checkField(field)
		return self.d[field]

	def setField(self, field, value):
		self._checkField(field)
		self.d[field] = value

	def _checkField(self, field):
		if field not in self.d:
			raise TypeError("field '" + str(field) + "' not in request")

	@staticmethod
	def getLIST_DISPLAY(title, list_items, option_string, aux=None):
		my_dict = {}
		my_dict['type'] = 'LIST_DISPLAY'
		my_dict['title'] = title
		my_dict['list_items'] = list_items
		my_dict['aux'] = aux
		my_dict['option_string'] = option_string
		my_dict['single_input'] = ''
		return InterfaceRequest(my_dict)

	@staticmethod
	def getFORM_DISPLAY(title, fields, aux=None):
		my_dict = {}
		my_dict['type'] = 'FORM_DISPLAY'
		my_dict['title'] = title
		my_dict['fields'] = fields
		my_dict['aux'] = aux
		my_dict['inputs'] = []
		return InterfaceRequest(my_dict)

	@staticmethod
	def getCONFIRM_DISPLAY(title, msg, aux=None):
		my_dict = {}
		my_dict['type'] = 'CONFIRM_DISPLAY'
		my_dict['title'] = title
		my_dict['msg'] = msg
		my_dict['aux'] = aux
		my_dict['response'] = ''
		return InterfaceRequest(my_dict)

	@staticmethod
	def getITEM_DISPLAY(title, list_items, option_string, aux=None):
		output = InterfaceRequest.getLIST_DISPLAY(title, list_items, option_string, aux)
		output.setField('type', 'ITEM_DISPLAY')
		return output

if __name__ == '__main__':
	ir = InterfaceRequest.getLIST_DISPLAY('Search results',
		[('Bananas ea', '$1.00'), ('Bananas kg', '$10.00')],
		'X to exit, C to continue',
		'Total 2 items')
	ir = UserInterface.display(ir)
	print('You said,', ir.getField('single_input'))
	ir2 = InterfaceRequest.getCONFIRM_DISPLAY('Confirm whateer', 'Please confirm that you wish to proceed with the transaction')
	ir2 = UserInterface.display(ir2)
	print('You said,', ir2.getField('response'))
	ir3 = InterfaceRequest.getFORM_DISPLAY('Registration: Please enter your details', [('Name', 'string'), ('Age', 'int')])
	ir3 = UserInterface.display(ir3)
	print('Responses were', ir3.getField('inputs'))
	ir4 = InterfaceRequest.getITEM_DISPLAY('Customer', [('Name', 'Jamie Hoffmann'), ('Age', 23), ('Course', 'MIT')], 'X to exit, E to edit')
	ir4 = UserInterface.display(ir4)
	print('You said,', ir4.getField('single_input'))
