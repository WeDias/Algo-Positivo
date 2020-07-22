import json
import smtplib
import sqlite3 as sql
from email import encoders
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def tratar_dados(linha) -> False or list:
    """
    :param linha:
    :return:
    """
    if linha.startswith('+') or linha.startswith('| id_opr_cad_pos |'):
        return False
    return list(map(lambda valor: valor.strip(), linha.split('|')))

def add_anexo(path) -> None:
    """
    add_anexo(): Adiciona um arquivo para ser enviado
    path: Caminho do arquivo
    :return: None
    """
    attachment = open(path, 'rb')
    index = path.rfind('/') + 1
    filename = path[index:]
    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload(attachment.read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(part2)
    attachment.close()

def enviar() -> None:
    """
    enviar(): Serve para enviar o arquivo JSON para os enderecos
    de email registrados no banco de dados SQLite3
    :return: None
    """
    global msg
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
    add_anexo('Dados/clientes.json')
    smtp = "smtp.gmail.com"
    server = smtplib.SMTP(smtp, 587)
    server.starttls()
    text = msg.as_string()
    server.login(email_from, open('Dados/senha.txt').read().strip())
    server.sendmail(email_from, email_to, text)
    server.quit()


def main() -> None:
    """
    :return:
    """
    with open('Dados/fatec_opr.csv') as arq_opr:
        operacoes = {}
        for linha in arq_opr.readlines():
            try:
                linha = tratar_dados(linha)
                operacoes[linha[1]] = linha[2]
            except TypeError:
                continue
    del arq_opr
    with open('Dados/fatec_pgt.csv') as arq_pgt:
        clientes = {}
        for linha in arq_pgt.readlines():
            try:
                linha = tratar_dados(linha)[1:8]
                dado = [(datetime.strptime(linha[3], '%d%m%Y') -
                         datetime.strptime(linha[4].split()[0], '%Y-%m-%d')).days,
                        float(linha[5]), linha[6]]
            except (ValueError, TypeError, KeyError):
                continue
            try:
                clientes[operacoes[linha[0]]]
            except KeyError:
                clientes[operacoes[linha[0]]] = []
            finally:
                clientes[operacoes[linha[0]]].append(dado)
    del arq_pgt, dado, operacoes, linha
    analise = {}
    for cliente, pagamentos in clientes.items():
        dias = 0
        analise[cliente] = {
            'STATUS': 'DESCONHECIDO',
            'PORCENTAGEM_DE_ATRASO': 0,
            'VALOR_MEDIO_PAGAMENTOS_ATRASADOS': 0,
            'MEDIA_DE_DIAS_DE_PAGAMENTOS_ATRASADOS': 0,
            'NUMERO_PAGAMENTOS_ATRASADOS': 0,
            'VALOR_TOTAL_PAGAMENTOS_ATRASADOS': 0,
            'VALOR_DE_MAIOR_ATRASO': {
                'MODALIDADE': 'DESCONHECIDO',
                'VALOR': 0
            },
            'MAIOR_NUMERO_DE_ATRASOS': {
                'MODALIDADE': 'DESCONHECIDO',
                'NUMERO_DE_ATRASOS': 0
            },
            'ATRASOS_POR_MODALIDADE': {},
            'NUMERO_DE_PAGAMENTOS': 0,
            'VALOR_TOTAL_PAGAMENTOS': 0,
            'VALOR_MEDIO_PAGAMENTOS': 0,
        }
        for pagamento in pagamentos:
            analise[cliente]['NUMERO_DE_PAGAMENTOS'] += 1
            analise[cliente]['VALOR_TOTAL_PAGAMENTOS'] += pagamento[1]
            if pagamento[0] > 0:
                dias += pagamento[0]
                analise[cliente]['NUMERO_PAGAMENTOS_ATRASADOS'] += 1
                analise[cliente]['VALOR_TOTAL_PAGAMENTOS_ATRASADOS'] += pagamento[1]
                try:
                    analise[cliente]['ATRASOS_POR_MODALIDADE'][pagamento[2]]
                except KeyError:
                    # noinspection PyTypeChecker
                    analise[cliente]['ATRASOS_POR_MODALIDADE'][pagamento[2]] = {'TOTAL_ATRASOS': 0, 'ATRASOS': []}
                finally:
                    # noinspection PyTypeChecker
                    analise[cliente]['ATRASOS_POR_MODALIDADE'][pagamento[2]]['TOTAL_ATRASOS'] += 1
                    # noinspection PyTypeChecker
                    analise[cliente]['ATRASOS_POR_MODALIDADE'][pagamento[2]]['ATRASOS'].append(pagamento[1])
        analise[cliente]['VALOR_TOTAL_PAGAMENTOS'] = \
            round(analise[cliente]['VALOR_TOTAL_PAGAMENTOS'], 2)
        analise[cliente]['VALOR_TOTAL_PAGAMENTOS_ATRASADOS'] = \
            round(analise[cliente]['VALOR_TOTAL_PAGAMENTOS_ATRASADOS'], 2)
        analise[cliente]['VALOR_MEDIO_PAGAMENTOS'] = \
            round(analise[cliente]['VALOR_TOTAL_PAGAMENTOS'] /
                  analise[cliente]['NUMERO_DE_PAGAMENTOS'], 2)
        mod_maior_atraso = valor_maior_atraso = None
        mod_maior_numero_atraso = valor_maior_numero_atraso = None
        for modalidade, atrasos in analise[cliente]['ATRASOS_POR_MODALIDADE'].items():
            # noinspection PyTypeChecker
            maior = max(atrasos['ATRASOS'])
            if not mod_maior_atraso:
                mod_maior_atraso = modalidade
                mod_maior_numero_atraso = modalidade
                valor_maior_atraso = maior
                # noinspection PyTypeChecker
                valor_maior_numero_atraso = atrasos['TOTAL_ATRASOS']
            else:
                if maior > valor_maior_atraso:
                    mod_maior_atraso = modalidade
                    valor_maior_atraso = maior
                # noinspection PyTypeChecker
                if atrasos['TOTAL_ATRASOS'] > valor_maior_numero_atraso:
                    mod_maior_numero_atraso = modalidade
                    # noinspection PyTypeChecker
                    valor_maior_numero_atraso = atrasos['TOTAL_ATRASOS']
            analise[cliente]['VALOR_DE_MAIOR_ATRASO']['MODALIDADE'] = mod_maior_atraso
            analise[cliente]['VALOR_DE_MAIOR_ATRASO']['VALOR'] = valor_maior_atraso
            analise[cliente]['MAIOR_NUMERO_DE_ATRASOS']['MODALIDADE'] = mod_maior_numero_atraso
            analise[cliente]['MAIOR_NUMERO_DE_ATRASOS']['NUMERO_DE_ATRASOS'] = valor_maior_numero_atraso
        try:
            analise[cliente]['MEDIA_DE_DIAS_DE_PAGAMENTOS_ATRASADOS'] = \
                round(dias / analise[cliente]['NUMERO_PAGAMENTOS_ATRASADOS'], 2)
            analise[cliente]['VALOR_MEDIO_PAGAMENTOS_ATRASADOS'] = \
                round(analise[cliente]['VALOR_TOTAL_PAGAMENTOS_ATRASADOS'] /
                      analise[cliente]['NUMERO_PAGAMENTOS_ATRASADOS'], 2)
            analise[cliente]['PORCENTAGEM_DE_ATRASO'] = \
                round((analise[cliente]['NUMERO_PAGAMENTOS_ATRASADOS'] /
                       analise[cliente]['NUMERO_DE_PAGAMENTOS']) * 100, 2)
        except ZeroDivisionError:
            pass
        if analise[cliente]['PORCENTAGEM_DE_ATRASO'] <= 10:
            analise[cliente]['STATUS'] = 'EXCELENTE'
        elif analise[cliente]['PORCENTAGEM_DE_ATRASO'] <= 30:
            analise[cliente]['STATUS'] = 'BOM'
        elif analise[cliente]['PORCENTAGEM_DE_ATRASO'] <= 50:
            analise[cliente]['STATUS'] = 'NEUTRO'
        elif analise[cliente]['PORCENTAGEM_DE_ATRASO'] <= 60:
            analise[cliente]['STATUS'] = 'RUIM'
        else:
            analise[cliente]['STATUS'] = 'PESSIMO'
    del atrasos, cliente, clientes, dias, maior, mod_maior_atraso, mod_maior_numero_atraso, \
        modalidade, pagamento, pagamentos, valor_maior_atraso, valor_maior_numero_atraso
    with open('Dados/clientes.json', 'w') as salvar:
        salvar.write(json.dumps(analise, indent=4))


if __name__ == '__main__':
    main()
    enviar()
