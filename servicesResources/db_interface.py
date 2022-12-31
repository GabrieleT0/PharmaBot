from datetime import datetime
import pyodbc
from PharmaBot.utility import util_func
from PharmaBot.user_info import UserInfo
SERVER = 'pharmabotserver.database.windows.net'
DATABASE = 'pharmaBotDB'
USERNAME = 'azureuser'
PASSWORD = 'pharmabotproject2022!'
DRIVER = '{ODBC Driver 18 for SQL Server}'
 
def insert_user(email,firstname,lastname,password):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO dbo.users([email],[password],[firstName],[lastName]) VALUES (?,?,?,?)",email,password,firstname,lastname)
                return True
    except:
        return False

def insert_medicine(email,name,type=None,grams=None,expirationDate=None):
    try:
        expirationDate = datetime.strptime(expirationDate,'%d/%m/%Y').date()
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO dbo.medicine([medicineName],[medicineType],[medicineGrams],[expirationDate],[email]) VALUES (?,?,?,?,?)",name,type,grams,expirationDate,email)
                
                return True
    except:

        return False

def get_pwd(email):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT password FROM dbo.users WHERE [email] = ?",email)
                row = cursor.fetchall()

                return row[0][0]
    except:
        return False

def login(email):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email,firstName,lastName FROM dbo.users WHERE [email] = ?",email)
            row = cursor.fetchall()
            email = row[0][0]
            firstName = row[0][1]
            lastName = row[0][2]
            cursor.execute("SELECT medicineName,medicineType,medicineGrams,expirationDate FROM dbo.medicine WHERE [email] = ?",email)
            rows = cursor.fetchall()
            medicineLi = []
            for row in rows:
                medicine = {}
                medicine['name'] = row[0]
                medicine['type'] = row[1]
                medicine['grams'] = row[2]
                medicine['expirationDate'] = row[3]
                medicineLi.append(medicine)
            user = UserInfo(email=email,firstName=firstName,lastName=lastName,medicine=medicineLi)
    
    return user

def delete_medicine(medicine_name,email):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM dbo.medicine WHERE [medicineName] = ? AND [email] = ?",medicine_name,email)
                return True
    except:
        return False

def check_medicine(medicine_name,email):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM dbo.medicine WHERE [medicineName] = ? AND [email] = ?",medicine_name,email)
                rows = cursor.fetchall()
                medicineLi = []
                for row in rows:
                    medicine = {}
                    medicine['name'] = row[0]
                    medicine['type'] = row[1]
                    medicine['grams'] = row[2]
                    medicine['expirationDate'] = row[3]
                    medicineLi.append(medicine)
                return medicineLi
    except:
        return False


def get_all_medicine(email):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT medicineName,medicineType,medicineGrams,expirationDate FROM dbo.medicine WHERE [email] = ?",email)
            rows = cursor.fetchall()
            medicineLi = []
            for row in rows:
                medicine = {}
                medicine['name'] = row[0]
                medicine['type'] = row[1]
                medicine['grams'] = row[2]
                medicine['expirationDate'] = row[3]
                medicineLi.append(medicine)

            return medicineLi


'''
insert_medicine('gabrieletuozzo@gmail.com','tachipirina',type='pillola',grams='500gr.',expirationDate='2023-02-01')
pwd = util_func.get_hashed_pwd('pharrmabotproject2022!')
insert_user('gabrieletuozzo@gmail.com','Gabriele','Tuozzo',pwd)

pwd_data = 'pharrmabotproject2022!'
user = login('gabrieletuozzo@gmail.com')
delete_medicine('tachipirina','gabrieletuozzo@gmail.com')

# print(util_func.check_pwd(pwd_data,pwd.encode('utf-8')))
'''