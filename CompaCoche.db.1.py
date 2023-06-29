import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import AccionesDB
from AccionesDB import modificar_dato_db
#from AccionesDB import cargar_lista_db
from AccionesDB import agregar_elemento_array

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog

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
    #elementos = []
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
    
class LoginDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Inicio de sesión')
        self.setGeometry(100, 100, 300, 150)

        self.user_label = QLabel('Usuario:', self)
        self.user_input = QLineEdit(self)

        self.password_label = QLabel('Contraseña:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.accept_button = QPushButton('Aceptar', self)
        self.cancel_button = QPushButton('Cancelar', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.user_label)
        vbox.addWidget(self.user_input)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.accept_button)
        hbox.addWidget(self.cancel_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_user_password(self):
        user = self.user_input.text()
        password = self.password_input.text()
        return user, password

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Compartir coche'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Establecer el color de fondo
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(200, 255, 200))
        self.setPalette(palette)

        horario_label = QLabel('Horario:', self)
        horario_combobox = QComboBox(self)
        horario_combobox.addItems(cargar_lista_db('Horario'))
        horario_combobox.setCurrentIndex(-1)

        turno_label = QLabel('Turno:', self)
        turno_combobox = QComboBox(self)
        turno_combobox.addItems(cargar_lista_db('Turnos'))
        turno_combobox.setCurrentIndex(-1)

        zona_label = QLabel('Zona:', self)
        zona_combobox = QComboBox(self)
        zona_combobox.addItems(cargar_lista_db('Zonas'))
        zona_combobox.setCurrentIndex(-1)

        coche_label = QLabel('¿Tienes coche?', self)
        coche_combobox = QComboBox(self)
        coche_combobox.addItems(['', 'Sí', 'No'])
        coche_combobox.setCurrentIndex(-1)

        plazas_label = QLabel('Plazas:', self)
        plazas_input = QLineEdit(self)
        plazas_input.setEnabled(False)

        add_button = QPushButton('Añadir/Modificar', self)
        search_button = QPushButton('Buscar', self)

        # Establecer el color de los botones
        add_button.setStyleSheet('background-color: #006600; color: white')
        search_button.setStyleSheet('background-color: #006600; color: white')

        vbox = QVBoxLayout()
        vbox.addWidget(horario_label)
        vbox.addWidget(horario_combobox)
        vbox.addWidget(turno_label)
        vbox.addWidget(turno_combobox)
        vbox.addWidget(zona_label)
        vbox.addWidget(zona_combobox)
        vbox.addWidget(coche_label)
        vbox.addWidget(coche_combobox)
        vbox.addWidget(plazas_label)
        vbox.addWidget(plazas_input)

        hbox = QHBoxLayout()
        hbox.addWidget(add_button)
        hbox.addWidget(search_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        coche_combobox.currentTextChanged.connect(lambda text: plazas_input.setEnabled(text == 'Sí'))

        add_button.clicked.connect(lambda: self.add_or_modify({
            'horario': horario_combobox.currentText(),
            'turno': turno_combobox.currentText(),
            'zona': zona_combobox.currentText(),
            'coche': coche_combobox.currentText(),
            'plazas': plazas_input.text() if coche_combobox.currentText() == 'Sí' else None
        }))
        search_button.clicked.connect(lambda: self.search({
            'horario': horario_combobox.currentText(),
            'turno': turno_combobox.currentText(),
            'zona': zona_combobox.currentText(),
            'coche': coche_combobox.currentText(),
            'plazas': plazas_input.text() if coche_combobox.currentText() == 'Sí' else None
        }))

        self.show()

    def add_or_modify(self, data):
        if all(data.values()):
            # Lógica para añadir o modificar el registro con los datos
            QMessageBox.information(self, 'Información', 'Registro añadido/modificado correctamente')
        else:
            QMessageBox.warning(self, 'Advertencia', 'Faltan campos por cumplimentar')

    def search(self, data):
        if all(data.values()):
            # Lógica para buscar coincidencias
            QMessageBox.information(self, 'Información', 'Búsqueda realizada correctamente')
        else:
            QMessageBox.warning(self, 'Advertencia', 'Faltan campos por cumplimentar')

if __name__ == '__main__':
    app = QApplication([])
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        user, password = login_dialog.get_user_password()
        if user == 'usuario' and password == 'contraseña':
            ex = App()
            app.exec_()
        else:
            QMessageBox.warning(None, 'Advertencia', 'Usuario o contraseña incorrectos')
    else:
        app.quit()