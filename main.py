from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional

# Azure database for MySQLへの接続用のモジュールをインポート
import mysql.connector
from mysql.connector import errorcode

# .envファイルから環境変数を読み込む
# dotenv_path = join(dirname(__file__), ".env")
# load_dotenv(dotenv_path)

# SERVER = os.environ.get("SERVER_NAME")
# ADMIN = os.environ.get("ADMIN")
# PWD = os.environ.get("PASSWORD")
# DB = os.environ.get("DATABASE")
# SLL = os.environ.get("SSL_PATH")

SERVER = "xxx"
ADMIN = "xxx"
PWD = "xxx"
DB = "xxx"
SLL = "xxx"

# Obtain connection string information from the portal
config = {
    'host':f'{SERVER}.mysql.database.azure.com',
    'user':f'{ADMIN}',
    'password':f'{PWD}',
    'database':f'{DB}',
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': f'{SLL}/DigiCertGlobalRootG2.crt.pem'
}

# ここからAPIの実装----------------------------------------------------------
app = FastAPI(
    title="POSアプリAPI",
    description="POSアプリのAPI仕様です。",
    version="0.0.1",
)

# .envファイルの内容をロード
# load_dotenv()

# テスト用の変数
# code = "363349884013"

# テスト用のAPI
@app.get("/")
def test():
    return {"Hello": "World"}

# 商品情報取得用のAPI
@app.get("/get-products/{code}", summary="商品情報取得API")
def read_items(code):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    # DBへ正常に接続できたときの処理
    else:
        cursor = conn.cursor()

        # Read data
        cursor.execute(f"SELECT PRD_ID, NAME, PRICE FROM m_product WHERE CODE={code};")
        rows = cursor.fetchall()
        print("Read", cursor.rowcount, "row(s) of data.")
        
        # 商品マスタに商品があれば、商品一意コード,商品名商,商品単価を格納。ない場合はNullを返す
        if len(rows) >= 1:
            prd_id, name, price = rows[0]
        else:
            return None

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
        
        return {"prd_id": prd_id, "code":code, "name": name, "price": price}