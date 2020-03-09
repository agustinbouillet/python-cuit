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
import argparse
import re


class Cuit:
  # Codigo de verificacion
  VERIFICATION_CODE  = '5432765432'
  MESSAGES = {
      'valid'          : 'El código «{cuit}», es válido.',
      'invalid'        : ('Introdujo «{cuit}» y éste no es un número de CUIT '
                         'válido.'),
      'invalid_chars'  : ('Solo puede introducir: números, guiones medios, '
                         'puntos o espacios.'),
      'invalid_length' : 'El CUIT debe tener 11 dígitos.'
  }


  def __init__(self, cuit):
    self.cuit   = str(cuit)
    self.number = self.filter_chars()


  def validate_digits(self):
    return True if len(self.number) == 11 else False


  def validate_chars(self):
    '''Valida si la infomración pasada por parámetro es adecuada.
    Caracteres válidos (\d-.\s)
    '''
    try:
      regex   = r'^([\d\-\.\s]+)$'
      matches = re.search(regex, self.cuit)
      if matches:
          return True
      return False
    except:
      return False


  def filter_chars(self):
    '''Limpia el valor de cualquier caracter que no sea un número.
    '''
    regex  = re.compile(r'[^\d]')
    subst  = ''
    result = re.sub(regex, subst, self.cuit, 0)
    return result


  def digito_verificador(self):
    """Calcula el dígito verificador.

    Digitos verificadores, por cada uno debe multiplicarse los numeros
    del cuit respectivamente.

    Returns:
      [int] -- Número verificador
    """
    cuit = self.number
    digito_verificador = None

    v1 = 0
    for i in range(10):
      v1 += int(Cuit.VERIFICATION_CODE[i]) * int(cuit[i])

    # obtengo el resto
    v2 = v1 % 11
    # 11 menos el resto
    v3 = 11 - v2
    # si el ressultado de v3 es == 11. El valor es 0
    if v3 == 11:
      digito_verificador = 0
    # si v3 es igual a 10. El valor es 9
    elif v3 == 10:
      # return False
      digito_verificador = 9
    # en todos los demas casos es el v3
    else:
      digito_verificador = v3

    return digito_verificador


  def is_valid_digito_verificador(self):
    """Valida que el número verificador coincida con el del número de
    CUIL ingresado.

    Returns:
      bool
    """
    digito_verificador = self.digito_verificador()
    if int(self.number[-1:]) == digito_verificador:
      return True

    return False


  def messages(self):
    """Mensajes de validación.
    """
    mensajes = []
    if self.is_valid():
      mensajes.append(self.MESSAGES.get('valid').format(cuit=self.cuit))
    else:
      mensajes.append(self.MESSAGES.get('invalid').format(cuit=self.cuit))

    if not self.validate_chars():
      mensajes.append(self.MESSAGES.get('invalid_chars'))

    if not self.validate_digits():
      mensajes.append(self.MESSAGES.get('invalid_length'))

    return mensajes


  def is_valid(self):
    num = self.number
    if self.validate_chars()\
        and self.validate_digits()\
        and self.is_valid_digito_verificador():
      return True

    return False



if __name__ == '__main__':

  parser = argparse.ArgumentParser(
      description='Permite guardar un rango de fechas de conteo.')

  parser.add_argument(
      '-c',
      '--cuit',
      type=str,
      help=('El número de CUIL solo puede contener números, guiones '
            'medios, puntos o espacios.')
  )
  parser.add_argument(
      '-m',
      '--msg',
      type=bool,
      help='Muestra los mensajes.')
  parser.add_argument(
      '-d',
      '--digit',
      type=bool,
      help=('Muestra el dígito verificador correspondiente al número de '
           'CUIT ingresado.')
  )

  args = parser.parse_args()
  c = Cuit(args.cuit)


  if args.digit:
    print(c.digito_verificador())

  elif args.msg:
    [print('—',i) for i in c.messages()]

  else:
    print(c.is_valid())
