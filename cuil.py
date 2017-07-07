import re

class Cuit(object):
    # Codigo de verificacion
    VERIFICACION  = '5432765432'

    def __init__(self, cuit):
        self.cuit = cuit
        self.number = self.filter()


    def validate_digits(self):
        return True if len(self.number) == 11 else False


    def validate_valid_chars(self):
        '''
        Valida si la infomración pasada por parámetro es adecuada.
        Caracteres válidos (\d-.\s)
        '''
        regex = r"^([\d\-\.\s]+)$"
        matches = re.search(regex, self.cuit)
        if matches:
                return True
        return False


    def filter(self):
        '''
        Limpia el valor de cualquier caracter que no sea un número.
        '''
        regex = r"[^\d]"
        subst = ""
        result = re.sub(regex, subst, str(self.cuit), 0)
        return result


    def __digito_verificador(self):
        # Digitos verificadores, por cada uno debe multiplicarse los numeros del cuit
        # respectivamente
        # EJ.
        # CUIT = 20258024428
        #   2025802442
        # x 5432765432
        # ------------

        cuit = self.number

        v1 = 0
        for i in range(10): v1 += int(self.VERIFICACION[i]) * int(cuit[i])

        # obtengo el resto
        v2 = v1 % 11
        # 11 menos el resto
        v3 = 11 - v2
        # si el ressultado de v3 es == 11. El valor es 0
        if v3 == 11:
            r = 0
        # si v3 es igual a 10. El valor es 9
        elif v3 == 10:
            # return False
            r = 9
        # en todos los demas casos es el v3
        else:
            r = v3

        if int(self.number[-1:]) == r:
            return True
        return False


    def get_messages(self):
        m = []
        if self.is_valid():
            m.append('El código “{0}”, es válido.'.format(self.cuit))
        else:
            m.append('Introdujo: “{0}”, y éste no es un número de CUIT válido.'.format(self.cuit))

        if not self.validate_valid_chars():
            m.append('Solo puede introducir: números, guiones medios, puntos o espacios.')

        if not self.validate_digits():
            m.append('El CUIT debe tener 11 dígitos.')

        return m


    def is_valid(self):
        num = self.number
        if self.validate_valid_chars()\
        and self.validate_digits()\
        and self.__digito_verificador():
            return True
        return False



if __name__ == "__main__":
    n = input('Ingrese un número de CUIT: ')
    o = Cuit(n)

    print('\n')
    for i in o.get_messages():
        print('---',i)
    print('\n')
