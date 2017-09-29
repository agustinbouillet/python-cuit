import re
import ssl
import json
import urllib.request
from urllib.error import URLError

#  para obtener un cuil a partir del dni
# https://aws.afip.gov.ar/sr-padron/v3/personas/24059752

class Cuil(object):
    provincias = {
        '0':'Ciudad Autónoma de Buenos Aires',
        '1':'Buenos Aires',
        '2':'Catamara',
        '3':'Córdoba',
        '4':'Corrientes',
        '5':'Entre Ríos',
        '6':'Jujuy',
        '7':'Mendoza',
        '8':'La Rioja',
        '9':'Salta',
        '10':'San Juan',
        '11':'San Luis',
        '12':'Santa Fe',
        '13':'Santiago del Estero',
        '14':'Tucumán',
        '16':'Chaco',
        '17':'Chubut',
        '18':'Formosa',
        '19':'Misiones',
        '20':'Neuquén',
        '21':'La Pampa',
        '22':'Río Negro',
        '23':'Santa Cruz',
        '24':'Tierra del Fuego'
    }

    WS_AFIP = "https://soa.afip.gob.ar/sr-padron/v3/persona/{cuil}"
    WS_AMAZON = "https://aws.afip.gov.ar/sr-padron/v3/persona/{cuil}"

    # Codigo de verificacion
    VERIFICACION  = '5432765432'

    def __init__(self, cuil):
        self.cuil = cuil
        self.number = self.filter()


    def webservice_cuil_validator(self, cuil=None, service_uri=None):
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        try:
            url = service_uri.format(cuil=cuil)
            return urllib.request.urlopen(url, context=gcontext)
        except URLError as e:
            print("No es posible obtener datos del webservice AFIP.")
            if hasattr(e, 'reason'):
                print("Error al intentar llegar al servidor.")
                print("Motivo: ", e.reason)
            elif hasattr(e, 'code'):
                print("El servidor no pudo responder a la petición.")
                print("Código de error: ", e.code)

        return None


    def afip_cuil_validator(self):
        """
        Valida un CUIL contra AFIP y amazon
        """
        # Validacion via AFIP
        ws_1 = self.webservice_cuil_validator(self.number, self.WS_AFIP)
        if ws_1:
            try:
                return json.loads(ws_1.read().decode('utf-8'))
            except ValueError:
                print("No se pudo acceder a los servicios de validación")


        # Validacion via amazon
        ws_2 = self.webservice_cuil_validator(self.number, self.WS_AMAZON)
        if ws_2:
            try:
                return json.loads(ws_2.read().decode('utf-8'))
            except ValueError:
                print("No se pudo acceder a los servicios de validación")

        return None


    def validate_digits(self):
        return True if len(self.number) == 11 else False


    def validate_valid_chars(self):
        '''
        Valida si la infomración pasada por parámetro es adecuada.
        Caracteres válidos (\d-.\s)
        '''
        regex = r"^([\d\-\.\s]+)$"
        matches = re.search(regex, self.cuil)
        if matches:
                return True
        return False


    def filter(self):
        '''
        Limpia el valor de cualquier caracter que no sea un número.
        '''
        regex = r"[^\d]"
        subst = ""
        result = re.sub(regex, subst, str(self.cuil), 0)
        return result


    def __digito_verificador(self):
        cuil = self.number

        v1 = 0
        for i in range(10): v1 += int(self.VERIFICACION[i]) * int(cuil[i])

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
            m.append('El código “{0}”, es válido.'.format(self.cuil))
        else:
            m.append("""Introdujo: “{0}”, y éste no es un \
número de CUIL válido.""".format(self.cuil))

        if not self.validate_valid_chars():
            m.append("""Solo puede introducir: números, guiones medios, \
puntos o espacios.""")

        if not self.validate_digits():
            m.append('El CUIL debe tener 11 dígitos.')

        return m


    def is_valid(self):
        num = self.number
        if self.validate_valid_chars()\
        and self.validate_digits()\
        and self.__digito_verificador():
            return True
        return False



if __name__ == "__main__":
    n = input('Ingrese un número de CUIL: ')
    o = Cuil(n)

    if o.is_valid():
        data_afip = o.afip_cuil_validator()
        print(data_afip)


    print('\n')
    for i in o.get_messages():
        print('---',i)
    print('\n')
