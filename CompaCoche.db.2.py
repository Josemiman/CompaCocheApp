import AccionesDB
from AccionesDB import modificar_dato_db
from AccionesDB import cargar_lista_db
from AccionesDB import agregar_elemento_array
from AccionesDB import agregar_datos_db
from AccionesDB import verificar_usuario_db
from AccionesDB import verificar_nuevo_usuario

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog


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

        self.accept_button = QPushButton('Iniciar Sesión', self)
        self.alta_button = QPushButton('Alta usuario', self)
        self.cancel_button = QPushButton('Cancelar', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.user_label)
        vbox.addWidget(self.user_input)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.accept_button)
        hbox.addWidget(self.alta_button)
        hbox.addWidget(self.cancel_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.accept_button.clicked.connect(self.accept)
        self.alta_button.clicked.connect(self.show_alta_usuario_dialog)
        self.cancel_button.clicked.connect(self.reject)

    def get_user_password(self):
        user = self.user_input.text()
        password = self.password_input.text()

        # Verificar si el usuario y la contraseña corresponden a un usuario existente
        if verificar_usuario_db(user, password):
            return user, password
        # Verificar si el usuario y la contraseña corresponden a un nuevo usuario
        elif verificar_nuevo_usuario(user, password):
            agregar_usuario_db(user, password)
            return user, password
        # Si no se encuentra el usuario o la contraseña, devolver None
        else:
            QMessageBox.warning(self, 'Advertencia', 'Usuario o contraseña erróneo')
            return None, None

    def show_alta_usuario_dialog(self):
        dialog = AltaUsuarioDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            user, password, nick, mail, tlfn = dialog.get_data()
            if user and password and nick and mail and  tlfn:
                agregar_datos_db('CompaCoche', 'Usuarios', {user:[password, '', '', '', '', '', '', nick, mail, tlfn]})
                self.user_input.setText(user)
                self.password_input.setText(password)
            else:
                QMessageBox.warning(self, 'Advertencia', 'Faltan campos por cumplimentar')

class AltaUsuarioDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Alta de usuario')
        self.setGeometry(100, 100, 900, 700)

        self.user_label = QLabel('Usuario:', self)
        self.user_input = QLineEdit(self)

        self.password_label = QLabel('Contraseña:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.nick_label = QLabel('Nick:', self)
        self.nick_input = QLineEdit(self)

        self.mail_label = QLabel('E-Mail:', self)
        self.mail_input = QLineEdit(self)

        self.tlfn_label = QLabel('Teléfono:', self)
        self.tlfn_input = QLineEdit(self)

        self.accept_button = QPushButton('Aceptar', self)
        self.cancel_button = QPushButton('Cancelar', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.user_label)
        vbox.addWidget(self.user_input)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_input)
        vbox.addWidget(self.nick_label)
        vbox.addWidget(self.nick_input)
        vbox.addWidget(self.mail_label)
        vbox.addWidget(self.mail_input)
        vbox.addWidget(self.tlfn_label)
        vbox.addWidget(self.tlfn_input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.accept_button)
        hbox.addWidget(self.cancel_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        user = self.user_input.text()
        password = self.password_input.text()
        nick = self.nick_input.text()
        mail = self.mail_input.text()
        tlfn = self.tlfn_input.text()
        return user, password, nick, mail, tlfn

class App(QWidget):

    def __init__(self, user):
        super().__init__()
        self.title = 'CompaCocheOPPLUS'
        self.left = 30
        self.top = 30
        self.width = 640
        self.height = 480


        self.user = user

        # Recuperar los datos del usuario de la base de datos
        datos_usuario = cargar_lista_db('Usuarios', self.user)

        self.initUI(datos_usuario)

    def initUI(self, datos_usuario):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #datos_usuario[3]
        # Establecer el color de fondo
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(200, 255, 200))
        self.setPalette(palette)

        horario_label = QLabel('Horario:', self)
        horario_combobox = QComboBox(self)
        horario_combobox.addItems(cargar_lista_db('FormData','Horario'))
        horario_combobox.setCurrentIndex(-1)

        turno_label = QLabel('Turno:', self)
        turno_combobox = QComboBox(self)
        turno_combobox.addItems(cargar_lista_db('FormData','Turnos'))
        turno_combobox.setCurrentIndex(-1)

        zona_label = QLabel('Zona:', self)
        zona_combobox = QComboBox(self)
        zona_combobox.addItems(cargar_lista_db('FormData','Zonas'))
        zona_combobox.setCurrentIndex(-1)

        coche_label = QLabel('¿Tienes coche?', self)
        coche_combobox = QComboBox(self)
        coche_combobox.addItems(['', 'Sí', 'No'])
        coche_combobox.setCurrentIndex(-1)

        plazas_label = QLabel('Plazas:', self)
        plazas_input = QLineEdit(self)
        plazas_input.setEnabled(False)

        parking_label = QLabel('Parking:', self)
        parking_combobox = QComboBox(self)
        parking_combobox.addItems(cargar_lista_db('FormData', 'Parking'))
        parking_combobox.setCurrentIndex(-1)
        parking_combobox.setEnabled(False)

        if datos_usuario:
            horario_combobox.setCurrentText(datos_usuario[1])
            turno_combobox.setCurrentText(datos_usuario[2])
            zona_combobox.setCurrentText(datos_usuario[3])
            coche_combobox.setCurrentText(datos_usuario[4])
            plazas_input.setText(datos_usuario[5])
            parking_combobox.setCurrentText(datos_usuario[6])
            if coche_combobox.currentText() == 'Sí':
                plazas_input.setEnabled(True)
            else:
                plazas_input.setEnabled(False)

        add_button = QPushButton('Actualizar datos', self)
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
        vbox.addWidget(parking_label)
        vbox.addWidget(parking_combobox)

        hbox = QHBoxLayout()
        hbox.addWidget(add_button)
        hbox.addWidget(search_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Conectar la señal currentTextChanged de coche_combobox
        coche_combobox.currentTextChanged.connect(
            lambda text: self.update_elements(text, plazas_input, parking_combobox))



        add_button.clicked.connect(lambda: self.add_or_modify({
            'usuario': user,
            'horario': horario_combobox.currentText(),
            'turno': turno_combobox.currentText(),
            'zona': zona_combobox.currentText(),
            'coche': coche_combobox.currentText(),
            'plazas': plazas_input.text() if coche_combobox.currentText() == 'Sí' else '0',
            'parking': parking_combobox.currentText() if coche_combobox.currentText() == 'Sí' else 'Ninguno'
        }))
        search_button.clicked.connect(lambda: self.search({
            'horario': horario_combobox.currentText(),
            'turno': turno_combobox.currentText(),
            'zona': zona_combobox.currentText(),
            'coche': coche_combobox.currentText(),
            'plazas': plazas_input.text() if coche_combobox.currentText() == 'Sí' else '0',
            'parking': parking_combobox.currentText() if coche_combobox.currentText() == 'Sí' else 'Ninguno'
        }))

        self.show()

    def update_elements(self, text, plazas_input, parking_combobox):
        try:
            datos_usuario = cargar_lista_db('Usuarios', self.user)
        except:
        	datos_usuario = ['', '', '', '', '', '0', 'Ninguno']
        enabled = text == 'Sí'
        plazas_input.setEnabled(enabled)
        parking_combobox.setEnabled(enabled)
        if enabled == False:
            plazas_input.setText('')
            parking_combobox.setCurrentIndex(-1)
        else:
        	plazas_input.setText(datos_usuario[5])
        	parking_combobox.setCurrentText(datos_usuario[6])
        	
    def add_or_modify(self, data):
        if all(data.values()):
            # Lógica para añadir o modificar el registro con los datos
            data_old = cargar_lista_db('Usuarios', user)
            modificar_dato_db(
                'Usuarios', data['usuario'], [
                    data_old[0],
                    data['horario'],
                    data['turno'],
                    data['zona'],
                    data['coche'],
                    data['plazas'],
                    data['parking'],
                    data_old[7],
                    data_old[8],
                    data_old[9]
                ]
            )

            QMessageBox.information(self, 'Información', 'Actualización realizada')
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
        if verificar_usuario_db(user, password):
            ex = App(user)
            ex.show()
            app.exec_()
        else:
            QMessageBox.warning(None, 'Advertencia', 'Usuario o contraseña incorrectos')
    else:
        app.quit()
