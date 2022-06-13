import sqlite3
import threading
import mysql.connector
import pandas as pd
from re import compile, I


class mysql_connector:
    def __init__(self, host='', user='', password='', database=''):
        # informações do banco de dados
        self.regex_data = compile(r"\d{2}[-\\/]?\d{2}[-\\/]?\d{4}", flags=I)
        self.regex_texto = compile(r"[\w\s]+", flags=I)
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def init_conetion(self):
        self.conexao = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    class read(threading.Thread):
        def __init__(self, host='', user='', password='', colunas='*', condicao="", tabela='equipamentos', order='', desc=False, fullquery='', database='BDequipamentos'):
            threading.Thread.__init__(self)
            self.database = database
            self.colunas = colunas
            self.condicao = condicao
            self.tabela = tabela
            self.order = order
            self.desc = desc
            self.fullquery = fullquery
            self.regex_data = compile(r"\d{2}[-\\/]?\d{2}[-\\/]?\d{4}", flags=I)
            self.regex_texto = compile(r"[\w\s]+", flags=I)
            self.host = host
            self.user = user
            self.password = password
            self.database = database

        def init_conetion(self):
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

        def run(self) -> None:
            try:
                self.init_conetion()
                cursor = self.conexao.cursor()
                self.condicao = self.condicao.lower()
                operadores = ['<', '>', '=', '<=', '>=', 'between', 'like', '%', 'in']
                negacao = 'not' if 'not' in self.condicao.lower().split(" ") else None
                if negacao:
                    self.condicao = self.condicao.replace('not', '')
                    self.condicao = self.condicao.strip()
                if self.colunas != '*':
                    self.colunas = self.colunas.split(',')
                    for i in range(len(self.colunas)):
                        self.colunas[i] = f'[{self.colunas[i].upper().strip()}]'
                    self.colunas = ', '.join(self.colunas)
                if self.condicao:
                    if 'between' in self.condicao.lower():
                        dados = self.condicao.lower().split('between')
                        dados[0] = f'[{(dados[0].strip()).upper()}]'
                        if 'not' in dados[0].lower():
                            dados[0] = dados[0].replace('not', '')
                            dados[0] += 'not'
                        dados[0] += ' between'
                        operadorlogio = 'and' if 'and' in dados[1] else 'or'
                        dadosPassados = dados[1].split(operadorlogio)
                        if dadosPassados[0].isalpha():
                            dadosPassados[0] = f"'{dadosPassados[0]}'"
                        if dadosPassados[0].isalpha():
                            dadosPassados[0] = f"'{dadosPassados[0]}'"
                        dados[1] = " ".join(dadosPassados)
                        self.condicao = dados[0] + f' {operadorlogio} '.join(dadosPassados)
                    else:
                        separador = []
                        for i in range((self.condicao.count('and') + self.condicao.count('or'))):
                            if 'and' in self.condicao:
                                separador.append('and')
                            if 'or' in self.condicao:
                                separador.append('or')
                        cont = 0
                        condicoes = self.condicao.split("and") if 'and' in self.condicao else self.condicao.split("or")
                        self.condicao = ''
                        for condi in condicoes:
                            operador = self.trazeroperador(operadores=operadores, condicoes=condi)
                            operador_aux = operador
                            dados = condi.split(operador)
                            dados[0] = f'[{(dados[0].strip()).upper()}]'
                            if len(dados) == 1:
                                dados.append('" "')
                            elif self.regex_data.findall(condi):
                                if len(dados) == 1:
                                    dados.append('" "')
                                dados[1] = f"'{pd.to_datetime(dados[1])}'"
                            elif 'like' == operador:
                                dados[1] = f"'%{dados[1].strip()}%'"
                            else:
                                if dados[1].isspace():
                                    dados[1] = f"'{dados[1]}'"
                                else:
                                    if self.existe_operador(operadores, dados[1]):
                                        operador = self.trazeroperador(operadores=operadores, condicoes=dados[1])
                                    if operador != '' and operador in dados[1]:
                                        aux = dados[1].split(operador)
                                        for auxs in aux:
                                            if auxs.isalpha():
                                                aux[aux.index(auxs)] = f"'{auxs.strip()}'"
                                            if auxs.isdigit():
                                                aux[aux.index(auxs)] = f"{auxs.strip()}"
                                        dados[1] = f' {operador}'.join(aux)
                                    else:
                                        if dados[1].isdigit():
                                            dados[1] = f"{dados[1].strip()}"
                                        else:
                                            if operador_aux == 'in':
                                                dados[1] = f"{dados[1].strip()}"
                                            else:
                                                dados[1] = f"'{dados[1].strip()}'"
                            condi = f' {operador_aux} '.join(dados)
                            if separador:
                                if cont > 0 and cont != self.condicao.index(condi[-1]):
                                    self.condicao += separador[cont - 1]
                            self.condicao += condi
                            cont += 1
                    if negacao is not None:
                        self.condicao = negacao + self.condicao
                if self.fullquery:
                    try:
                        cursor.execute(self.fullquery)
                        resultado = cursor.fetchall()
                        cursor.close()
                        sqliteConnector.retorno = resultado
                    except sqlite3.Error as e:
                        sqliteConnector.retorno = e
                else:
                    comando = f'SELECT {self.colunas} FROM {self.tabela}'
                    if self.condicao:
                        comando = f'SELECT {self.colunas} FROM {self.tabela} WHERE {self.condicao}'
                        if self.order:
                            comando = f'SELECT {self.colunas} FROM {self.tabela} WHERE {self.condicao} order by {self.order}'
                            if self.desc:
                                comando = f'SELECT {self.colunas} FROM {self.tabela} WHERE {self.condicao} order by {self.order} desc'
                    if self.order and not self.condicao:
                        comando = f'SELECT {self.colunas} FROM {self.tabela} order by {self.order}'
                        if self.desc:
                            comando = f'SELECT {self.colunas} FROM {self.tabela} order by {self.order} desc'

                    comando = comando + ';'
                    cursor.execute(comando)
                    resultado = cursor.fetchall()
                    cursor.close()
                    self.conexao.close()
                    sqliteConnector.retorno = resultado
            except Exception as e:
                sqliteConnector.retorno = e

        def trazeroperador(self, operadores, condicoes):
            operador = ''
            for op in operadores:
                if op in condicoes:
                    operador = op
            return operador

        def existe_operador(self, operadores, condicao):
            for i in operadores:
                if i in condicao:
                    return True
            return False

    class create(threading.Thread):
        def __init__(self, dados, database='', host='', user='', password=''):
            threading.Thread.__init__(self)
            self.dados = dados
            self.database = database
            self.host = host
            self.user = user
            self.password = password
            self.database = database

        def init_conetion(self):
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

        def run(self) -> None:
            try:
                self.init_conetion()
                cursor = self.conexao.cursor()
                lista_de_dados = pd.DataFrame(self.dados)
                lista_de_dados.fillna(" ", inplace=True)
                lista_de_dados.to_sql(con=self.conexao, schema='BDequipamentos', name='equipamentos', method='multi',
                                      if_exists='append', index=False)
                cursor.close()
                self.conexao.close()
            except Exception as e:
                return

    class update(threading.Thread):
        def __init__(self, dados, attr, database, host='', user='', password=''):
            threading.Thread.__init__(self)
            self.dados = dados
            self.attr = attr
            self.database = database
            self.host = host
            self.user = user
            self.password = password
            self.database = database

        def init_conetion(self):
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

        def run(self) -> None:
            try:
                self.init_conetion()
                cursor = self.conexao.cursor()
                attrs = [f'[{i}]' for i in self.attr]
                lista_de_dados = self.dados
                lista_de_dados.fillna(" ", inplace=True)
                valores = lista_de_dados[lista_de_dados.columns[0]].to_list()
                contador = 0
                for vez in range(len(valores)):
                    mandar = "set "
                    contadorvalor = 0
                    for i in lista_de_dados.columns:
                        if i == lista_de_dados.columns[-1]:
                            mandar += f'{attrs[contadorvalor]} = "{lista_de_dados[i].iloc[contador]}"'
                            break
                        mandar += f'{attrs[contadorvalor]} = "{lista_de_dados[i].iloc[contador]}",'
                        contadorvalor += 1
                    contador += 1
                    comando = f'UPDATE equipamentos {mandar} WHERE ID = {lista_de_dados[lista_de_dados.columns[0]].iloc[vez]}; '
                    cursor.execute(comando)
                    self.conexao.commit()
                cursor.close()
                self.conexao.close()
            except Exception as e:
                sqliteConnector.retorno = e

    class delete(threading.Thread):
        def __init__(self, dados, database='', host='', user='', password=''):
            threading.Thread.__init__(self)
            self.dados = dados
            self.database = database
            self.host = host
            self.user = user
            self.password = password
            self.database = database

        def init_conetion(self):
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

        def run(self) -> None:
            try:
                self.init_conetion()
                cursor = self.conexao.cursor()
                valores = self.dados.to_list()
                valores.reverse()
                for vez in valores:
                    comando = f'DELETE FROM equipamentos WHERE ID = {vez};'
                    cursor.execute(comando)
                    self.conexao.commit()
                cursor.close()
                self.conexao.close()
            except Exception as e:
                sqliteConnector.retorno = e


class sqliteConnector(threading.Thread):
    retorno = None

    def __init__(self, database, operacao=''):
        threading.Thread.__init__(self)
        self.database = database
        self.operacao = operacao

    def create_connection(self):
        try:
            self.conector = sqlite3.connect(self.database)
        except sqlite3.Error as e:
            return e

    class read(threading.Thread):
        def __init__(self, colunas='*', condicao="", tabela='equipamentos', order='', desc=False, fullquery='', database='BDequipamentos'):
            threading.Thread.__init__(self)
            self.database = database
            self.colunas = colunas
            self.condicao = condicao
            self.tabela = tabela
            self.order = order
            self.desc = desc
            self.fullquery = fullquery
            self.regex_data = compile(r"\d{2}[-\\/]?\d{2}[-\\/]?\d{4}", flags=I)
            self.regex_texto = compile(r"[\w\s]+", flags=I)

        def create_connection(self):
            try:
                self.conector = sqlite3.connect(self.database)
            except sqlite3.Error as e:
                return e

        def run(self) -> None:
            try:
                self.create_connection()
                cursor = self.conector.cursor()
                self.condicao = self.condicao.lower()
                operadores = ['<', '>', '=', '<=', '>=', 'between', 'like', '%', 'in']
                negacao = 'not' if ' not ' in self.condicao.lower().split(" ") else None
                if negacao:
                    self.condicao = self.condicao.replace('not', '')
                    self.condicao = self.condicao.strip()
                if self.colunas != '*':
                    self.colunas = self.colunas.split(',')
                    for i in range(len(self.colunas)):
                        self.colunas[i] = f'[{self.colunas[i].upper().strip()}]'
                    self.colunas = ', '.join(self.colunas)
                if self.condicao:
                    if 'between' in self.condicao.lower():
                        dados = self.condicao.lower().split('between')
                        dados[0] = f'[{(dados[0].strip()).upper()}]'
                        if 'not' in dados[0].lower():
                            dados[0] = dados[0].replace('not', '')
                            dados[0] += 'not'
                        dados[0] += ' between'
                        operadorlogio = 'and' if 'and' in dados[1] else 'or'
                        dadosPassados = dados[1].split(operadorlogio)
                        if dadosPassados[0].isalpha():
                            dadosPassados[0] = f"'{dadosPassados[0]}'"
                        if dadosPassados[0].isalpha():
                            dadosPassados[0] = f"'{dadosPassados[0]}'"
                        dados[1] = " ".join(dadosPassados)
                        self.condicao = dados[0] + f' {operadorlogio} '.join(dadosPassados)
                    else:
                        separador = []
                        for i in range((self.condicao.count(' and ') + self.condicao.count(' or '))):
                            if ' and ' in self.condicao:
                                separador.append('and')
                            if ' or ' in self.condicao:
                                separador.append('or')
                        cont = 0
                        condicoes = self.condicao.split(" and ") if ' and ' in self.condicao else self.condicao.split(" or ")
                        self.condicao = ''
                        for condi in condicoes:
                            operador = self.trazeroperador(operadores=operadores, condicoes=condi)
                            operador_aux = operador
                            dados = condi.split(operador)
                            dados[0] = f'[{(dados[0].strip()).upper()}]'
                            if len(dados) == 1:
                                dados.append('" "')
                            elif self.regex_data.findall(condi):
                                if len(dados) == 1:
                                    dados.append('" "')
                                dados[1] = f"'{pd.to_datetime(dados[1])}'"
                            elif 'like' == operador:
                                dados[1] = f"'%{dados[1].strip()}%'"
                            else:
                                if dados[1].isspace():
                                    dados[1] = f"'{dados[1]}'"
                                else:
                                    if self.existe_operador(operadores, dados[1]):
                                        operador = self.trazeroperador(operadores=operadores, condicoes=dados[1])
                                    if operador != '' and operador in dados[1]:
                                        aux = dados[1].split(operador)
                                        for auxs in aux:
                                            if auxs.isalpha():
                                                aux[aux.index(auxs)] = f"'{auxs.strip()}'"
                                            if auxs.isdigit():
                                                aux[aux.index(auxs)] = f"{auxs.strip()}"
                                        dados[1] = f' {operador}'.join(aux)
                                    else:
                                        if dados[1].isdigit():
                                            dados[1] = f"{dados[1].strip()}"
                                        else:
                                            if operador_aux == 'in':
                                                dados[1] = f"{dados[1].strip()}"
                                            else:
                                                dados[1] = f"'{dados[1].strip()}'"
                            condi = f' {operador_aux} '.join(dados)
                            if separador:
                                if cont > 0 and cont != self.condicao.index(condi[-1]):
                                    self.condicao += separador[cont - 1]
                            self.condicao += condi
                            cont += 1
                    if negacao is not None:
                        self.condicao = negacao + self.condicao
                if self.fullquery:
                    try:
                        cursor.execute(self.fullquery)
                        resultado = cursor.fetchall()
                        cursor.close()
                        sqliteConnector.retorno = resultado
                    except sqlite3.Error as e:
                        sqliteConnector.retorno = e
                else:
                    comando = f'SELECT {self.colunas} FROM {self.tabela}'
                    if self.condicao:
                        comando = f'SELECT {self.colunas} FROM {self.tabela} WHERE {self.condicao}'
                        if self.order:
                            comando = f'SELECT {self.colunas} FROM {self.tabela} WHERE {self.condicao} order by {self.order}'
                            if self.desc:
                                comando = f'SELECT {self.colunas} FROM {self.tabela} WHERE {self.condicao} order by {self.order} desc'
                    if self.order and not self.condicao:
                        comando = f'SELECT {self.colunas} FROM {self.tabela} order by {self.order}'
                        if self.desc:
                            comando = f'SELECT {self.colunas} FROM {self.tabela} order by {self.order} desc'

                    comando = comando + ';'
                    cursor.execute(comando)
                    resultado = cursor.fetchall()
                    cursor.close()
                    self.conector.close()
                    sqliteConnector.retorno = resultado
            except Exception as e:
                sqliteConnector.retorno = e

        def trazeroperador(self, operadores, condicoes):
            operador = ''
            for op in operadores:
                if op in condicoes:
                    operador = op
            return operador

        def existe_operador(self, operadores, condicao):
            for i in operadores:
                if i in condicao:
                    return True
            return False

    class create(threading.Thread):
        def __init__(self, dados, database):
            threading.Thread.__init__(self)
            self.dados = dados
            self.database = database

        def create_connection(self):
            try:
                self.conector = sqlite3.connect(self.database)
            except sqlite3.Error as e:
                return e

        def run(self) -> None:
            try:
                self.create_connection()
                cursor = self.conector.cursor()
                lista_de_dados = pd.DataFrame(self.dados)
                lista_de_dados.fillna(" ", inplace=True)
                lista_de_dados.to_sql(con=self.conector, schema='BDequipamentos', name='equipamentos', method='multi',
                                      if_exists='append', index=False)
                cursor.close()
                self.conector.close()
            except Exception as e:
                return

    class update(threading.Thread):
        def __init__(self, dados, attr, database):
            threading.Thread.__init__(self)
            self.dados = dados
            self.attr = attr
            self.database = database

        def create_connection(self):
            try:
                self.conector = sqlite3.connect(self.database)
            except sqlite3.Error as e:
                return e

        def run(self) -> None:
            try:
                self.create_connection()
                cursor = self.conector.cursor()
                attrs = [f'`{i}`' for i in self.attr]
                lista_de_dados = self.dados
                lista_de_dados.fillna(" ", inplace=True)
                valores = lista_de_dados[lista_de_dados.columns[0]].to_list()
                contador = 0
                for vez in range(len(valores)):
                    mandar = "set "
                    contadorvalor = 0
                    for i in lista_de_dados.columns:
                        if i == lista_de_dados.columns[-1]:
                            mandar += f'{attrs[contadorvalor]} = "{lista_de_dados[i].iloc[contador]}"'
                            break
                        mandar += f'{attrs[contadorvalor]} = "{lista_de_dados[i].iloc[contador]}",'
                        contadorvalor += 1
                    contador += 1
                    comando = f'UPDATE equipamentos {mandar} WHERE ID = {lista_de_dados[lista_de_dados.columns[0]].iloc[vez]}; '
                    cursor.execute(comando)
                    self.conector.commit()
                cursor.close()
                self.conector.close()
            except Exception as e:
                sqliteConnector.retorno = e

    class delete(threading.Thread):
        def __init__(self, dados, database):
            threading.Thread.__init__(self)
            self.dados = dados
            self.database = database

        def create_connection(self):
            try:
                self.conector = sqlite3.connect(self.database)
            except sqlite3.Error as e:
                return e

        def run(self) -> None:
            try:
                self.create_connection()
                cursor = self.conector.cursor()
                valores = self.dados.to_list()
                valores.reverse()
                for vez in valores:
                    comando = f'DELETE FROM equipamentos WHERE ID = {vez};'
                    cursor.execute(comando)
                    self.conector.commit()
                cursor.close()
                self.conector.close()
            except Exception as e:
                sqliteConnector.retorno = e
