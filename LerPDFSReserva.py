from os.path import join
from re import compile, IGNORECASE
from threading import Thread
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import pandas as pd
from tabula.io import read_pdf


class LerPDFS(Thread):
    @staticmethod
    def lerPDF(arquivo):
        fp = open(f"{arquivo}", 'rb')
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        # device = TextConverter(rsrcmgr, retstr, codec='cp850', laparams=laparams)
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = PDFPage.get_pages(fp)
        data = ""
        for page in pages:
            interpreter.process_page(page)
            data += retstr.getvalue()
        return data.replace("\n", " ").replace("  ", " ")

    def formatar(self, x):
        if "º" not in x:
            x = x.replace(",", ".")
            return x
        else:
            if not self.regex_auxiliar.findall(x):
                x = x.replace("º", ".")
                x = x.replace("'", "")
                x = x.split(".")
                return str(float(x[0]) + (float(x[1]) / 60))
            else:
                return x

    @staticmethod
    def ajuntar_tamanho(ajutaveis):
        tamanhos = []
        for indice in ajutaveis.keys():
            tamanhos.append(len(ajutaveis[indice]))
        for indice in ajutaveis.keys():
            if len(ajutaveis[indice]) < max(tamanhos):
                for maximo in range(max(tamanhos) - len(ajutaveis[indice])):
                    ajutaveis[indice].append(" ")
        return ajutaveis

    @staticmethod
    def preenchervazios(data):
        colunas = "CÓDIGO,EQUIPAMENTO,RESOLUÇÃO,CAPACIDADE,FABRICANTE,LOCAL,CERTIFICADO,DATA DA CALIBRAÇÃO".split(",")
        for p in colunas:
            data[p] = data[p].fillna(method='ffill')
        return data

    def retirar_space(self, valor):
        coluna = []
        for i in valor.values:
            if str(i).isspace():
                coluna.append(None)
            else:
                coluna.append(i)
        return pd.Series(coluna, name=valor.name)

    def __init__(self, pdfs):
        self.equipamentos = pd.DataFrame(pd.read_excel(join('pdfs', "baseDadosReserva.xls")))
        Thread.__init__(self)
        self.equipamentos['ERRO'].fillna(0, inplace=True)
        self.equipamentos['INCERTEZA DE MEDIÇÃO'].fillna(0, inplace=True)
        self.equipamentos['CERTIFICADO'].fillna(0, inplace=True)
        self.df_aux = pd.DataFrame(columns=self.equipamentos.columns)
        # self.equipamentos = self.equipamentos.drop('Unnamed: 0', axis=1)
        self.pdfs = pdfs
        # pdfs = ["0353 2020.pdf", "0345 2020.pdf",'0431 2020.pdf', '0432 2020.pdf', '0433 2020.pdf','0485 2020.pdf']
        # pdfs = ['Certificado 38432_2020.pdf']
        self.valores = list(set(self.equipamentos['CÓDIGO']))
        self.valores.pop(0)
        self.regex_certificado = compile(r"\s(\d{3,5}[-/]\d{4})\s", flags=IGNORECASE)
        self.regex_auxiliar = compile(r"^\d+$", flags=IGNORECASE)
        self.regex_datadecalibracao = compile(r"\sData da calibração\s?:(\s\d{2}[\\/]\d{2}[\\/]\d{4}\s)", flags=IGNORECASE)
        self.regex_datadecalibracao_aux = compile(r"(\s\d{2}[\\/]\d{2}[\\/]\d{4}\s)", flags=IGNORECASE)
        self.regex_identificacao = compile(r"Identificação\s?:\s(\w{1,3}-?\d{1,3}[-/]?\d{1,3})?", flags=IGNORECASE)
        self.regex_identificacao_aux = compile(r"Identificação:\s(\d+)", flags=IGNORECASE)
        self.regex_nome = compile(r"\sInstrumento:\s(.*?)\sFabricante: Modelo: N° de série:\s", flags=IGNORECASE)
        self.regex_nome_aux = compile(r"\sInstrumento:\s(.*?)\sModelo\s?: Fabricante: N° de série:\s", flags=IGNORECASE)
        self.regex_fabricante = compile(r"\sFabricante: Modelo: N° de série:\s(\w+)\s", flags=IGNORECASE)
        self.fabricante_aux = compile(fr"\sFabricante: N° de série:\s\d{2}[\\/]\d{2}[\\/]\d{4}\s(\w+)\s", flags=IGNORECASE)
        self.regex_local_de_calibracao = compile(r"\sLocal da calibração\s?:\s(.+?)\s[Calibrdo p:Dtcçã]+?", flags=IGNORECASE)

    def run(self) -> None:
        for i in self.pdfs:
            if ".pdf" in i:
                texto = self.lerPDF(join("pdfs", i))
                try:
                    certificadoNumero = self.regex_certificado.findall(texto)
                    data_calibracao = self.regex_datadecalibracao.findall(texto) if self.regex_datadecalibracao.findall(
                        texto) else self.regex_datadecalibracao_aux.findall(texto)
                    identificacao = self.regex_identificacao.findall(texto) or self.regex_identificacao_aux.findall(
                        texto)
                    nome = self.regex_nome.findall(texto) if self.regex_nome.findall(
                        texto) else self.regex_nome_aux.findall(texto)
                    fabricante = self.regex_fabricante.findall(texto)
                    local = self.regex_local_de_calibracao.findall(texto)
                    if not fabricante or not local:
                        palavras = texto.split(' ')
                        if not nome:
                            nome = [palavras[palavras.index("Instrumento:") + 1]]
                        if not fabricante:
                            fabricante = [palavras[palavras.index('Fabricante:') + 5]]
                        if not local:
                            local = palavras[palavras.index('Local') + 4]
                except Exception as e:
                    print(f"{i} não pode ser lido, erro")
                    continue
                # pegando as tabelas do pdf
                tabela = pd.DataFrame()
                try:
                    tabelas = read_pdf(join("pdfs", i), pages='all', encoding="cp850")
                    tabela = pd.concat(tabelas, ignore_index=False)
                    tabela = tabela[tabela['Erro'].notna()].loc[:, ['Erro', "Incerteza"]]
                    tabela = pd.DataFrame(tabela[tabela.index > 1])
                except Exception:
                    print(f'Não for possível ler a tabela do arquivo {i}')
                    continue
                finally:
                    try:
                        tabela.reset_index(drop=True, inplace=True)
                        self.equipamentos.reset_index(drop=True, inplace=True)
                        # self.equipamentos.reindex(list(range(len(self.equipamentos['CÓDIGO']))))
                        # tabela.reindex(list(range(len(tabela['Erro']))))
                    except Exception as e:
                        pass

                try:
                    if bool(list(tabela['Erro'])) or bool(list(tabela['Incerteza'])):
                        pass
                except Exception as E:
                    print(f"Não foi possível ler o {i}")
                    continue

                try:
                    resolucao = self.equipamentos.loc[
                                    self.equipamentos['EQUIPAMENTO'].str.contains(nome[0].split(" ")[0],
                                                                                  na=False), 'RESOLUÇÃO'].iloc[
                                :len(tabela['Erro'])]
                    capacidade = self.equipamentos.loc[
                                     self.equipamentos['EQUIPAMENTO'].str.contains(nome[0].split(" ")[0],
                                                                                   na=False), 'CAPACIDADE'].iloc[
                                 :len(tabela['Erro'])]
                    criterio_avaliacao = self.equipamentos.loc[
                                             self.equipamentos['EQUIPAMENTO'].str.contains(nome[0].split(" ")[0],
                                                                                           na=False), 'CRITÉRIO DE ACEITAÇÃO'].iloc[
                                         :len(tabela['Erro'])]

                    unidade_cri_avi = self.equipamentos.loc[
                                          self.equipamentos['EQUIPAMENTO'].str.contains(nome[0].split(" ")[0],
                                                                                        na=False), 'UNIDADE DO CRITERIO DE ACEITAÇÃO'].iloc[
                                      :len(tabela['Erro'])]
                    nomenclatura_do_resultado = self.equipamentos.loc[
                                                    self.equipamentos['EQUIPAMENTO'].str.contains(
                                                        nome[0].split(" ")[0],
                                                        na=False), 'NOMENCLATURA DO RESULTADO'].iloc[
                                                :len(tabela['Erro'])]
                    unidade_do_resultado = self.equipamentos.loc[
                                               self.equipamentos['EQUIPAMENTO'].str.contains(nome[0].split(" ")[0],
                                                                                             na=False), 'UNIDADE DO RESULTADO'].iloc[
                                           :len(tabela['Erro'])]

                    tabela['Erro'] = tabela['Erro'].apply(lambda x: self.formatar(str(x)))
                    tabela['Incerteza'] = tabela["Incerteza"].apply(lambda x: self.formatar(str(x)))

                    tabela['Erro'] = tabela['Erro'].astype('float64')
                    tabela['Incerteza'] = tabela['Incerteza'].astype('float64')
                    criterio_avaliacao = criterio_avaliacao.apply(lambda x: self.formatar(str(x)))
                    criterio_avaliacao.index = [i for i in range(len(criterio_avaliacao))]
                    resultado = tabela['Erro'] + tabela['Incerteza']
                    resultado = resultado.apply(lambda x: self.formatar(str(x)))
                    resultado.index = [i for i in range(len(criterio_avaliacao))]
                    validar = pd.Series(resultado <= criterio_avaliacao).to_list()
                    lista_status = []
                    for valor in validar:
                        if valor:
                            lista_status.append('OK')
                        else:
                            lista_status.append("NOK")
                    dados = {
                        'CÓDIGO': identificacao,
                        'EQUIPAMENTO': nome,
                        'RESOLUÇÃO': resolucao.to_list(),
                        'CAPACIDADE': capacidade.to_list(),
                        'FABRICANTE': fabricante,
                        'LOCAL': local,
                        'OPERADOR': [" " for i in range(len(tabela['Erro']))],
                        'CRITÉRIO DE ACEITAÇÃO': criterio_avaliacao.to_list(),
                        'UNIDADE DO CRITERIO DE ACEITAÇÃO': unidade_cri_avi.to_list(),
                        'CERTIFICADO': certificadoNumero,
                        'NOMENCLATURA DO RESULTADO': nomenclatura_do_resultado.to_list(),
                        'ERRO': tabela['Erro'].to_list(),
                        'INCERTEZA DE MEDIÇÃO': tabela['Incerteza'].to_list(),
                        'RESULTADO': (tabela['Erro'] + tabela['Incerteza']).to_list(),
                        'UNIDADE DO RESULTADO': unidade_do_resultado.to_list(),
                        'DATA DA CALIBRAÇÃO': data_calibracao,
                        'STATUS': lista_status
                    }
                    dados = self.ajuntar_tamanho(dados)
                    dados = pd.DataFrame(dados, index=[i for i in range(len(tabela['Erro']))])

                    if self.df_aux.empty:
                        self.df_aux = dados.copy()
                    else:
                        self.df_aux = pd.concat([self.df_aux, dados], axis=0, ignore_index=True)
                    print(f"OK {i}")
                    continue
                except Exception as e:
                    print(f"{i}, Deu erro")
                    continue
        try:
            # arrumando a coluna de resultado
            self.df_aux['ERRO'] = self.df_aux['ERRO'].apply(lambda x: self.formatar(str(x)))
            self.df_aux['INCERTEZA DE MEDIÇÃO'] = self.df_aux['INCERTEZA DE MEDIÇÃO'].apply(
                lambda x: self.formatar(str(x)))
            self.df_aux.loc[:, ['INCERTEZA DE MEDIÇÃO', 'ERRO']] = self.df_aux.loc[:,
                                                                   ['INCERTEZA DE MEDIÇÃO', 'ERRO']].astype(
                'float64')

            self.df_aux['RESULTADO'] = self.df_aux['RESULTADO'].apply(lambda x: self.formatar(str(x)))
            self.df_aux['CRITÉRIO DE ACEITAÇÃO'] = self.df_aux['CRITÉRIO DE ACEITAÇÃO'].apply(
                lambda x: self.formatar(str(x)))
            validacao_status = self.df_aux['RESULTADO'] <= self.df_aux['CRITÉRIO DE ACEITAÇÃO']
            serie_validade = pd.DataFrame(validacao_status)
            self.df_aux.loc[:, "STATUS"] = "OK" if serie_validade.all else "NOK"

            self.df_aux = self.df_aux.apply(lambda x: self.retirar_space(x))
            self.df_aux.ffill(inplace=True)
            self.df_aux.fillna(value=0)
            self.df_aux.to_excel(join("pdfs", "DadosLidos.xls"))
        except Exception as e:
            pass
