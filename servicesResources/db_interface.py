from datetime import datetime
import pyodbc
from utility import util_func
from user_info import UserInfo

SERVER = 'pharmabotdb.database.windows.net'
DATABASE = 'pharmaBotDB'
USERNAME = 'azureuser'
PASSWORD = 'pharmabotproject2022!'
DRIVER = '{ODBC Driver 18 for SQL Server}'
#DRIVER = '{FreeTDS}'
 
def insert_user(email,firstname,lastname,password):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO dbo.users([email],[pwd],[firstName],[lastName]) VALUES (?,?,?,?)",email,password,firstname,lastname)
            return True

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
                cursor.execute("SELECT pwd FROM dbo.users WHERE [email] = ?",email)
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

def update_medicine(medicine_name,field_to_update,new_value,email):
    try:
        if field_to_update == 'expirationDate':
            new_value = datetime.strptime(new_value,'%d/%m/%Y').date()
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"UPDATE dbo.medicine SET [{field_to_update}] = ? WHERE [medicineName] = ? AND [email] = ?",new_value,medicine_name,email)
                return True
    except Exception as error:
        print(error)


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

def insert_reminder_info(conversation_id,reminder_text):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO dbo.reminders([conversationID],[reminderText]) VALUES (?,?)",conversation_id,reminder_text)
                
                return True
    except:

        return False

def get_str_reminder(conversation_id):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT reminderText,ID FROM dbo.reminders WHERE [conversationID] = ?",conversation_id)
                rows = cursor.fetchall()
                messages = []
                for row in rows:
                    messages.append((row[0],row[1]))
                
                return messages
    except:
        return False

def delete_reminder(id_reminder):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM dbo.reminders WHERE [ID] = ?",id_reminder)
                return True
    except:
        return False

def delete_account(email):
    try:
        with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM dbo.medicine WHERE [email] = ?",email)
                cursor.execute("DELETE FROM dbo.users WHERE [email] = ?",email)
                return True
    except Exception as e:
        return False

'''
r = update_medicine('Tachipirina','medicineGrams','2000gr.','gabrieletuozzo@gmail.com')
print(r)
'''
'''
insert_medicine('gabrieletuozzo@gmail.com','tachipirina',type='pillola',grams='500gr.',expirationDate='2023-02-01')
pwd = util_func.get_hashed_pwd('pharrmabotproject2022!')
insert_user('gabrieletuozzo@gmail.com','Gabriele','Tuozzo',pwd)

pwd_data = 'pharrmabotproject2022!'
user = login('gabrieletuozzo@gmail.com')
delete_medicine('tachipirina','gabrieletuozzo@gmail.com')

# print(util_func.check_pwd(pwd_data,pwd.encode('utf-8')))
'''

''''
r = get_str_reminder('632fdc28-b260-4313-b2f5-d630ed9eab8f')
print(r)
'''