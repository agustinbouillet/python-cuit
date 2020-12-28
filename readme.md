# Validador de CUIT

El Código Único de Identificación Tributaria (CUIT) es una clave que se
utiliza en el sistema tributario de la República Argentina para poder
identificar inequívocamente a las personas físicas o jurídicas autónomas,
susceptibles de tributar. Las claves son asignadas por la Administración
Federal de Ingresos Públicos (AFIP), para poder confeccionar el registro
o censo de las mismas, para efectos administrativos y tributarios.

Más información en: https://es.wikipedia.org/wiki/Clave_%C3%9Anica_de_Identificaci%C3%B3n_Tributaria


## Uso

```python
codigo = "34-99903208-9"
c = cuit.Cuit(codigo)
```

### is_valid()

Retorna un valor _boolean_.

```python
>>> c.is_valid()
True
```

### codigo_verificador()

Retorna el número verificador que corresponde para el código ingresado 
independientemente de cual lleve.

```python
>>> c.codigo_verificador()
9
```

### messages()

Retorna una lista con los mensajes de éxito o error.

#### True

```python
>>> c.messages()
['El código «34-99903208-9», es válido.']
```

#### False

```python
>>> c = cuit.Cuit("34+99903208+9")
>>> c.messages()
['Introdujo «34+99903208+9» y éste no es un número de CUIT válido.',
 'Solo puede introducir: números, guiones medios, puntos o espacios.']
```

```python
>>> c = cuit.Cuit("foo")
>>> c.messages()
['Introdujo «foo» y éste no es un número de CUIT válido.',
 'Solo puede introducir: números, guiones medios, puntos o espacios.',
 'El CUIT debe tener 11 dígitos.']
```

```python
>>> c = cuit.Cuit("3499903208")
>>> c.messages()
['Introdujo «3499903208» y éste no es un número de CUIT válido.',
 'El CUIT debe tener 11 dígitos.']
```


## Uso por línea de comando

Argumentos `-c` o `--cuit`. Retorna una validación del tipo _boolean_.

```bash
$ python3 cuit.py -c 34-99903208-9
True
```

Argumentos `-m` o `--msg`. Lista los mensajes de error o éxito.

```bash
$ python3 cuit.py -c 34-99903208-9 -m
— El código «34-99903208-9», es válido.
```

```bash
$ python3 cuit.py -c 34-99903208 -m
— Introdujo «34-99903208» y éste no es un número de CUIT válido.
— El CUIT debe tener 11 dígitos.
```

Argumentos `-d` o `--digito`. Retorna el número verificador que
corresponde para el código ingresado independientemente de cual lleve.

```bash
$ python3 cuit.py -c 34-99903208-9 -d
9
```

---


[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=C5TSLQQEEE5PQ)



