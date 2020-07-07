import json
import smtplib
import pandas as pd
import sqlite3 as sql
from email import encoders
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def tratar() -> None:
    """
    :return:
    """
    with open('Dados/Bruto/stg_mdl.csv') as mdl:
        with open('Dados/Tratado/stg_mdl_ok.csv', 'w') as mdl_ok:
            texto = ''
            for linha in mdl:
                mdl_dados = linha.split('|')
                texto += f'{mdl_dados[1]}|{mdl_dados[2]}\n'
            mdl_ok.write(texto)
    del mdl, mdl_ok, texto
    df_opr = pd.read_csv('Dados/Bruto/fatec_opr.csv', sep='|', usecols=[2, 11])
    df_opr['DOC_CLI'] = df_opr.DOC_CLI.astype('str')
    df_opr['DOC_CLI'].duplicated().sum()
    df_opr_ok = df_opr.loc[df_opr['DOC_CLI'].str.len() == 11]
    df_opr_ok.to_csv('Dados/Tratado/df_opr_ok.csv', index=False, header=True)
    del df_opr, df_opr_ok
    df_endereco = pd.read_csv('Dados/Bruto/fatec_endereco_pessoa.csv', sep='|', usecols=[1, 2, 3])
    df_cpf = pd.read_csv('Dados/Bruto/fatec_endereco_pessoa.csv', sep='|', usecols=[1, 2, 3, 4])
    df_modelo = pd.DataFrame(columns=['doc_cli', 'idc_sexo', 'ano_data_nascimento', 'nom_cidade', 'des_estado'])
    for index in range(len(df_endereco.index)):
        cidade = df_endereco.iloc[index, 1].strip()
        for index2 in range(len(df_cpf.index)):
            ano = df_cpf.iloc[index2, 3].strip()
            if df_endereco.iloc[index, 0] == \
                    df_cpf.iloc[index2, 0] and ano != 'NULL' and cidade != 'CIDADE NAO ENCONTRADA':
                df_modelo.loc[0] = [df_cpf.iloc[index2, 1], df_cpf.iloc[index2, 2].strip(),
                                    df_cpf.iloc[index2, 3].strip(), df_endereco.iloc[index, 1].strip(),
                                    df_endereco.iloc[index, 2].strip()]
                df_modelo.index = df_modelo.index + 1
    df_modelo = df_modelo.sort_index()
    df_modelo.to_csv('Dados/Tratado/pessoa.csv', index=False, header=True, sep="|")


def analisar() -> None:
    """
    :return:
    """
    dados_pessoas = {}
    with open('Dados/Tratado/fatec_pessoa_ok.csv') as arq_pessoa:
        ano_atual = datetime.now().year
        arq_pessoa.readline()
        for linha in arq_pessoa.readlines():
            dados_pessoa = linha.rstrip().split('|')
            dados_pessoas[dados_pessoa[0]] = {
                'sexo': dados_pessoa[1],
                'idade': ano_atual - int(dados_pessoa[2]),
                'cidade': dados_pessoa[3],
                'estado': dados_pessoa[4]
            }
    dados_estados = {}
    del arq_pessoa, dados_pessoa, linha, ano_atual
    with open('Dados/Tratado/fatec_opr_ok.csv') as arq_operacao:
        arq_operacao.readline()
        for linha in arq_operacao.readlines():
            dados_operacao = linha.rstrip().split('|')
            try:
                pessoa = dados_pessoas[dados_operacao[0]]
            except KeyError:
                continue
            try:
                dados_estados[pessoa['estado']]
            except KeyError:
                padrao = {
                    'qtd_clientes': 0,
                    'qtd_sexo_f': 0,
                    'qtd_sexo_m': 0,
                    'modalidades': {
                        'A01': 0, 'A02': 0, 'A04': 0, 'A05': 0, 'A99': 0,
                        'B01': 0, 'B02': 0, 'B03': 0, 'B04': 0, 'B05': 0,
                        'B06': 0, 'B07': 0, 'B99': 0, 'C01': 0, 'D01': 0,
                        'E01': 0, 'E02': 0, 'F01': 0, 'G01': 0
                    }
                }
                dados_estados[pessoa['estado']] = {
                    'soma_idades': 0,
                    'soma_idades_f': 0,
                    'soma_idades_m': 0,
                    'total_clientes': 0,
                    'total_clientes_sexo_f': 0,
                    'total_clientes_sexo_m': 0,
                    'media_idade_clientes': 0,
                    'media_idade_sexo_f': 0,
                    'media_idade_sexo_m': 0,
                    'faixas': {
                        '18-29': padrao.copy(),
                        '30-39': padrao.copy(),
                        '40-49': padrao.copy(),
                        '50-59': padrao.copy(),
                        '60+': padrao.copy(),
                    }
                }
            finally:
                estado_atual = dados_estados[pessoa['estado']]
                sexo = pessoa['sexo'].lower()
                estado_atual['total_clientes'] += 1
                estado_atual['soma_idades'] += pessoa['idade']
                estado_atual[f'total_clientes_sexo_{sexo}'] += 1
                estado_atual[f'soma_idades_{sexo}'] += pessoa['idade']
                # noinspection PyTypeChecker
                estado_atual['media_idade_clientes'] = \
                    round(estado_atual['soma_idades'] / estado_atual['total_clientes'], 2)
                # noinspection PyTypeChecker
                estado_atual[f'media_idade_sexo_{sexo}'] = \
                    round(estado_atual[f'soma_idades_{sexo}'] / estado_atual[f'total_clientes_sexo_{sexo}'], 2)
                if pessoa['idade'] <= 29:
                    faixa = '18-29'
                elif pessoa['idade'] <= 39:
                    faixa = '30-39'
                elif pessoa['idade'] <= 49:
                    faixa = '40-49'
                elif pessoa['idade'] <= 59:
                    faixa = '50-59'
                else:
                    faixa = '60+'
                estado_atual['faixas'][faixa]['qtd_clientes'] += 1
                estado_atual['faixas'][faixa][f'qtd_sexo_{sexo}'] += 1
                mod = estado_atual['faixas'][faixa]['modalidades'].copy()
                mod[dados_operacao[1]] += 1
                estado_atual['faixas'][faixa]['modalidades'] = mod.copy()
                del dados_pessoas[dados_operacao[0]]
    del faixa, linha, padrao, pessoa, sexo, estado_atual, \
        arq_operacao, dados_operacao, dados_pessoas, mod
    for chave, valor in dados_estados.items():
        del dados_estados[chave]['soma_idades'], \
            dados_estados[chave]['soma_idades_f'], \
            dados_estados[chave]['soma_idades_m']
    with open('Dados/Final/estados.json', 'w') as salvar:
        salvar.write(json.dumps(dados_estados, indent=4))


def enviar() -> None:
    """
    :return:
    """
    conn = sql.connect('Dados/banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM emails;')
    email_destino = []
    for email in cursor.fetchall():
        email_destino.append(email[0])
    cursor.close()
    email_from = 'algopositivospc@gmail.com'
    email_to = email_destino
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Subject'] = 'Dados'
    html = '''\
    <html>
     <head></head>
      <body>
       <img src="https://raw.githubusercontent.com/IsraelAugusto0110/PI_ADS_2Sem/master/Documenta%C3%A7%C3%A3o/bg.png"/>
       <p><font size="2">Este é um e-mail automático, gerado pelo algopositivo.</font></p>
      </body>
    </html>
    '''
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
    attachment = open('Dados/Final/estados.json', 'rb')
    filename = 'estados.json'
    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload(attachment.read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(part2)
    attachment.close()
    smtp = "smtp.gmail.com"
    server = smtplib.SMTP(smtp, 587)
    server.starttls()
    text = msg.as_string()
    server.login(email_from, open('Dados/senha.txt').read().strip())
    server.sendmail(email_from, email_to, text)
    server.quit()


if __name__ == '__main__':
    analisar()
