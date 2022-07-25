import mysql.connector
import numpy as np
import pandas as pd

con = mysql.connector.connect(host="localhost", user="masoud",password="m", database="Nikaro",auth_plugin='mysql_native_password')
cursor=con.cursor()

#                       USING LIMIT
query = "SELECT ut.id,ut.subject FROM `users_tracking_activity_log` as ut WHERE 1 LIMIT 10;"
cursor.execute(query)
table = cursor.fetchall()
print(type(table))
df = pd.DataFrame (table, columns = ['product_name','asd'])
print(df)


#                       PRINT NUMBER OF ROWS
# print(np.array(table).shape[0])
# table.gender.replace('-unknown-', np.nan, inplace=True)

#                       USE VARIABLE
# cursor.execute("SELECT last_name, first_name, hire_date "
#                "FROM employees WHERE emp_no = %s", (123,))

#                       PRINT ALL FETCH
#   PRINT COLUMN 1
# print(attr[1])

###################################################################

