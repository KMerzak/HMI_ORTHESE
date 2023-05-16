from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import os
acc,_ = loadUiType(os.path.join('mainwindow.ui'))
sea,_ = loadUiType(os.path.join('seance.ui'))
exo,_ = loadUiType(os.path.join('Exercices.ui'))

class Acc(QMainWindow,acc):
    def __init__(self,parent=None):
        super(Acc, self).__init__(parent)
        self.setupUi(self)
        self.sea=None
        self.exo=None
        self.buttSeance.clicked.connect(self.seanceOnClicked)
        self.buttExercice.clicked.connect(self.exerciceOnClicked)

    #@Slot
    def seanceOnClicked(self):
        if self.sea== None:
            self.sea=Seance()
            self.sea.show()
        else :
            self.sea=None
    #@Slot
    def exerciceOnClicked(self):
        if self.exo== None:
            self.exo=Exercice()
            self.exo.show()
        else :
            self.exo=None

#Code qui définit la fenêtre des séances
class Seance(QWidget,sea):
    def __init__(self,parent=None):
        super(Seance, self).__init__(parent)
        self.setupUi(self)



#Classe qui définit la fenêtre des Exercices
class Exercice(QWidget,exo):
    def __init__(self,parent=None):
        super(Exercice, self).__init__(parent)
        self.setupUi(self)


        #On vérifie la connection avec la base de donnée locale
        if not createConnection():
            sys.exit(1)

        #On définit notre model pour le tableau
        self.model = QSqlTableModel(self)
        self.model.setTable("Exercices")
        #Méthode d'actualisation des données
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        #Définition des noms des colonnes
        self.model.setHeaderData(0, Qt.Horizontal, "Nom")
        self.model.setHeaderData(1, Qt.Horizontal, "Durée")
        self.model.setHeaderData(2, Qt.Horizontal, "Raideur Alpha")
        self.model.setHeaderData(3, Qt.Horizontal, "Raideur Beta")
        self.model.setHeaderData(4, Qt.Horizontal, "Raideur Gamma")
        self.model.setHeaderData(5, Qt.Horizontal, "Vitesse Alpha")
        self.model.setHeaderData(6, Qt.Horizontal, "Vitesse Beta")
        self.model.setHeaderData(7, Qt.Horizontal, "Vitesse Gamma")

        #Chargement des données
        self.model.select()
        #On applique le modèle à notre tableau
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()#Sert à redimensionner les colonnes

        self.buttEnrModif.clicked.connect(self.model.submitAll)


#Fonction qui crée la connection à notre base de données
def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName(r"C:\Users\Merzak\Desktop\HMI_ORTHESE\Orthe.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "Erreur de Connexion !",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True