from flask import Flask, request, json
import MySQLdb
import pandas as pd
from datetime import datetime


app = Flask(__name__)

conexao = MySQLdb.connect(db="exercicio_01", user="root", host="localhost", port=33069)
conexao.autocommit(True)
cursor = conexao.cursor()


def calcular_idade(nascimento):
    today = datetime.today()
    return today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))


@app.route("/serasa/consulta/")
def consultar_pessoas():
    sql = """SELECT * FROM pessoa"""
    cursor.execute(sql)
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)

    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"])
    df = df.loc[df["data_nascimento"].apply(calcular_idade) >= 18]

    df = df.drop(["cpf", "data_nascimento"], axis=1)
    print(df)
    return df.to_json(orient="records")


@app.route("/pessoa/consultar-divida/", methods=["POST"])
def consultar_pessoa_divida():
    raw_request = request.data.decode("utf-8")
    dict_values = json.loads(raw_request)

    sql = f"""SELECT * FROM pessoa WHERE cpf = '{dict_values['cpf']}'"""
    cursor.execute(sql)
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)

    return df.to_json(orient="records").replace("\/", "/")


@app.route("/pessoa/pagar-divida/", methods=["POST"])
def pagar_pessoa_divida():
    raw_request = request.data.decode("utf-8")
    dict_values = json.loads(raw_request)

    try:
        sql = f"""SELECT * FROM pessoa WHERE cpf = '{dict_values['cpf']}'"""
        cursor.execute(sql)
        df = pd.DataFrame(cursor.fetchall())
        if dict_values['divida'] != str(df[2][0]):
            return "o valor da dívida não corresponde ao valor informado ..."
        else:
            sql2 = f"UPDATE pessoa SET divida = 0.0, score = 1000 WHERE cpf = {dict_values['cpf']}"
            cursor.execute(sql2)
            return "divida paga com sucesso !!"
    except:
        return "pessoa não encontrada ..."


if __name__ == "__main__":
    app.run(debug=True)
