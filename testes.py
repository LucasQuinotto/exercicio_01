import MySQLdb
from pandas import pandas as pd

conexao = MySQLdb.connect(db="exercicio_01", user="root", host="localhost", port=33069)
conexao.autocommit(True)
cursor = conexao.cursor()


def consultar_pessoa_divida(dict_values):
    sql = f"""SELECT * FROM pessoa WHERE cpf = '{dict_values['cpf']}'"""
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    divida = df[2][0]
    print(divida)

consultar_pessoa_divida(dict(cpf="0001"))