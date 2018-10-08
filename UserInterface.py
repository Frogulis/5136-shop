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
    
    Field types:
        int -- whole decimal number 00000
        number -- valid decimal number 00000[.00000]
        money -- float to 2 places 00000.00
        string -- accept any input
        nstring -- string that must be non-empty after strip
        yn -- y or n (case permissive)

    """

    @classmethod
    def writeLine(c, s):
        c._printWhitespace(s)

    @classmethod
    def displayList(c, title, list_items, option_string, aux=None):
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
    def displayConfirm(c, title, msg, aux=None):
        c._printWhitespace(title)
        c._printWhitespace(msg, 2)
        if aux is not None:
            c._printWhitespace(aux, 2)
        i = input('y/n or blank to cancel: ')
        return i

    @classmethod
    def displayItem(c, title, list_items, option_string, aux=None):
        return c.displayList(title, list_items, option_string, aux)


    @classmethod
    def displayForm(c, title, fields, aux=None):
        c._printWhitespace(title)
        inputs = []
        for item in fields:
            c._printWhitespace(item[0], 2)
            inputs.append(input())
        if aux is not None:
            c._printWhitespace(aux, 2)
        return inputs

    @classmethod
    def displayError(c, string):
        print("Error: ", string)
        return None

    @classmethod
    def _printWhitespace(c, s, no_spaces=0, line_end='\n'):
        for i in range(no_spaces):
            print(' ', end='')
        print(s, end=line_end)

    @classmethod
    def displayForm(c, title, fields, aux=None):
        

        c._printWhitespace(title)
        inputs = []
        for item in fields:
            c._printWhitespace(item[0], 2)
            inputs.append(c.tryInput(item))
        if aux is not None:
            c._printWhitespace(aux, 2)
        return inputs

    @classmethod
    def tryInput(c, field):
        def isNumber(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        if field[1] not in ['int', 'number', 'money', 'nstring', 'string', 'yn']:
            raise ValueError('Invalid field type:' + str(field[1]))
        while True:
            newInput = input()
            try:
                if field[1] == 'int' and float(newInput) != round(float(newInput), 0):
                    c.displayError('Please enter a valid whole number')
                elif field[1] == 'number' and not isNumber(newInput):
                    c.displayError('Please enter a valid numerical value')
                elif field[1] == 'money' and float(newInput) != round(float(newInput), 2):
                    c.displayError('Please enter a money value with 2 decimal places')
                elif field[1] == 'nstring' and newInput.strip() == "":
                    c.displayError('Please enter a non-whitespace response')
                elif field[1] == 'yn' and newInput.lower().strip() not in ['y', 'n']:
                    c.displayError("Please enter either 'y' or 'n'")
                else:
                    return newInput
                
            except ValueError:
                c.displayError('Please enter a valid numerical value')


    @classmethod
    def displayError(c, string):
        c._printWhitespace("Error: " + str(string))
        return None


if __name__ == '__main__':
    # testing
    t1 = "A title"
    t2 = \
        "A veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\
eeeeeery long tiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiitle"
    li1 = [('Banana', 'Unit: ea, Source: QLD, Expiry date: 22/22/22, Price: $1'),
           ('Apple', 'Unit: ea, Source: SA, Expiry date: 22/22/22, Price: $1.50'),
           ('Potato', 'Unit: kg, Source: VIC, Expiry date: 22/22/22, Price: $10'),
           ('Marijuana', 'Unit: kg, Source: Himalayas, Expiry date: 22/22/22, Price: $5000')]
    li2 = [('Banalongboynananananananananananananananananananananananananana\
        nananananananana', 'Unit: ea, Source: QLD, Expiry date: 22/22/22, Price: $1'),

           ('Apple', 'Unit: ea, Source: SA, Expiry date: 22/22/22, Price: $1.50'),
           ('Potato', 'Unit: kg, Source: VIC, Expiry date: 22/22/22, Price: $10')]
    f1 = [('Name', 'string'), ('Address', 'nstring'), ('Age', 'int')]
    f2 = [('thing', 'string') for _ in range(10)]
    o1 = 'X to exit, C to continue, W to whatever'

    choice = input("which test u want:\n1. list\n2. form\n3. confirm")
    if choice == '1':
        print("u input: ", UserInterface.displayList(t1, li1, o1))
        print("u input: ", UserInterface.displayList(t2, li2, o1))
        print("u input: ", UserInterface.displayList(t1, li1, o1, 'some aux string'))
    elif choice == '2':
        print("u input: ", UserInterface.displayForm(t1, f1))
        #print("u input: ", UserInterface.displayForm(t2, f2, 'some aux'))
    elif choice == '3':
        print("u input: ", UserInterface.displayConfirm('Confirm purchase',
            'Are you sure you\'d like to proceed?'))
    else:
        print("invalid choice")
