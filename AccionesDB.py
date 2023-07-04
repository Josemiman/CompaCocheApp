import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


#¡Ho
#datos = {
#    "Zonas": "Puerto de la Torre1"
#}

#agregar_datos_db("CompaCoche", datos)
#```

def modificar_dato_db(id, campo, valor):
    # Configura las credenciales de Firebase
    cred = credentials.Certificate('AccessKey.json')
    firebase_admin.initialize_app(cred)

    # Accede a la base de datos de Firestore
    db = firestore.client()

    # Obtiene una referencia al documento que se desea modificar
    ref = db.collection('CompaCoche').document(id)

    # Modifica el campo deseado con el nuevo valor
    ref.update({campo: valor})

    # Elimina la aplicación de Firebase
    firebase_admin.delete_app(firebase_admin.get_app())

    return "El documento con ID {} ha sido modificado exitosamente".format(id)

#En esta función, debes pasar como parámetros el ID del documento que deseas modificar, el campo que deseas modificar y el nuevo valor que deseas asignar. Recuerda que debes tener los permisos necesarios para modificar datos en la base de datos..

#modificar_dato_db('Usuarios', 'Mortadelo', ['pwd','caca'])

def cargar_lista_db(documento, campo):
    # Configura las credenciales de Firebase
    cred = credentials.Certificate('AccessKey.json')
    firebase_admin.initialize_app(cred)

    # Accede a la base de datos de Firestore
    db = firestore.client()


    # Obtiene una referencia al documento especificado
    ref = db.collection('CompaCoche').document(documento)

    # Obtiene el documento especificado y lo convierte a un diccionario de Python
    doc = ref.get().to_dict()

    try:
        # Obtiene el campo especificado del diccionario y lo convierte a una lista
        elementos = doc[campo]

        # Agrega los elementos a la lista de retorno
        retorno = []
        for i in elementos:
            retorno.append(i)

        retorno.append('Otro')

        # Elimina la aplicación de Firebase
        firebase_admin.delete_app(firebase_admin.get_app())

        return retorno
    except:
        # Elimina la aplicación de Firebase
        firebase_admin.delete_app(firebase_admin.get_app())

        return ['None']

#Aquí tienes una función modificada que te permitirá añadir un elemento a un campo de tipo array:

def agregar_elemento_array(coleccion, id_documento, campo, elemento):
    # Configura las credenciales de Firebase
    cred = credentials.Certificate('AccessKey.json')
    firebase_admin.initialize_app(cred)

    # Accede a la base de datos de Firestore
    db = firestore.client()

    # Añade el elemento al campo de tipo array
    db.collection(coleccion).document(id_documento).update({
        campo: firestore.ArrayUnion([elemento])
    })

    # Elimina la aplicación de Firebase
    firebase_admin.delete_app(firebase_admin.get_app())

    return "Elemento añadido correctamente al campo de tipo array"


#En esta función, debes pasar el nombre de la colección, el ID del documento, el nombre del campo de tipo array al que deseas añadir el elemento y el valor del elemento que deseas añadir.

#El método `update()` se utiliza para actualizar el campo de tipo array utilizando `firestore.ArrayUnion([elemento])`, que añade el elemento al campo existente sin duplicarlo.

#Espero que esto te sea útil. ¡Si tienes alguna otra pregunta, estaré encantado de ayudarte! 😊👍

#agregar_elemento_array('CompaCoche', 'FormData', 'Zonas','Mordor Norte')

def agregar_datos_db(coleccion, id_documento, datos):
    # Configura las credenciales de Firebase
    cred = credentials.Certificate('AccessKey.json')
    firebase_admin.initialize_app(cred)

    # Accede a la base de datos de Firestore
    db = firestore.client()

    # Actualiza los datos en el documento especificado
    db.collection(coleccion).document(id_documento).update(datos)

    # Elimina la aplicación de Firebase
    firebase_admin.delete_app(firebase_admin.get_app())

    return "Datos añadidos correctamente"


def verificar_usuario_db(user, password):
    # Como el usuario lo guardo en la bbdd como un diccionario en el que la clave es el usuario y el valor una lista de datos
    # #uso try para intentar recuperarlo
    try:
        contra = cargar_lista_db('Usuarios', user)
        if contra[0] == password:
            return True
        else:
            return False
    # Si no existe la clave (usuario), devuelve KeyError y uso esa excepción para devolver False
    except KeyError:
        return False

def verificar_nuevo_usuario(user, password):
    return False