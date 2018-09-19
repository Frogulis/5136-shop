from UserInterface import UserInterface

class InterfaceRequest:
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
	def getLIST_DISPLAY(title, list_items, option_string):
		my_dict = {}
		my_dict['type'] = 'LIST_DISPLAY'
		my_dict['title'] = title
		my_dict['list_items'] = list_items
		my_dict['option_string'] = option_string
		my_dict['single_input'] = ''
		return InterfaceRequest(my_dict)

	@staticmethod
	def getFORM_DISPLAY(title, fields):
		my_dict = {}
		my_dict['type'] = 'FORM_DISPLAY'
		my_dict['title'] = title
		my_dict['fields'] = fields
		my_dict['inputs'] = []
		return InterfaceRequest(my_dict)

	@staticmethod
	def getCONFIRM_DISPLAY(title, msg):
		my_dict = {}
		my_dict['type'] = 'CONFIRM_DISPLAY'
		my_dict['title'] = title
		my_dict['msg'] = msg
		my_dict['response'] = ''
		return InterfaceRequest(my_dict)

	@staticmethod
	def getITEM_DISPLAY(title, list_items, option_string):
		output = InterfaceRequest.getLIST_DISPLAY(title, list_items, option_string)
		output.setField('type', 'ITEM_DISPLAY')
		return output

if __name__ == '__main__':
	ir = InterfaceRequest.getLIST_DISPLAY('Search results', [('Bananas ea', '$1.00'), ('Bananas kg', '$10.00')], 'X to exit, C to continue')
	ir = UserInterface.display(ir)
	print('You said,', ir.getField('single_input'))
	ir2 = InterfaceRequest.getCONFIRM_DISPLAY('Confirm whateer', 'Please confirm that you wish to proceed with the transaction')
	ir2 = UserInterface.display(ir2)
	print('You said,', ir2.getField('response'))
