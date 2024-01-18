from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
from xml.dom import minidom
import pyperclip
path=""
def select_click():
    global code,path
    btnstxt = ""
    mytxt = ""
    path = browse_file()
    if path:
        try:
            file = minidom.parse(path)
            widgets = file.getElementsByTagName('widget')
            for w in widgets:
                if w.attributes['class'].value == "QPushButton":  # Bouton
                    btnstxt += f"windows.{w.attributes['name'].value}.clicked.connect({w.attributes['name'].value}_click)\n"
                    mytxt += f"def {w.attributes['name'].value}_click():\n    pass\n"
                elif w.attributes['class'].value in ["QLineEdit", "QLabel"]:  # Zone de texte ou Libellé
                    # btnstxt = btnstxt + "windows."+w.attributes['name'].value +".clicked.connect ( "+  w.attributes['name'].value +"_click )"+chr(13)+chr(10)
                    pass  # Adjust this part as needed

            code = f'''from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication

{mytxt}

app = QApplication([])
windows = loadUi("{path}")
windows.show()
{btnstxt}
app.exec_()'''
            windows.fichier.setText(path)
        except:
            QMessageBox.critical(windows, "Erreur", "le fichier est vide ou endommagé")
def copier_click():
    try:
        pyperclip.copy(code)
        QMessageBox.information(windows, "Information", "Code copié avec succès")
    except:
        QMessageBox.critical(windows, "Erreur", "Sélectionnez d'abord un fichier")
def creer_click():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    if path=="":
        QMessageBox.critical(windows, "Erreur", "Sélectionnez d'abord un fichier")
    else:
        try:
            file_name, _ = QFileDialog.getSaveFileName(windows, "Sauvegarder", path[:len(path)-3]+".py", "Python Files (*.py);;All Files (*)", options=options)
            if file_name:
                QMessageBox.information(windows, "Information", "fichier Sauvegardé avec succès")
        except:
            QMessageBox.critical(windows, "Erreur", "l'enregistrement du fichier a échoué")
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(code)
            except:
                QMessageBox.critical(windows, "Erreur", "l'écriture du code dans le fichier a échoué")
def browse_file():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(windows, "Open .ui File", "", "UI Files (*.ui);;All Files (*)", options=options)
        return(file_name)

app = QApplication([])
windows = loadUi("main.ui")
windows.show()
windows.select.clicked.connect(select_click)
windows.copier.clicked.connect(copier_click)
windows.creer.clicked.connect(creer_click)
windows.setWindowTitle("qtDesign to Python")
app.exec_()