from threading import Thread
from pandas import DataFrame, to_datetime
from CRUD import sqliteConnector
from PyQt5.QtWidgets import QMessageBox
from re import I, compile

regex_auxiliar = compile(r"^\d+$", I)


def formatar(x):
    if "º" not in x:
        x = x.replace(",", ".")
        return x
    else:
        if not regex_auxiliar.findall(x):
            x = x.replace("º", ".")
            x = x.replace("'", "")
            x = x.split(".")
            return str(float(x[0]) + (float(x[1]) / 60))
        else:
            return x


def salvar(equipamentos, tela):
    try:
        equipamentos = DataFrame(equipamentos)
        banco = sqliteConnector(database='BDequipamentos')
        QMessageBox.about(tela, 'Alert', "Os dados estão sendo salvos, por favor aguarde um pouco")
        equipamentos['DATA DA CALIBRAÇÃO'] = to_datetime(equipamentos['DATA DA CALIBRAÇÃO'])
        equipamentos['ERRO'] = equipamentos['ERRO'].apply(lambda x: formatar(str(x)))
        equipamentos['ERRO'] = equipamentos['ERRO'].astype('float64')
        equipamentos['INCERTEZA DE MEDIÇÃO'] = equipamentos['INCERTEZA DE MEDIÇÃO'].astype('float64')
        equipamentos['INCERTEZA DE MEDIÇÃO'] = equipamentos['INCERTEZA DE MEDIÇÃO'].apply(lambda x: formatar(str(x)))
        equipamentos['RESULTADO'] = equipamentos['RESULTADO'].astype('float64')
        equipamentos['CRITÉRIO DE ACEITAÇÃO'] = equipamentos['CRITÉRIO DE ACEITAÇÃO'].apply(lambda x: formatar(str(x)))

        valores = set(equipamentos['CÓDIGO'])
        for i in valores:
            criar = banco.create(dados=equipamentos.loc[equipamentos['CÓDIGO'] == i,], database='BDequipamentos')
            criar.start()
            print('ok')
        QMessageBox.about(tela, 'Alert', "Os dados foram salvos")
    except Exception as e:
        print(f"{e}")
        return


def alterar(equipamentos, tela):
    try:
        banco = sqliteConnector(database='BDequipamentos')
        valores = set(equipamentos['CÓDIGO'])
        QMessageBox.about(tela, 'Alert', "Os dados estão sendo alterados, por favor aguarde um pouco")
        for i in valores:
            resultado = banco.read('*', condicao=f'código = {i}')
            resultado.start()
            resultado.join(1000)
            resultado = sqliteConnector.retorno
            colunas_bd = ["ID", 'CÓDIGO', 'EQUIPAMENTO', 'RESOLUÇÃO', 'CAPACIDADE', 'FABRICANTE',
                          'LOCAL', 'OPERADOR', 'CRITÉRIO DE ACEITAÇÃO',
                          'UNIDADE DO CRITERIO DE ACEITAÇÃO', 'CERTIFICADO',
                          'NOMENCLATURA DO RESULTADO', 'ERRO', 'INCERTEZA DE MEDIÇÃO',
                          'RESULTADO', 'UNIDADE DO RESULTADO', 'DATA DA CALIBRAÇÃO', 'STATUS',
                          'PERIODICIDADE']
            aux = DataFrame(columns=colunas_bd, data=resultado)
            if aux.empty:
                a = Thread(target=salvar(equipamentos, tela))
                a.start()
            else:
                up = banco.update(dados=equipamentos.loc[equipamentos['CÓDIGO'] == i,],
                                  attr=equipamentos.loc[equipamentos['CÓDIGO'] == i,].columns,
                                  database="BDequipamentos")
                up.start()
                print('ok')
        QMessageBox.about(tela, 'Alert', "Os dados foram alterados")
    except Exception as e:
        print(f"{e}")
        return


def delete(ids, tela):
    try:
        QMessageBox.about(tela, 'Alert', "Os dados estão sendo deletados")
        banco = sqliteConnector(database='BDequipamentos')
        dele = banco.delete(dados=ids, database="BDequipamentos")
        dele.start()
        QMessageBox.about(tela, 'Alert', "Os dados foram deletados")
        print('ok')
    except Exception as e:
        print(f"{e}")
        return
