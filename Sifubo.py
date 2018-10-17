##########################################
##                                      ##
## Simplificador de funciones booleanas ##
##                                      ##
##########################################

class digital():
    def __init__(self, value):
        if value == '0':
            self.value = False
        elif value:
            self.value = True
        else:
            self.value = False

    def __add__(self, other):
        if self.value or other.value:
            return True
        else:
            return False

    def __mul__(self, other):
        if self.value and other.value:
            return True
        else:
            return False

    def __str__(self):
        return str(self.value)

    def __int__(self):
        if self.value:
            return 1
        else:
            return 0

    def negate(self):
        return not self.value

    @staticmethod
    def evaluate(expression):
        # Minima recurrencia
        if len(expression) == 1:
            return digital(expression)

        ##### Establecemos un orden en las operaciones
        # Paréntesis
        while(True):
            contador = 0
            for i, char in enumerate(expression):
                # Buscamos paréntesis exteriores y procesamos su contenido
                if char == '(':
                    contador += 1
                    if contador == 1:
                        inicio = i
                elif char == ')':
                    contador -= 1
                    if contador == 0:
                        resuelto = digital.evaluate(expression[inicio+1:i])
                        # Quitamos lo que ya hemos evaluado
                        expression_list = list()
                        for j, letra in enumerate(expression):
                            if j < inicio or j > i:
                                expression_list.append(letra)
                        # Introducimos el resultado de lo evaluado
                        expression_list.insert(inicio, str(int(resuelto)))
                        expression = str().join(expression_list)
                        # Rompemos el for
                        break
            else:
                # Si hemos completado el for sin break
                break

        # Negaciones
        while(True):
            contador = 0
            for i, char in enumerate(expression):
                # Buscamos negaciones exteriores y procesamos su contenido
                if char == '<':
                    contador += 1
                    if contador == 1:
                        inicio = i
                elif char == '>':
                    contador -= 1
                    if contador == 0:
                        resuelto = digital.evaluate(expression[inicio+1:i]).negate()
                        # Quitamos lo que ya hemos evaluado
                        expression_list = list()
                        for j, letra in enumerate(expression):
                            if j < inicio or j > i:
                                expression_list.append(letra)
                        # Introducimos el resultado de lo evaluado
                        expression_list.insert(inicio, str(int(resuelto)))
                        expression = str().join(expression_list)
                        # Rompemos el for
                        break
            else:
                # Si hemos completado el for sin break
                break

        # Multiplicaciones
        while(True):
            for i, char in enumerate(expression):
                if char == '*':
                    factor1 = digital(expression[i-1])
                    factor2 = digital(expression[i+1])
                    resuelto = factor1 * factor2
                    # Quitamos lo que ya hemos evaluado
                    expression_list = list()
                    for j, letra in enumerate(expression):
                        if j < i-1 or j > i+1:
                            expression_list.append(letra)
                    # Introducimos el resultado de lo evaluado
                    expression_list.insert(i-1, str(int(resuelto)))
                    expression = str().join(expression_list)
                    # Rompemos el for
                    break
            else:
                # Si hemos completado el for sin break
                break

        # Sumas
        while(True):
            for i, char in enumerate(expression):
                if char == '+':
                    factor1 = digital(expression[i-1])
                    factor2 = digital(expression[i+1])
                    resuelto = factor1 + factor2
                    # Quitamos lo que ya hemos evaluado
                    expression_list = list()
                    for j, letra in enumerate(expression):
                        if j < i-1 or j > i+1:
                            expression_list.append(letra)
                    # Introducimos el resultado de lo evaluado
                    expression_list.insert(i-1, str(int(resuelto)))
                    expression = str().join(expression_list)
                    # Rompemos el for
                    break
            else:
                # Si hemos completado el for sin break
                break

        # Recurrimos una vez más para finalizar
        return digital.evaluate(expression)


class digital_expression(digital):
    variables_permitidas = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    alfabeto = variables_permitidas + '01'
    validas = alfabeto + '+*<>()'

    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return self.expression

    @property
    def variables(self):
        # Creamos una lista con todas las variables
        variables = list()
        for char in self.expression:
            if char not in variables:
                if char in digital_expression.variables_permitidas:
                    variables.append(char)
        variables.sort()
        return variables

    def truth_table(self):
        '''Crea la tabla de verdad de la funcion'''
        # Si la expresión está vacía
        if not self.expression:
            raise ValueError('Expression is empty')

        variables = self.variables
        exponente = len(variables)

        # Mostramos los índices
        for variable in variables:
            print(variable, '\t', end='')
        print('\tX')

        for i in range(2**exponente):
            expression = self.expression
            # Obtenemos las variaciones binarias
            binario = bin(i)[2:]
            ceros = exponente - len(binario)
            variation = '0'*ceros + binario

            for cambio in zip(variables, variation):
                expression = expression.replace(cambio[0], cambio[1])
            result = super().evaluate(expression)
            result = str(int(result))

            # Mostramos la fila
            for num in variation:
                print(num, '\t', end='')
            print('\t'+ result)

    @staticmethod
    def syntax_check(entrada):
        '''Comprueba la sintaxis de un string'''
        # Comprobamos el input no contenga carácteres inválidos
        for char in entrada:
            if char not in digital_expression.validas:
                raise SyntaxError(f'"{char}" is not a valid character')

        # Comprobamos que todos los paréntesis esten emparejados
        contador = 0
        for char in entrada:
            if char == '(':
                contador += 1
            elif char == ')':
                contador -= 1
            # Si se han cerrado más de los que se han abierto
            if contador < 0:
                raise SyntaxError('Incorrect brackets syntax')
        if contador != 0:
            raise SyntaxError('Missing closing brackets')

        # Comprobamos que todas las negaciones esten emparejadas
        contador = 0
        for char in entrada:
            if char == '<':
                contador += 1
            elif char == '>':
                contador -= 1
            if contador < 0:
                raise SyntaxError('Incorrect negation syntax')
        if contador != 0:
            raise SyntaxError('Missing closing negations')

        # Comprobamos que no hayan paréntesis vacios
        if '()' in entrada:
            raise SyntaxError('Empty brackets')

        # Comprobamos que no hayan negaciones vacias
        if '<>' in entrada:
            raise SyntaxError('Empty negation')

        # Comprobamos que no hayan signos seguidos
        flag = False
        for i, char in enumerate(entrada):
            if char == '*' or char == '+':
                if flag:
                    raise SyntaxError('Too many operations')
                flag = True
            else:
                flag = False

        # Comprobamos que la entrada no empieze ni acabe por un operador
        if len(entrada) > 0:
            if entrada[0] == '+' or entrada[0] == '*':
                raise SyntaxError(f"Input can't start with an operator")
            if entrada[-1] == '+' or entrada[-1] == '*':
                raise SyntaxError(f"Input can't finish with an operator")

        # Comprobamos demás fallos de sintaxis
        invalid_parent_syntax = ('(+', '(*', '+)', '*)', '<+', '<*', '+>', '*>')
        for invalid in invalid_parent_syntax:
            if invalid in entrada:
                raise SyntaxError(f'Invalid syntax: "{invalid}"')

    @staticmethod
    def rellenar_mult(entrada):
        gaps = ('vv', 'v(', ')v', ')(', 'v<', '>v', '><')
        entrada_filled = list(entrada)
        contador = 0
        for i in range(len(entrada)-1):
            # Cogemos trozos de 2 en 2
            trozo = list(entrada[i:i+2])
            if trozo[0] in digital_expression.alfabeto: trozo[0] = 'v'
            if trozo[1] in digital_expression.alfabeto: trozo[1] = 'v'
            trozo_str = str().join(trozo)
            if trozo_str in gaps:
                entrada_filled.insert(i+1+contador, '*')
                contador += 1
        return str().join(entrada_filled)

    @classmethod
    def from_string(cls, entrada):
        entrada = entrada.upper().replace(' ', '')
        cls.syntax_check(entrada)
        entrada = cls.rellenar_mult(entrada)
        return cls(entrada)


##################
# Entrada de datos
##################
entrada = 'A'
bool_funct = digital_expression.from_string(entrada)
print('Function')
print(f'f = {bool_funct}\n')

bool_funct.truth_table()
