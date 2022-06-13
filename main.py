import os
from sys import argv, exit
from datetime import datetime
from re import I, compile
from numpy import NaN
import Modelo_pandas_PyQT5
import pandas as pd
from threading import Thread
from SalvarDados import *
from LerPDFSReserva import *
import tela
from CRUD import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from pyautogui import alert


class buscaDados(QMainWindow, tela.Ui_MainWindow, Thread):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        Thread.__init__(self)
        self.df = pd.DataFrame()
        self.pesquisar.clicked.connect(self.buttom_search)
        self.exportar.clicked.connect(self.exportarParaDesktop)
        self.actionimportar.triggered.connect(self.importarDados)
        self.actionImportar_arquivo_csv.triggered.connect(self.importarDadosCSV)
        self.actionSalvar_dados.triggered.connect(self.salvarBD)
        self.actionImportar_dados_para_vizualizar.triggered.connect(self.vizualizar)
        self.deletar.clicked.connect(self.deletarDados)
        self.actionAtualizar_status.triggered.connect(self.atualizar)
        self.regex_auxiliar = compile(r"^\d+$", I)
        self.regex_tira_litra = compile(r"\d+\.?\d+", I)
        self.actionLer_pdfs.triggered.connect(self.leraPDFarquivo)

    def leraPDFarquivo(self):
        leitor = LerPDFS(os.listdir(os.path.join('pdfs')))
        leitor.start()
        QMessageBox.about(self, "Alert", "Os pdfs estão sendo lidos, por favor aguarde")

    def formatar(self, x):
        if "º" not in x:
            x = x.replace(",", ".")
            return x
        else:
            if not self.regex_auxiliar.findall(x):
                x = x.replace("º", ".")
                x = x.replace("'", "")
                x = x.split(".")
                return float(float(x[0]) + (float(x[1]) / 60))
            else:
                return x

    def tirarletras(self, valor):
        valorretorno = self.regex_tira_litra.findall(valor)
        if valorretorno:
            return float(valorretorno[0])
        else:
            return valor

    def atualizar(self):
        QMessageBox.about(self, "Alert", "Dados serão atualizados")
        bd = sqliteConnector('BDequipamentos')
        resultado = bd.read(colunas='*')
        resultado.start()
        resultado.join(1000)
        colunas_bd = ["ID", 'CÓDIGO', 'EQUIPAMENTO', 'RESOLUÇÃO', 'CAPACIDADE', 'FABRICANTE',
                      'LOCAL', 'OPERADOR', 'CRITÉRIO DE ACEITAÇÃO',
                      'UNIDADE DO CRITERIO DE ACEITAÇÃO', 'CERTIFICADO',
                      'NOMENCLATURA DO RESULTADO', 'ERRO', 'INCERTEZA DE MEDIÇÃO',
                      'RESULTADO', 'UNIDADE DO RESULTADO', 'DATA DA CALIBRAÇÃO', 'STATUS',
                      'PERIODICIDADE']
        df = pd.DataFrame(columns=colunas_bd, data=sqliteConnector.retorno)

        criterio_avaliacao = pd.Series(df.loc[:, 'CRITÉRIO DE ACEITAÇÃO'])
        criterio_avaliacao = criterio_avaliacao.apply(lambda x: self.formatar(str(x)))
        criterio_avaliacao.index = [i for i in range(len(criterio_avaliacao))]
        criterio_avaliacao = criterio_avaliacao.apply(lambda x: self.tirarletras(x))
        criterio_avaliacao = criterio_avaliacao.astype('float64')

        erro = df.loc[:, 'ERRO']
        erro = erro.apply(lambda x: self.formatar(str(x)))
        erro.index = [i for i in range(len(erro))]
        erro = erro.astype('float64')

        incerteza = df.loc[:, 'INCERTEZA DE MEDIÇÃO']
        incerteza = incerteza.apply(lambda x: self.formatar(str(x)))
        incerteza.index = [i for i in range(len(incerteza))]
        incerteza = incerteza.astype('float64')

        resultado = pd.Series(erro + incerteza)
        resultado.index = [i for i in range(len(resultado))]

        try:
            validar = pd.Series(resultado <= criterio_avaliacao).to_list()
            lista_status = []
            for i in validar:
                if i:
                    lista_status.append('OK')
                else:
                    lista_status.append("NOK")
            df.loc[:, 'ERRO'] = erro
            df.loc[:, 'INCERTEZA DE MEDIÇÃO'] = incerteza
            df.loc[:, 'RESULTADO'] = resultado
            df.loc[:, 'STATUS'] = pd.Series(lista_status)

            t = threading.Thread(target=alterar(df, self))
            t.start()
            sqliteConnector.retorno = None
        except Exception as e:
            return e

    def deletarDados(self):
        t = Thread(target=delete(self.df['ID'], self))
        t.start()
        self.quantidade.setText('0')
        model = Modelo_pandas_PyQT5.PandasModel(pd.DataFrame())
        self.tabela.setModel(model)
        self.validacaodatas.setModel(model)

    def vizualizar(self):
        arquivo = QFileDialog.getOpenFileName()[0]
        self.df = pd.DataFrame(pd.read_excel(arquivo))
        model = Modelo_pandas_PyQT5.PandasModel(self.df)
        self.tabela.setModel(model)

    def salvarBD(self):
        try:
            arquivo = QFileDialog.getOpenFileName()[0]
            self.df = pd.DataFrame(pd.read_excel(arquivo))
            if 'PERIODICIDADE' not in self.df.columns:
                QMessageBox.about(self, "Alert", 'A coluna de periodicidade não foi feita, por favor faça a e importe '
                                                 'novamente')
                return
            if 'Unnamed: 0' in self.df.columns:
                self.df.drop('Unnamed: 0', axis=1, inplace=True)
            t = Thread(target=alterar(self.df, self))
            t.start()
        except Exception as e:
            return

    def importarDados(self):
        arquivo = QFileDialog.getOpenFileName()[0]
        if not arquivo:
            return
        try:
            try:
                self.df = pd.DataFrame(pd.read_excel(arquivo))
            except Exception as e:
                try:
                    self.df = pd.DataFrame(pd.read_json(arquivo))
                except Exception as e:
                    try:
                        self.df = pd.DataFrame(pd.read_csv(arquivo))
                    except Exception as e:
                        QMessageBox.about(self, 'Alert', "Erro na leitura do arquivo, não foi possível ler esse formato")
                        return
            if 'PERIODICIDADE' not in self.df.columns:
                QMessageBox.about(self, "Alert", 'A coluna de periodicidade não foi feita, por favor faça a e importe '
                                                 'novamente')
                return
            self.df['DATA DA CALIBRAÇÃO'] = pd.to_datetime(self.df['DATA DA CALIBRAÇÃO'], errors='coerce')
            if 'Unnamed: 0' in self.df.columns:
                self.df.drop('Unnamed: 0', axis=1, inplace=True)
            if 'ID' in self.df.columns:
                self.df.drop('ID', axis=1, inplace=True)
        except Exception as e:
            QMessageBox.about(self, 'Alert', f"Falha, eror: {e}")
            return
        t = Thread(target=salvar(self.df, self))
        t.start()

    def importarDadosCSV(self):
        arquivo = QFileDialog.getOpenFileName()[0]
        if not arquivo:
            return
        try:
            try:
                self.df = pd.DataFrame(pd.read_excel(arquivo))
            except Exception as e:
                try:
                    self.df = pd.DataFrame(pd.read_json(arquivo))
                except Exception as e:
                    try:
                        self.df = pd.DataFrame(pd.read_csv(arquivo))
                    except Exception as e:
                        QMessageBox.about(self, 'Alert', "Erro na leitura do arquivo, não foi possível ler esse formato")
                        return
            self.df = pd.DataFrame(pd.read_csv(arquivo))
            if 'PERIODICIDADE' not in self.df.columns:
                QMessageBox.about(self, "Alert", 'A coluna de periodicidade não foi feita, por favor faça a e importe '
                                                 'novamente')
                return
            self.df['DATA DA CALIBRAÇÃO'] = pd.to_datetime(self.df['DATA DA CALIBRAÇÃO'], errors='coerce')
            if 'Unnamed: 0' in self.df.columns:
                self.df.drop('Unnamed: 0', axis=1, inplace=True)
            if 'ID' in self.df.columns:
                self.df.drop('ID', axis=1, inplace=True)
        except Exception as e:
            QMessageBox.about(self, 'Alert', f"Falha, eror: {e}")
            return
        t = Thread(target=salvar(self.df, self))
        t.start()

    def exportarParaDesktop(self):
        try:
            if self.df.empty:
                QMessageBox.about(self, "Alert", 'É necessário fazer uma pesquisa primeiro, para salva-lá')
                return
            try:
                tipo = self.tipoEx.currentText()
                if 'csv' in tipo.lower():
                    self.df.to_csv(rf'C:\Users\{os.getlogin()}\Desktop\dados.csv', encoding='cp850')
                if 'excel' in tipo.lower():
                    self.df.to_excel(rf'C:\Users\{os.getlogin()}\Desktop\dados.xls',encoding='cp850')
                if 'json' in tipo.lower():
                    self.df.to_json(rf'C:\Users\{os.getlogin()}\Desktop\dados.json', indent=4)
                QMessageBox.about(self, "Alert", 'Dados salvos na área de trabalho')
            except Exception as e:
                QMessageBox.about(self, "Alert", f'Não foi possível salvar os dados, {e}')
        except Exception:
            QMessageBox.about(self, 'ERROR', "Algo deu errado na hora de salvar")

    def buttom_search(self):
        try:
            bd = sqliteConnector(database='BDequipamentos')
            colunas = self.coluna.text().upper()
            if not colunas:
                colunas = '*'
            if colunas != '*':
                colunas = colunas.split(',')
                for i in range(len(colunas)):
                    colunas[i] = f'{colunas[i].upper().strip()}'
                colunas = ','.join(colunas)
            tabela = self.nomeTabela.text()
            if not tabela:
                tabela = 'equipamentos'
            ordenado = self.ordenador.currentText()
            desc = self.desc.isChecked()
            condicao = self.condicao.text()
            if 'drop' in condicao or 'delete' in condicao or 'update' in condicao:
                self.condicao.setText("")
                QMessageBox.about(self, "Alert", "Essas funcionalidades estão bloqueadas aqui")
                return
            resultado = bd.read(colunas=colunas, condicao=condicao, tabela=tabela, order=ordenado, desc=desc)
            resultado.start()
            colunas_bd = ["ID", 'CÓDIGO', 'EQUIPAMENTO', 'RESOLUÇÃO', 'CAPACIDADE', 'FABRICANTE',
                          'LOCAL', 'OPERADOR', 'CRITÉRIO DE ACEITAÇÃO',
                          'UNIDADE DO CRITERIO DE ACEITAÇÃO', 'CERTIFICADO',
                          'NOMENCLATURA DO RESULTADO', 'ERRO', 'INCERTEZA DE MEDIÇÃO',
                          'RESULTADO', 'UNIDADE DO RESULTADO', 'DATA DA CALIBRAÇÃO', 'STATUS',
                          'PERIODICIDADE']
            resultado.join(100)
            resultado = bd.retorno
            if type(resultado) is not list:
                QMessageBox.about(self, "Alert", "A consulta não pode ser feita, algo deu errado com o Banco de dados "
                                                 "ou foi feita uma pesquisa inválida")
                model2 = Modelo_pandas_PyQT5.PandasModel(pd.DataFrame())
                self.tabela.setModel(model2)
                self.validacaodatas.setModel(model2)
                self.quantidade.setText('0')
                return
            elif not resultado:
                QMessageBox.about(self, "Alert", "A consulta feita não consta no banco de dados")
                model2 = Modelo_pandas_PyQT5.PandasModel(pd.DataFrame())
                self.validacaodatas.setModel(model2)
                self.tabela.setModel(model2)
                self.quantidade.setText('0')
                return
            elif colunas == '*':
                self.df = pd.DataFrame(columns=colunas_bd, data=resultado)
                if self.df.empty:
                    QMessageBox.about(self, "Alert", "A consulta feita não consta no banco de dados")
                    model2 = Modelo_pandas_PyQT5.PandasModel(pd.DataFrame())
                    self.validacaodatas.setModel(model2)
                    self.quantidade.setText('0')
                    return
            else:
                self.df = pd.DataFrame(columns=colunas.split(','), data=resultado)
            if 'DATA DA CALIBRAÇÃO' in self.df.columns and not self.df.empty and 'PERIODICIDADE' in self.df.columns:
                datasAtuais = [pd.to_datetime(datetime.now()) for i in range(len(self.df['DATA DA CALIBRAÇÃO']))]
                validar = []
                try:
                    proxima = []
                    for data, adi in zip(self.df['DATA DA CALIBRAÇÃO'], self.df['PERIODICIDADE']):
                        proxima.append(pd.to_datetime(data, errors='coerce') + pd.DateOffset(
                            months=int(adi)))
                    validar = pd.Series(pd.to_datetime(proxima, errors='coerce') >= datasAtuais).to_list()
                except Exception as e:
                    return
                datas = []
                for i in validar:
                    if i:
                        datas.append('EM DIA')
                    else:
                        datas.append("PRECISA CALIBRAR")
                colunaEmdia = pd.Series(datas, name="VALIDADO")

                colunaproximacalibracao = pd.Series(data=proxima, name='Proxima calibração')
                dfdatas = pd.concat([colunaEmdia, colunaproximacalibracao], axis=1, ignore_index=True)
                dfdatas.columns = [colunaEmdia.name, colunaproximacalibracao.name]
                model2 = Modelo_pandas_PyQT5.PandasModel(dfdatas)
                self.validacaodatas.setModel(model2)
            else:
                model2 = Modelo_pandas_PyQT5.PandasModel(pd.DataFrame())
                self.validacaodatas.setModel(model2)
            model = Modelo_pandas_PyQT5.PandasModel(self.df)
            self.tabela.setModel(model)
            if 'CÓDIGO' in self.df.columns:
                valores = set(self.df['CÓDIGO'])
                self.quantidade.setText(str(len(valores)))
                return
            aux = bd.read(colunas='CÓDIGO')
            aux.start()
            aux.join(100)
            aux = bd.retorno
            valores = set(aux)
            bd.retorno = None
            self.quantidade.setText(str(len(valores)))
        except Exception as e:
            QMessageBox.about(self, "Faltal Error", f"A pesquisa feita é inválida")


pasta = os.listdir()
if 'pdfs' not in pasta:
    alert('A pasta dos pdfs não consta no diretório atual, irei criar uma, ponha os pdfs la dentro por favor',
          'Error')
    os.mkdir(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfs"))
if 'BDequipamentos' not in pasta:
    alert("Erro fatal, o banco de dados não consta na pasta")
    exit(-1)
qt = QApplication(argv)
novo = buscaDados()
novo.start()
novo.show()
qt.exec_()
