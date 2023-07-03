def cargar_lista_db(campo):
    # Configura las credenciales de Firebase
    cred = credentials.Certificate('AccessKey.json')
    firebase_admin.initialize_app(cred)

    # Accede a la base de datos de Firestore
    db = firestore.client()

    # Obtiene una referencia a la colección "CompaCoche"
    ref = db.collection('CompaCoche')

    # Obtiene todos los documentos de la colección "CompaCoche"
    docs = ref.get()

    # Itera sobre los documentos según el campo
    # elementos = []
    #    for doc in docs:
    #        elementos.append(doc.to_dict()[campo])
    #
    #    retorno = []
    #    for i in elementos[0]:
    #        retorno.append(i)
    retorno = []
    retorno.append('')
    elementos = docs[0].to_dict()[campo]
    for i in elementos:
        retorno.append(i)
    retorno.append('Otro')

    # Elimina la aplicación de Firebase
    firebase_admin.delete_app(firebase_admin.get_app())

    return retorno



#Para utilizar esta función, debes pasarle dos argumentos: el nombre de la colección a la que quieres añadir los datos y un diccionario con los datos que quieres añadir. Por ejemplo, si quisieras añadir un nuevo coche a la colección "CompaCoche", podrías hacerlo de la siguiente manera: