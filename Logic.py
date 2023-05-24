from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import os
import sys

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

        if not createConnection():
            sys.exit(1)

        self.tableModel = QSqlTableModel(self)
        self.columnModel=QStandardItemModel()

        self.tableModel.setTable("Seances")
        self.tableModel.select()

        self.selectData()

        self.columnView.setModel(self.columnModel)


    #Fonction qui récupère les données correspondantes aux séances
    def selectData(self):
        self.lstSeance = []
        self.nomExo = []
        self.lstExo=[]
        #self.
        for i in range(self.tableModel.rowCount()) :

            self.data = self.tableModel.record(i)


            self.lstSeance.append(QStandardItem(self.data.value("Nom")))
            self.exo=self.data.value("Liste_exo")

            self.nomExo=self.exo.split(",")

            for j in self.nomExo :
                self.lstExo.append(QStandardItem(j))
                self.lstSeance[i].appendRow(self.lstExo[-1])

            self.columnModel.appendRow(self.lstSeance[i])


            print(type(self.data.value("Liste_exo")))

    def triExo(self,nomExercice):
        pass


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


        #Ajout Limite Movement max positive + negative + valeur que le medecin peut appliquer
        #Ajout de cycle + durée cycle en fct de durée

        #Chargement des données
        self.model.select()
        #On applique le modèle à notre tableau
        self.tableView.setModel(self.model)
        self.rowToDelete=None
        self.tableView.resizeColumnsToContents()#Sert à redimensionner les colonnes
        self.tableView.pressed.connect(self.selectDel)
        self.buttEnrModif.clicked.connect(self.model.submitAll)#Enregistre les modifs
        self.buttAnnul.clicked.connect(self.model.revertAll)#Annule les modifs
        self.buttAjtExo.clicked.connect(self.model.insertRow)
        self.buttDelExo.clicked.connect(self.delWarning)


#Selectionne la ligne à supprimer
    def selectDel(self,index):
        self.ind=index
        self.rowToDelete=self.ind.row()

#Fonction qui supprimme la ligne
    def delRowOnClick(self):
        if self.rowToDelete is not None :
            self.model.removeRow(self.rowToDelete)
            self.model.submitAll()
            self.rowToDelete=None

    #Message de confirmation de suppression
    def delWarning(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Confirmer la suppression")
        self.msg.setText("Voulez vous vraiment supprimer cette Exercice ?")
        self.msg.setStandardButtons(QMessageBox.Yes| QMessageBox.Cancel)
        self.do =self.msg.exec_()
        if self.do == QMessageBox.Yes :
            self.delRowOnClick()


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