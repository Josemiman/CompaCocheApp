import AccionesDB
from AccionesDB import modificar_dato_db
from AccionesDB import cargar_lista_db
from AccionesDB import agregar_elemento_array

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
        self.title = 'CompaCocheOPPLUS'
        self.left = 30
        self.top = 30
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
        vbox.addWidget(parking_label)
        vbox.addWidget(parking_combobox)

        hbox = QHBoxLayout()
        hbox.addWidget(add_button)
        hbox.addWidget(search_button)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        #coche_combobox.currentTextChanged.connect(lambda text: plazas_input.setEnabled(text == 'Sí'))
        # Conectar la señal currentTextChanged de coche_combobox
        coche_combobox.currentTextChanged.connect(
            lambda text: self.update_elements(text, plazas_input, parking_combobox))



        add_button.clicked.connect(lambda: self.add_or_modify({
            'horario': horario_combobox.currentText(),
            'turno': turno_combobox.currentText(),
            'zona': zona_combobox.currentText(),
            'coche': coche_combobox.currentText(),
            'plazas': plazas_input.text() if coche_combobox.currentText() == 'Sí' else None,
            'parking': parking_combobox.currentText() if coche_combobox.currentText() == 'Sí' else None
        }))
        search_button.clicked.connect(lambda: self.search({
            'horario': horario_combobox.currentText(),
            'turno': turno_combobox.currentText(),
            'zona': zona_combobox.currentText(),
            'coche': coche_combobox.currentText(),
            'plazas': plazas_input.text() if coche_combobox.currentText() == 'Sí' else None,
            'parking': parking_combobox.currentText() if coche_combobox.currentText() == 'Sí' else None
        }))

        self.show()

    def update_elements(self, text, plazas_input, parking_combobox):
        enabled = text == 'Sí'
        plazas_input.setEnabled(enabled)
        parking_combobox.setEnabled(enabled)

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