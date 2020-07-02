import csv
import sqlite3
import os.path

db_file = '../app/site.db'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_file)

# insert into sqlite database

con = sqlite3.connect(db_path)
cur = con.cursor()

with open('mf_average_apr_rates.csv', 'r') as fin:  # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin)  # comma is default delimiter
    next(dr)
    # Nested lists, tuples are used for executemany, not for execute.
    to_db = [(i['Loan Term'], i['Loan Amount'], i['Loan Provider']
              , i['Loan Product'], i['Average APR'], i['Source'], i['Date Extracted']) for i in dr]

create_table_sql = """CREATE TABLE IF NOT EXISTS stg_mf_historical_apr_rates (
id INTEGER PRIMARY KEY NOT NULL ,
loan_term smallinteger,
loan_amount NUMERIC(18,0),
loan_provider varchar(255),
loan_product varchar(100),
average_apr_rate float,
source varchar(100),
date_extracted datetime
);
"""
cur.execute(create_table_sql)
cur.executemany("INSERT INTO main.stg_mf_historical_apr_rates (loan_term, loan_amount,	loan_provider"
                ", loan_product, average_apr_rate,	source, date_extracted) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
cur.execute("DELETE FROM lenders;")

lender_data = cur.execute('SELECT DISTINCT trim(loan_provider) as lender '
                          'FROM  stg_mf_historical_apr_rates order by trim(loan_provider);')

lender_list = [tuple(l) for l in lender_data]

cur.executemany("INSERT INTO lenders (lender) VALUES (?);", lender_list)

con.commit()
con.close()
