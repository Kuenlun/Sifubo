##########################################
##                                      ##
## Simplificador de funciones booleanas ##
##                                      ##
##########################################

class Digital():
    allowed_vars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = allowed_vars + '01'
    allowed = alphabet + '+*<>()'

    def __init__(self, function):
        self.function = function

    @property
    def variables(self):
        '''Returns a list with all the variables in a function'''
        variables = list()
        for char in self.function:
            if char not in variables:
                if char in Digital.allowed_vars:
                    variables.append(char)
        variables.sort()
        return variables

    @property
    def evaluable(self):
        '''Returns the evaluable expression of a Digital function'''
        return Digital.create_evaluable(self.function, list())[1]

    def evaluate(self, values):
        '''Solves the Digital function for the given values'''
        var = dict(zip(self.variables, values))
        order = self.evaluable
        for i, operation in enumerate(order):
            # Check if expression is negated
            if operation[0] == '!': negate = True
            else:                   negate = False
            if negate: expression = operation[1:]
            else:      expression = operation
            # Check wich kind of operation is if it is an operation
            sum = False
            pro = False
            aux = True
            if '+' in expression:
                sum = True
                a, b = expression.split('+')
            elif '*' in expression:
                pro = True
                a, b = expression.split('*')
            else:
                aux = False
                if expression == '0' or expression == '1':
                    result = Digital(expression)
                else:
                    result = Digital(var[expression])
            if aux:
                # Check if is a pointer and replace
                if a[0] == '$':
                    a = order[int(a[1:])]
                if b[0] == '$':
                    b = order[int(b[1:])]
                # Replace variables with values
                if a != '0' and a != '1':
                    a = var[a]
                if b != '0' and b != '1':
                    b = var[b]
                # Convert to Digital objects
                a = Digital(a)
                b = Digital(b)
                # Operate
                if sum: result = a + b
                else:   result = a * b
            # Negate if necesary
            if negate:
                result.negate()
            # Replace result in list
            order[i] = str(result)
        return result

    @staticmethod
    def create_evaluable(function, order):
        '''Determinates the order in wich operations will be done'''
        # If there is only one character in function
        if len(function) == 1:
            order.append(function)
            function = '$' + str(len(order)-1)
            return function, order
        # Basement
        for i in '()<>+*':
            if i in function:
                break
        else:
            return function, order
        # Brackets
        while(True):
            c = 0
            for i, char in enumerate(function):
                # Look for outter brackets and process it's content
                if char == '(':
                    c += 1
                    if c == 1:
                        start = i
                elif char == ')':
                    c -= 1
                    if c == 0:
                        solved, order = Digital.create_evaluable(function[start+1:i], order)
                        # Replace what has been solved
                        function = function[:start] + str(solved) + function[i+1:]
                        break
            else:
                # If for has finished without breaking
                break
        # Negations
        while(True):
            c = 0
            for i, char in enumerate(function):
                # Look for outter brackets and process it's content
                if char == '<':
                    c += 1
                    if c == 1:
                        start = i
                elif char == '>':
                    c -= 1
                    if c == 0:
                        solved, order = Digital.create_evaluable(function[start+1:i], order)
                        order[-1] = '!' + order[-1]
                        # Replace what has been solved
                        function = function[:start] + str(solved) + function[i+1:]
                        break
            else:
                # If for has finished without breaking
                break
        # Products
        while(True):
            dollar = None
            for i, char in enumerate(function):
                if char == '$':
                    dollar = i
                elif char == '+':
                    dollar = None
                elif char == '*':
                    # First element
                    if not(dollar is None):
                        a = function[dollar:i]
                    else:
                        a = function[i-1]
                    # Second element
                    if function[i+1] == '$':
                        for j, letter in enumerate(function[i+2:]):
                            if letter in '*+':
                                b = function[i+1:i+2+j]
                                break
                        else:
                            b = function[i+1:]
                    else:
                        b = function[i+1]
                    order.append(f'{a}*{b}')
                    # Replace what has been solved
                    function = function[:i-len(a)] + '$' + str(len(order)-1) + function[i+1+len(b):]
                    break
            else:
                # If for has finished without breaking
                break
        # Additions
        while(True):
            dollar = None
            for i, char in enumerate(function):
                if char == '$':
                    dollar = i
                elif char == '*':
                    dollar = None
                elif char == '+':
                    # First element
                    if not(dollar is None):
                        a = function[dollar:i]
                    else:
                        a = function[i-1]
                    # Second element
                    if function[i+1] == '$':
                        for j, letter in enumerate(function[i+2:]):
                            if letter in '*+':
                                b = function[i+1:i+2+j]
                                break
                        else:
                            b = function[i+1:]
                    else:
                        b = function[i+1]
                    order.append(f'{a}+{b}')
                    # Replace what has been solved
                    function = function[:i-len(a)] + '$' + str(len(order)-1) + function[i+1+len(b):]
                    break
            else:
                # If for has finished without breaking
                break
        # Last recurrence
        if len(function) > 1:
            return Digital.create_evaluable(function, order)
        else:
            return function, order

    def __str__(self):
        return self.function

    def __repr__(self):
        return str(self.evaluable)

    def __add__(self, other):
        if len(self.function) == 1 and len(other.function) == 1:
            if self.function == '1' or other.function == '1':
                return Digital('1')
            else:
                return Digital('0')

    def __mul__(self, other):
        if len(self.function) == 1 and len(other.function) == 1:
            if self.function == '1' and other.function == '1':
                return Digital('1')
            else:
                return Digital('0')

    def negate(self):
        '''Negates the Digital function'''
        if len(self.function) == 1:
            if self.function == '1':
                self.function == '0'
            else:
                self.function == '1'

    def truth_table(self):
        '''Shows the truth table of a Digital function'''
        # Show the variables as indices
        for variable in self.variables:
            print(variable, '\t', end='')
        print('\tX')

        # Show rows
        exponent = len(self.variables)
        for variation in Digital.binary_variations(exponent):
            result = self.evaluate(variation)
            for num in variation:
                print(num, '\t', end='')
            print('\t' + str(result))

    @staticmethod
    def binary_variations(exponent):
        '''Returns a generator of all binary variations given a exponent'''
        for _ in range(2**exponent):
            binary = bin(_)[2:]
            zeros = exponent - len(binary)
            variation = '0'*zeros + binary
            yield variation

    # EN DESARROLLO '(<A+<B>)>' Sigue fallando la comprobación de entrada
    @staticmethod
    def syntax_check(str_input):
        '''Checks the syntax of a Digital function'''
        ## Assert input isn't empty
        if not str_input:
            raise SyntaxError('Input must contain something')

        ## Assert that the input doen't have invalid characters
        for char in str_input:
            if char not in Digital.allowed:
                raise SyntaxError(f'"{char}" is not a valid character')

        ## Assert all brackets and negations are coupled
        c_br = 0
        c_ng = 0
        for char in str_input:
            if   char == '(': c_br += 1
            elif char == '<': c_ng += 1
            elif char == ')': c_br -= 1
            elif char == '>': c_ng -= 1
            # More brackets closed than opened
            if c_br < 0: raise SyntaxError('Incorrect bracket syntax')
            # More negations closed than opened
            if c_ng < 0: raise SyntaxError('Incorrect negation syntax')
        if c_br != 0:    raise SyntaxError('Missing closing bracket')
        if c_ng != 0:    raise SyntaxError('Missing closing negation')

        ## To not allow inputs like this: (<(>))
        # Copy the function but just with () and <>
        function = [x for x in str_input if x in '<>()']
        for i in range(len(function)-1):
            # Check function in chunks of 2 chars
            chunk = str().join(function[i:i+2])
            if chunk == '(>' or chunk == '<)':
                raise SyntaxError('Bad bracket/negation syntax')

        ## Assert no empty brackets
        if '()' in str_input: raise SyntaxError('Empty brackets')

        ## Assert no empty negations
        if '<>' in str_input: raise SyntaxError('Empty negation')

        ## Assert there aren't operators together
        flag = False
        for i, char in enumerate(str_input):
            if char == '*' or char == '+':
                if flag: raise SyntaxError('Two opetator together')
                flag = True
            else:
                flag = False

        ## Assert beginning and ending don't start/finish with operator
        if len(str_input) > 0:
            if str_input[0] == '+' or str_input[0] == '*':
                raise SyntaxError(f"Input can't start with an operator")
            if str_input[-1] == '+' or str_input[-1] == '*':
                raise SyntaxError(f"Input can't finish with an operator")

        ## Assert there aren't invalid operations
        invalid_operations = ('(+', '(*', '+)', '*)', '<+', '<*', '+>', '*>')
        for operation in invalid_operations:
            if operation in str_input:
                raise SyntaxError(f'Invalid syntax: "{operation}"')

    @staticmethod
    def fill_mult(str_input):
        '''Fills the omited products (*) of an input'''
        gaps = ('vv', 'v(', ')v', ')(', 'v<', '>v', '><')
        filled_input = list(str_input)
        c = 0
        for i in range(len(str_input)-1):
            # Check str_input in chunks of 2 chars
            chunk = list(str_input[i:i+2])
            if chunk[0] in Digital.alphabet: chunk[0] = 'v'
            if chunk[1] in Digital.alphabet: chunk[1] = 'v'
            chunk_str = str().join(chunk)
            if chunk_str in gaps:
                filled_input.insert(i+1+c, '*')
                c += 1
        return str().join(filled_input)

    @classmethod
    def from_string(cls, str_input):
        '''Parses a string into a Digital object'''
        str_input = str_input.upper().replace(' ', '')
        cls.syntax_check(str_input)
        str_input = cls.fill_mult(str_input)
        return cls(str_input)



####################
# Entrada de datos #
####################
entrada = 'AB'
bool_funct = Digital.from_string(entrada)
print(f'Function:\nf = {bool_funct}')
print(bool_funct.evaluable)

bool_funct.truth_table()
