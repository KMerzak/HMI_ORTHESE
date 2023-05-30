from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlRecord
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

        self.tableSeanceModel = QSqlTableModel(self)
        self.tableExerciceModel = QSqlTableModel(self)
        self.currentIndex= None

        self.columnModel=QStandardItemModel()

        self.tableSeanceModel.setTable("Seances")
        self.tableExerciceModel.setTable("Exercices")

        self.tableSeanceModel.select()

        self.selectData()

        self.columnView.setModel(self.columnModel)

        self.columnView.setResizeGripsVisible(False)

        self.buttAjSeance.clicked.connect(self.AjSeance)

        self.buttAjExo.clicked.connect(self.AjExo)

        self.columnView.clicked.connect(self.sel)

        self.buttEnregSean.clicked.connect(self.ajSeanceBase)

    def AjSeance(self):
        self.columnModel.insertRow(self.columnModel.rowCount(),QStandardItem('New Seance'))

    def ajSeanceBase(self):
        self.tableSeanceModel.setFilter("")
        self.tableSeanceModel.select()
        if self.currentIndex is not None :
            for i in range(self.tableSeanceModel.rowCount()) :
                if self.columnModel.itemFromIndex(self.currentIndex).text() == self.tableSeanceModel.record(i).field(0).value() :
                    print(i)
                    print("égale")
                    return
            self.rec=self.tableSeanceModel.record()
            self.rec.setValue(0,"{}".format(self.columnModel.itemFromIndex(self.currentIndex).text()))
            self.tableSeanceModel.insertRecord(-1,self.rec)
            self.tableSeanceModel.submitAll()


    def AjExo(self):
        self.exo1 = Exercice()
        self.exo1.buttAjExoSea.show()
        self.exo1.show()
        self.exo1.buttAjExoSea.clicked.connect(self.selExo)

    def selExo(self):

        self.exoToAdd=self.exo1.model.record(self.exo1.rowSelected).field(0).value()
        self.tableSeanceModel.setFilter("Nom = '{}' ".format(self.columnModel.itemFromIndex(self.currentIndex).text()))
        self.tableSeanceModel.select()
        self.oldSeance=self.tableSeanceModel.record(0)
        self.newLstExo=self.tableSeanceModel.record(0).field(1).value() + ',' + self.exoToAdd
        self.tableSeanceModel.setData(self.tableSeanceModel.index(0,1),self.newLstExo)
        self.tableSeanceModel.submitAll()
        self.columnModel.clear()
        self.selectData()
        self.exo1.close()






    #Fonction qui récupère les données correspondantes aux séances
    def selectData(self):
        self.lstSeance = []
        self.nomExo = []
        self.lstExo=[]
        self.attributeExo = []

        self.dataExo=[]

        self.tableSeanceModel.setFilter("")
        self.tableSeanceModel.select()

        self.defs = [QStandardItem("Nom"), QStandardItem("Durée"), QStandardItem("Raideur Alpha"),
                     QStandardItem("Raideur Beta"), QStandardItem("Raideur Gamma"), QStandardItem("Vitesse Alpha"),
                     QStandardItem("Vitesse Beta"), QStandardItem("Vitesse Gamma")]


        for i in range(self.tableSeanceModel.rowCount()) :
            #On récupère les données de la table Seances
            self.data = self.tableSeanceModel.record(i)


            self.lstSeance.append(QStandardItem(self.data.value("Nom")))

            #On récupère la liste des exercices
            self.exo=self.data.value("Liste_exo")
            self.nomExo=self.exo.split(",")

            #On ajoute à chaque séance ses exercices
            for j in self.nomExo :
                if j != "" :
                    self.lstExo.append(QStandardItem(j))
                    self.lstSeance[i].appendRow(self.lstExo[-1])

            #On ajoute notre séance à la liste des séances
            self.columnModel.appendRow(self.lstSeance[i])



        self.triExo()




    def sel(self,index):
        self.currentIndex=index
        self.parentIndex=index.parent()
        self.ExoParent=self.columnModel.itemFromIndex(self.parentIndex)





    #Fonction qui attribue chaque valeurs à son exercice correspondant
    def triExo(self):

        for i in range(len(self.lstExo)) :
            #On réinitialise notre liste dattributs pour chaque exercice (pour pas avoir de chevauchement)
            self.attributeExo.clear()

            #On séléctionne uniquement les exercices de la table Exercice qui sont dans la séance
            self.tableExerciceModel.setFilter("Nom = '{}' ".format(self.lstExo[i].text()))
            self.tableExerciceModel.select()

            #On itère pour chaque attributs
            for j in range(len(self.defs)) :
                 self.attributeExo.append(QStandardItem(self.defs[j]))
                 self.lstExo[i].appendRow(self.attributeExo[-1])
                 self.attributeExo[j].appendRow(QStandardItem(str(self.tableExerciceModel.record(0).field(j).value())))



#Classe qui définit la fenêtre des Exercices
class Exercice(QWidget,exo):
    def __init__(self,parent=None):
        super(Exercice, self).__init__(parent)
        self.setupUi(self)
        self.buttAjExoSea.hide()

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

        self.buttRetour.clicked.connect(self.close)






#Selectionne la ligne à supprimer
    def selectDel(self,index):
        self.ind=index
        self.rowToDelete=self.ind.row()
        self.rowSelected=self.ind.row()

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
    path=os.path.dirname(os.path.realpath(__file__))+"\\Orthe.db"

    con.setDatabaseName(path)
    if not con.open():
        QMessageBox.critical(
            None,
            "Erreur de Connexion !",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True