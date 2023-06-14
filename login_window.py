import tkinter
import student
import teacher
import manager

from utils import *

TEACHER = 0
STUDENT = 1
MANAGER = 2

class login:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("用户登录界面")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.user_label = tkinter.Label(self.root, text="用户名")
        self.user_entry = tkinter.Entry(self.root, width=15)
        self.pswd_label = tkinter.Label(self.root, text="密码")
        self.password_entry = tkinter.Entry(self.root, width=15, show='*')
        self.star_button = tkinter.Button(self.root, text="登陆", command=self.login)

        self.initialize()

    def initialize(self):
        self.user_label.grid(row=0, column=0)
        self.user_entry.grid(row=0, column=1)
        self.pswd_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)
        self.star_button.grid(row=2, column=1)

        self.user_entry.focus()

    def judge(self):
        login=self.user_entry.get()
        password=self.password_entry.get()
        if login.strip() == '' or password.strip() == '':
            return 3, ()
        db = connect()
        cursor = db.cursor()
        sql = "SELECT studentID FROM tb_student where studentID='%s' and studentPswd='%s'" % (login,password)
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result)!=0:
            return STUDENT, result[0][0]
        else:
            sql = "SELECT * FROM tb_teacher where teacherID='%s' and teacherPswd='%s'" % (login, password)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(type(result), result)
            if len(result)!=0:
                return TEACHER, result[0][0]
            else:
                sql = "SELECT managerID FROM tb_manager where managerID='%s' and managerPswd='%s'" % (login, password)
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result)!=0:
                    return MANAGER, result[0][0]
                else:
                    return MANAGER, result


    def login(self):
        type, result =self.judge()
        if len(result)!=0:
            self.root.destroy()
            if type == STUDENT:
                c=student.menu(result)
                c.start()
            elif type == TEACHER:
                t=teacher.menu(result)
                t.start()
            else:
                m=manager.menu(result)
                m.start()
        else:
            tkinter.Label(self.root, text="用户名或密码错误，请重新输入").grid(row=3, column=1)

    def start(self):
        self.root.mainloop()

if __name__ == '__main__':
    start = login()
    start.start()
