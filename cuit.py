# -*- coding: utf-8 -*-
"""Validador de CUIL/CUIT

El Código Único de Identificación Tributaria (CUIT) es una clave que se
utiliza en el sistema tributario de la República Argentina para poder
identificar inequívocamente a las personas físicas o jurídicas autónomas,
susceptibles de tributar. Las claves son asignadas por la Administración
Federal de Ingresos Públicos (AFIP), para poder confeccionar el registro
o censo de las mismas, para efectos administrativos y tributarios.

@See:
https://es.wikipedia.org/wiki/Clave_%C3%9Anica_de_Identificaci%C3%B3n_Tributaria
"""
import re

class Cuit:
  # Codigo de verificacion
  VERIFICACION  = '5432765432'
  MESSAGES = {
      'valid'          : 'El código «{cuit}», es válido.',
      'invalid'        : ('Introdujo «{cuit}» y éste no es un número de CUIT '
                         'válido.'),
      'invalid_chars'  : ('Solo puede introducir: números, guiones medios, '
                         'puntos o espacios.'),
      'invalid_length' : 'El CUIT debe tener 11 dígitos.'
  }


  def __init__(self, cuit):
    self.cuit   = cuit
    self.number = self.filter()


  def validate_digits(self):
    return True if len(self.number) == 11 else False


  def validate_valid_chars(self):
    '''Valida si la infomración pasada por parámetro es adecuada.
    Caracteres válidos (\d-.\s)
    '''
    regex = r'^([\d\-\.\s]+)$'
    matches = re.search(regex, self.cuit)
    if matches:
        return True
    return False


  def filter(self):
    '''Limpia el valor de cualquier caracter que no sea un número.
    '''
    regex = r'[^\d]'
    subst = ''
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
    """Mensajes de validación.
    """
    mensajes = []
    if self.is_valid():
      mensajes.append(self.MESSAGES.get('valid').format(cuit=self.cuit))
    else:
      mensajes.append(self.MESSAGES.get('invalid').format(cuit=self.cuit))

    if not self.validate_valid_chars():
      mensajes.append(self.MESSAGES.get('invalid_chars'))

    if not self.validate_digits():
      mensajes.append(self.MESSAGES.get('invalid_length'))

    return mensajes


  def is_valid(self):
    num = self.number
    if self.validate_valid_chars()\
        and self.validate_digits()\
        and self.__digito_verificador():
      return True

    return False



if __name__ == '__main__':
  n = input('Ingrese un número de CUIT: ')
  o = Cuit(n)
  print(o.MESSAGES)
  [print('—',i) for i in o.get_messages()]
  print('\n')
