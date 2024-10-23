from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
# from typing import List
# import os
# import datetime

# Azure database for MySQLへの接続用のモジュールをインポート
# import mysql.connector
# from mysql.connector import errorcode

# # .envファイルから環境変数を読み込む
# dotenv_path = join(dirname(__file__), ".env")
# load_dotenv(dotenv_path)

# SERVER = os.environ.get("SERVER_NAME")
# ADMIN = os.environ.get("ADMIN")
# PWD = os.environ.get("PASSWORD")
# DB = os.environ.get("DATABASE")
# SLL = os.environ.get("SSL_PATH")

# SERVER = os.getenv("SERVER_NAME")
# ADMIN = os.getenv("ADMIN_NAME")
# PWD = os.getenv("PWD")
# DB = os.getenv("DB_NAME")
# SLL_CA = os.getenv("SLL_CA")

# # Obtain connection string information from the portal
# config = {
#     'host':f'{SERVER}.mysql.database.azure.com',
#     'user':f'{ADMIN}',
#     'password':f'{PWD}',
#     'database':f'{DB}',
#     'client_flags': [mysql.connector.ClientFlag.SSL],
#     'ssl_ca': f'{SLL_CA}'
# }

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

# リクエストボディの定義　パターン１
# class PurchaseHistory(BaseModel):
#     emp_cd: str
#     store_cd: str
#     pos_no: str
#     prd_id: str
#     prd_code: str
#     prd_name: str
#     prd_price: int

# リクエストボディの定義　パターン2
# class Product(BaseModel):
#     prd_id: str
#     prd_code: str
#     prd_name: str
#     prd_price: int
# class PurchaseHistory(BaseModel):
#     emp_cd: str
#     store_cd: str
#     pos_no: str
#     products: List[Product] # 複数の商品をリストで受け取る

# テスト用のAPI
@app.get("/")
def test():
    return {"Hello": "World"}

# 非同期処理にした方がよさそう。
# # 商品情報取得用のAPI
# @app.get("/get-products/{code}", summary="商品情報取得API")
# def read_items(code: str):
#     try:
#         conn = mysql.connector.connect(**config)
#         print("Connection established")
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with the user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)
#     # DBへ正常に接続できたときの処理
#     else:
#         cursor = conn.cursor()

#         # Read data
#         cursor.execute(f"SELECT PRD_ID, NAME, PRICE FROM m_product WHERE CODE={code};")
#         rows = cursor.fetchall()
#         print("Read", cursor.rowcount, "row(s) of data.")
        
#         # 商品マスタに商品があれば、商品一意コード,商品名商,商品単価を格納。ない場合はNullを返す
#         if len(rows) >= 1:
#             prd_id, name, price = rows[0]
#         else:
#             return None

#         # Cleanup
#         conn.commit()
#         cursor.close()
#         conn.close()
#         print("Done.")
        
#         return {"prd_id": prd_id, "code":code, "name": name, "price": price}

# # 購入履歴登録用のAPI
# @app.post("/post-histories", summary="購入履歴登録API")
# def add_histories(histories: List[PurchaseHistory]): # パターン１のリクエストボディにした場合
#     try:
#         conn = mysql.connector.connect(**config)
#         print("Connection established")
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with the user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)
#     # DBへ正常に接続できたときの処理
#     else:
#         dt_now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         cursor = conn.cursor()
#         # Insert some data into table.取引テーブルの行追加
#         cursor.execute(f"""INSERT INTO t_trd (DATETIME, TOTAL_AMT, TTL_AMT_EX_TAX) VALUES ("{dt_now}", 0, 0);""")
#         cursor.execute("SELECT LAST_INSERT_ID();")
#         trd_id = cursor.fetchone()[0]

#     #     # 取引明細テーブルへの登録 および 合計と税金額の計算
#         i = 1
#         v_sum_notax = 0
#         tax_rate = 0.1 # 消費税率 *本当は税マスタから取得する
#         for history in histories:
#             cursor.execute("""
#                            INSERT INTO t_trd_dtl (TRD_ID, DTL_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE, TAX_CD) VALUES (%s, %s, %s, %s, %s, %s, %s);
#                            """,
#                            (trd_id, i, history.prd_id, history.prd_code, history.prd_name, history.prd_price, "10"))
#             v_sum_notax += history.prd_price
#             i += 1
#         v_sum = int(v_sum_notax * (1+tax_rate))

#     #     # Update a data row in the table.取引テーブルの更新
#         cursor.execute("UPDATE t_trd SET TOTAL_AMT = %s, TTL_AMT_EX_TAX = %s WHERE TRD_ID = %s;", (v_sum,v_sum_notax, trd_id))
#         print("Updated",cursor.rowcount,"row(s) of data.")

#         # Cleanup
#         conn.commit()
#         cursor.close()
#         conn.close()
#         print("Done.")

#         return {"total_amt": v_sum, "total_amt_notax":v_sum_notax}