# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Primeira_tela.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1287, 912)
        MainWindow.setMinimumSize(QtCore.QSize(1287, 912))
        MainWindow.setMaximumSize(QtCore.QSize(1287, 912))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabela = QtWidgets.QTableView(self.centralwidget)
        self.tabela.setGeometry(QtCore.QRect(10, 150, 951, 701))
        self.tabela.setObjectName("tabela")
        self.pesquisar = QtWidgets.QPushButton(self.centralwidget)
        self.pesquisar.setGeometry(QtCore.QRect(20, 100, 75, 23))
        self.pesquisar.setObjectName("pesquisar")
        self.coluna = QtWidgets.QLineEdit(self.centralwidget)
        self.coluna.setGeometry(QtCore.QRect(80, 30, 113, 20))
        self.coluna.setObjectName("coluna")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(20, 20, 61, 41))
        self.label.setObjectName("label")
        self.condicao = QtWidgets.QLineEdit(self.centralwidget)
        self.condicao.setGeometry(QtCore.QRect(160, 70, 231, 20))
        self.condicao.setObjectName("condicao")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 30, 47, 21))
        self.label_2.setObjectName("label_2")
        self.nomeTabela = QtWidgets.QLineEdit(self.centralwidget)
        self.nomeTabela.setGeometry(QtCore.QRect(270, 30, 113, 20))
        self.nomeTabela.setObjectName("nomeTabela")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(120, 60, 41, 41))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1040, 10, 71, 41))
        self.label_5.setObjectName("label_5")
        self.desc = QtWidgets.QRadioButton(self.centralwidget)
        self.desc.setGeometry(QtCore.QRect(20, 60, 82, 17))
        self.desc.setObjectName("desc")
        self.ordenador = QtWidgets.QComboBox(self.centralwidget)
        self.ordenador.setGeometry(QtCore.QRect(1120, 20, 151, 22))
        self.ordenador.setObjectName("ordenador")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.ordenador.addItem("")
        self.exportar = QtWidgets.QPushButton(self.centralwidget)
        self.exportar.setGeometry(QtCore.QRect(1040, 100, 75, 23))
        self.exportar.setObjectName("exportar")
        self.tipoEx = QtWidgets.QComboBox(self.centralwidget)
        self.tipoEx.setGeometry(QtCore.QRect(1120, 101, 151, 21))
        self.tipoEx.setObjectName("tipoEx")
        self.tipoEx.addItem("")
        self.tipoEx.addItem("")
        self.tipoEx.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1100, 70, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.deletar = QtWidgets.QPushButton(self.centralwidget)
        self.deletar.setGeometry(QtCore.QRect(120, 100, 91, 23))
        self.deletar.setObjectName("deletar")
        self.validacaodatas = QtWidgets.QTableView(self.centralwidget)
        self.validacaodatas.setGeometry(QtCore.QRect(960, 150, 291, 701))
        self.validacaodatas.setObjectName("validacaodatas")
        self.quantidade = QtWidgets.QLineEdit(self.centralwidget)
        self.quantidade.setGeometry(QtCore.QRect(540, 30, 113, 20))
        self.quantidade.setObjectName("quantidade")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(390, 30, 151, 16))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1287, 21))
        self.menubar.setObjectName("menubar")
        self.menuOp_es = QtWidgets.QMenu(self.menubar)
        self.menuOp_es.setObjectName("menuOp_es")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actioncadastrar = QtWidgets.QAction(MainWindow)
        self.actioncadastrar.setObjectName("actioncadastrar")
        self.actionimportar = QtWidgets.QAction(MainWindow)
        self.actionimportar.setObjectName("actionimportar")
        self.actionLer_pdfs = QtWidgets.QAction(MainWindow)
        self.actionLer_pdfs.setObjectName("actionLer_pdfs")
        self.actionImportar_arquivo_csv = QtWidgets.QAction(MainWindow)
        self.actionImportar_arquivo_csv.setObjectName("actionImportar_arquivo_csv")
        self.actionSalvar_dados = QtWidgets.QAction(MainWindow)
        self.actionSalvar_dados.setObjectName("actionSalvar_dados")
        self.actionImportar_dados_para_vizualizar = QtWidgets.QAction(MainWindow)
        self.actionImportar_dados_para_vizualizar.setObjectName("actionImportar_dados_para_vizualizar")
        self.actionDeletar_dados_pesquisados = QtWidgets.QAction(MainWindow)
        self.actionDeletar_dados_pesquisados.setObjectName("actionDeletar_dados_pesquisados")
        self.actionAtualizar_status = QtWidgets.QAction(MainWindow)
        self.actionAtualizar_status.setObjectName("actionAtualizar_status")
        self.menuOp_es.addAction(self.actionimportar)
        self.menuOp_es.addAction(self.actionImportar_arquivo_csv)
        self.menuOp_es.addAction(self.actionLer_pdfs)
        self.menuOp_es.addAction(self.actionSalvar_dados)
        self.menuOp_es.addAction(self.actionImportar_dados_para_vizualizar)
        self.menuOp_es.addAction(self.actionAtualizar_status)
        self.menubar.addAction(self.menuOp_es.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Buscar Dados"))
        self.pesquisar.setText(_translate("MainWindow", "Pesquisar"))
        self.label.setText(_translate("MainWindow", "MOSTRAR "))
        self.label_2.setText(_translate("MainWindow", "Da tabela"))
        self.label_4.setText(_translate("MainWindow", "Onde "))
        self.label_5.setText(_translate("MainWindow", "Ordenado por"))
        self.desc.setText(_translate("MainWindow", "Descrecente"))
        self.ordenador.setItemText(0, _translate("MainWindow", "ID"))
        self.ordenador.setItemText(1, _translate("MainWindow", "CÓDIGO"))
        self.ordenador.setItemText(2, _translate("MainWindow", "EQUIPAMENTO"))
        self.ordenador.setItemText(3, _translate("MainWindow", "RESOLUÇÃO"))
        self.ordenador.setItemText(4, _translate("MainWindow", "CAPACIDADE"))
        self.ordenador.setItemText(5, _translate("MainWindow", "FABRICANTE"))
        self.ordenador.setItemText(6, _translate("MainWindow", "LOCAL"))
        self.ordenador.setItemText(7, _translate("MainWindow", "OPERADOR"))
        self.ordenador.setItemText(8, _translate("MainWindow", "CRITÉRIO DE ACEITAÇÃO"))
        self.ordenador.setItemText(9, _translate("MainWindow", "UNIDADE DO CRITERIO DE ACEITAÇÃO"))
        self.ordenador.setItemText(10, _translate("MainWindow", "CERTIFICADO"))
        self.ordenador.setItemText(11, _translate("MainWindow", "NOMENCLATURA DO RESULTADO"))
        self.ordenador.setItemText(12, _translate("MainWindow", "ERRO"))
        self.ordenador.setItemText(13, _translate("MainWindow", "INCERTEZA DE MEDIÇÃO"))
        self.ordenador.setItemText(14, _translate("MainWindow", "RESULTADO"))
        self.ordenador.setItemText(15, _translate("MainWindow", "UNIDADE DO RESULTADO"))
        self.ordenador.setItemText(16, _translate("MainWindow", "DATA DA CALIBRAÇÃO"))
        self.ordenador.setItemText(17, _translate("MainWindow", "STATUS"))
        self.ordenador.setItemText(18, _translate("MainWindow", "PERIODICIDADE"))
        self.exportar.setText(_translate("MainWindow", "Exportar"))
        self.tipoEx.setItemText(0, _translate("MainWindow", "CSV"))
        self.tipoEx.setItemText(1, _translate("MainWindow", "Excel"))
        self.tipoEx.setItemText(2, _translate("MainWindow", "Json"))
        self.label_3.setText(_translate("MainWindow", "Exportar dados:"))
        self.deletar.setText(_translate("MainWindow", "Deletar pesquisa"))
        self.label_6.setText(_translate("MainWindow", "Quantidade de equipamentos:"))
        self.menuOp_es.setTitle(_translate("MainWindow", "Opções"))
        self.actioncadastrar.setText(_translate("MainWindow", "cadastrar dados"))
        self.actionimportar.setText(_translate("MainWindow", "Importar arquivo excel"))
        self.actionLer_pdfs.setText(_translate("MainWindow", "Ler pdfs"))
        self.actionImportar_arquivo_csv.setText(_translate("MainWindow", "Importar arquivo csv"))
        self.actionSalvar_dados.setText(_translate("MainWindow", "Salvar dados"))
        self.actionImportar_dados_para_vizualizar.setText(_translate("MainWindow", "Importar dados para vizualizar"))
        self.actionDeletar_dados_pesquisados.setText(_translate("MainWindow", "Deletar dados pesquisados"))
        self.actionAtualizar_status.setText(_translate("MainWindow", "Atualizar status"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
