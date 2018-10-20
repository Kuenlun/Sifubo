##########################################
#                                        #
#  Simplificador de Funciones Booleanas  #
#                                        #
##########################################


class Digital():
    def __init__(self, value):
        if value == '0':
            self.value = False
        elif value:
            self.value = True
        else:
            self.value = False

    def __str__(self):
        if self.value:
            return '1'
        else:
            return '0'

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        if self.value or other.value:
            return Digital(1)
        else:
            return Digital(0)

    def __mul__(self, other):
        if self.value and other.value:
            return Digital(1)
        else:
            return Digital(0)

    def negate(self):
        '''Negates the Digital input'''
        if self.value:
            self.value = False
        else:
            self.value = True


class DigitalFunction():
    allowed_vars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = allowed_vars + '01'
    allowed = alphabet + '+*<>()'

    def __init__(self, function):
        self.function = function

    def __str__(self):
        # Delete all product signs
        function = DigitalFunction.erase_mult(self.function)
        # Space all sum
        out_list = [f' + ' if char == '+' else char for char in function]
        function = str().join(out_list)
        return function

    def __repr__(self):
        return self.function

    def __add__(self, other):
        function = f'{self.function}+{other.function}'
        return DigitalFunction(function)

    def __mul__(self, other):
        function = f'({self.function})*({other.function})'
        return DigitalFunction(function)

    #####
    # Object property related
    #####
    @property
    def variables(self):
        '''Returns a list with all the variables in a function'''
        variables = list()
        for char in self.function:
            if char not in variables:
                if char in DigitalFunction.allowed_vars:
                    variables.append(char)
        variables.sort()
        return variables

    @property
    def evaluable(self):
        '''Returns the evaluable expression of a Digital function'''
        return DigitalFunction.create_evaluable(self.function, list())[1]

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
                # Look for inner brackets and process it's content
                if char == '(':
                    c += 1
                    if c == 1:
                        start = i
                elif char == ')':
                    c -= 1
                    if c == 0:
                        solved, order = DigitalFunction.create_evaluable(function[start+1:i], order)
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
                        solved, order = DigitalFunction.create_evaluable(function[start+1:i], order)
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
            return DigitalFunction.create_evaluable(function, order)
        else:
            return function, order

    #####
    # Methods
    #####
    def evaluate(self, values):
        '''Solves the Digital function for the given values'''
        var = dict(zip(self.variables, values))
        order = self.evaluable
        for i, operation in enumerate(order):
            # Check if expression is negated
            if operation[0] == '!':
                negate = True
            else:
                negate = False
            if negate:
                expression = operation[1:]
            else:
                expression = operation
            # Check wich kind of operation is if it is an operation
            sum = False
            aux = True
            if '+' in expression:
                sum = True
                a, b = expression.split('+')
            elif '*' in expression:
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
                if sum:
                    result = a + b
                else:
                    result = a * b
            # Negate if necesary
            if negate:
                result.negate()
            # Replace result in list
            order[i] = str(result)
        return result

    def negate(self):
        '''Negates the DigitalFunction input'''
        self.function = f'<{self.function}>'

    def truth_table(self):
        '''Shows the truth table of a Digital function'''
        # Show the variables as indices
        for variable in self.variables:
            print(variable, '\t', end='')
        print('\tX')

        # Show rows
        exponent = len(self.variables)
        for variation in DigitalFunction.binary_variations(exponent):
            result = self.evaluate(variation)
            for num in variation:
                print(num, '\t', end='')
            print('\t' + str(result))

    def first_canonical(self):
        '''Returns the first canonical form of a digital function'''
        out_list = list()
        variables = self.variables
        exponent = len(variables)
        for variation in DigitalFunction.binary_variations(exponent):
            result = self.evaluate(variation)
            if result.value:
                term_list = list()
                for i, num in enumerate(variation):
                    if num == '1':
                        term_list.append(variables[i])
                    else:
                        term_list.append(f'<{variables[i]}>')
                term = str().join(term_list)
                # Product of nums in term
                term = DigitalFunction.fill_mult(term)
                out_list.append(term)
        # Sum of terms
        out_list = [f'{x}+' for x in out_list]
        # Delete last +
        out_list[-1] = out_list[-1][:-1]
        out = str().join(out_list)
        return DigitalFunction(out)

    def sum_of_minterms(self):
        '''Returns the sum of minterms of a digital function'''
        out_list = list()
        variables = self.variables
        exponent = len(variables)
        for i, variation in enumerate(DigitalFunction.binary_variations(exponent)):
            result = self.evaluate(variation)
            if result.value:
                out_list.append(i)
        return tuple(out_list)

    def second_canonical(self):
        '''Returns the second canonical form of a digital function'''
        out_list = list()
        variables = self.variables
        exponent = len(variables)
        for variation in DigitalFunction.binary_variations(exponent):
            result = self.evaluate(variation)
            if not result.value:
                term_list = list()
                for i, num in enumerate(variation):
                    if num == '0':
                        term_list.append(variables[i])
                    else:
                        term_list.append(f'<{variables[i]}>')
                # Sum of nums in term
                term_list = [f'{x}+' for x in term_list]
                # Delete last +
                term_list[-1] = term_list[-1][:-1]
                term = str().join(term_list)
                out_list.append(term)
        # Product of terms
        out_list = [f'({x})*' for x in out_list]
        # Delete last product
        out_list[-1] = out_list[-1][:-1]
        out = str().join(out_list)
        return DigitalFunction(out)

    def prod_of_maxterms(self):
        '''Returns the product of maxterms of a digital function'''
        out_list = list()
        variables = self.variables
        exponent = len(variables)
        for i, variation in enumerate(DigitalFunction.binary_variations(exponent)):
            result = self.evaluate(variation)
            if not result.value:
                out_list.append(i)
        return tuple(out_list)

    # Remains a lot to do here
    def pretty(self):
        '''Returns a pretty string of the function'''
        # Delete all product signs
        function = DigitalFunction.erase_mult(self.function)
        # Space all sum
        out_list = [f' + ' if char == '+' else char for char in function]
        function = str().join(out_list)
        return function

    #####
    # Input related functions
    #####
    @classmethod
    def from_string(cls, str_input):
        '''Parses a string into a Digital object'''
        str_input = str_input.upper().replace(' ', '')
        cls.syntax_check(str_input)
        str_input = cls.fill_mult(str_input)
        return cls(str_input)

    @staticmethod
    def syntax_check(str_input):
        '''Checks the syntax of a Digital function'''
        # Assert input isn't empty
        if not str_input:
            raise SyntaxError('Input must contain something')

        # Assert that the input doen't have invalid characters
        for char in str_input:
            if char not in DigitalFunction.allowed:
                raise SyntaxError(f'"{char}" is not a valid character')

        # Assert all brackets and negations are coupled
        c_br = 0
        c_ng = 0
        for char in str_input:
            if char == '(':
                c_br += 1
            elif char == '<':
                c_ng += 1
            elif char == ')':
                c_br -= 1
            elif char == '>':
                c_ng -= 1
            # More brackets closed than opened
            if c_br < 0:
                raise SyntaxError('Incorrect bracket syntax')
            # More negations closed than opened
            if c_ng < 0:
                raise SyntaxError('Incorrect negation syntax')
        if c_br != 0:
            raise SyntaxError('Missing closing bracket')
        if c_ng != 0:
            raise SyntaxError('Missing closing negation')

        # To not allow inputs like this: (<(>))
        DigitalFunction.brng_syntax(str_input)

        # Assert no empty brackets
        if '()' in str_input:
            raise SyntaxError('Empty brackets')

        # Assert no empty negations
        if '<>' in str_input:
            raise SyntaxError('Empty negation')

        # Assert there aren't operators together
        flag = False
        for i, char in enumerate(str_input):
            if char == '*' or char == '+':
                if flag:
                    raise SyntaxError('Two opetator together')
                flag = True
            else:
                flag = False

        # Assert beginning and ending don't start/finish with operator
        if len(str_input) > 0:
            if str_input[0] == '+' or str_input[0] == '*':
                raise SyntaxError(f"Input can't start with an operator")
            if str_input[-1] == '+' or str_input[-1] == '*':
                raise SyntaxError(f"Input can't finish with an operator")

        # Assert there aren't invalid operations
        invalid_operations = ('(+', '(*', '+)', '*)', '<+', '<*', '+>', '*>')
        for operation in invalid_operations:
            if operation in str_input:
                raise SyntaxError(f'Invalid syntax: "{operation}"')

    @staticmethod
    def brng_syntax(f):
        '''To not allow inputs like this: (<(>))'''
        while(True):
            c_br = 0
            c_ng = 0
            for i, char in enumerate(f):
                # Look for inner brackets/negations and process it's content
                if char == '(':
                    c_br += 1
                    if c_br == 1:
                        prev_br = i
                elif char == '<':
                    c_ng += 1
                    if c_ng == 1:
                        prev_ng = i
                elif char == ')':
                    c_br -= 1
                    if c_br == 0:
                        if '<' in f[prev_br+1:i] or '>' in f[prev_br+1:i]:
                            # Calls brng again with inner info
                            DigitalFunction.brng_syntax(f[prev_br+1:i])
                            # Erases inner info
                            f = f[:prev_br] + f[i+1:]
                        else:
                            # Delete brackets and inner stuff
                            f = f[:prev_br] + f[i+1:]
                        break
                elif char == '>':
                    c_ng -= 1
                    if c_ng == 0:
                        if '(' in f[prev_ng+1:i] or ')' in f[prev_ng+1:i]:
                            # Calls brng again with inner info
                            DigitalFunction.brng_syntax(f[prev_ng+1:i])
                            # Erases inner info
                            f = f[:prev_ng] + f[i+1:]
                        else:
                            # Delete negations and inner stuff
                            f = f[:prev_ng] + f[i+1:]
                        break
            else:
                # If for has finished without breaking
                if c_br != 0 or c_ng != 0:
                    raise SyntaxError('Bad bracket/negation syntax')
                break

    @staticmethod
    def fill_mult(str_input):
        '''Fills the omited products (*) of an input'''
        gaps = ('vv', 'v(', ')v', ')(', 'v<', '>v', '><')
        filled_input = list(str_input)
        c = 0
        for i in range(len(str_input)-1):
            # Check str_input in chunks of 2 chars
            chunk = list(str_input[i:i+2])
            if chunk[0] in DigitalFunction.alphabet:
                chunk[0] = 'v'
            if chunk[1] in DigitalFunction.alphabet:
                chunk[1] = 'v'
            chunk_str = str().join(chunk)
            if chunk_str in gaps:
                filled_input.insert(i+1+c, '*')
                c += 1
        return str().join(filled_input)

    @staticmethod
    def erase_mult(str_input):
        out_list = [char for char in str_input if char != '*']
        return str().join(out_list)

    #####
    # Related to digital
    #####
    @staticmethod
    def binary_variations(exponent):
        '''Returns a generator of all binary variations given a exponent'''
        for _ in range(2**exponent):
            binary = bin(_)[2:]
            zeros = exponent - len(binary)
            variation = '0'*zeros + binary
            yield variation


############
#  Example #
############
# Give an input
input = 'AB+(C*D)'
print(f'Input: {input}\n')
# Convert the input into a DigitalFunction object
function = DigitalFunction.from_string(input)
print('DigitalFunction Object')
print(f'f = {function}\n')
# Show the sum of minterms
print('Sum of Minterms')
print(function.sum_of_minterms())
print()
# Show the first canonical form of the function
function_canonical = function.first_canonical()
print('First Canonical Form')
print(f'f = {function_canonical}\n')
# Show the table of truth of the function
print('Table of Truth')
function.truth_table()
