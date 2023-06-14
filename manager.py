import tkinter
from tkinter import ttk
from utils import *
import pymysql

RADIO = 0.1
WINDOW_SIZE = '800x500+200+100'
INFO_TEXT_INDENT = 60
INFO_TEXT_LINE_SPACE = 30
STUDENT = 0
TEACHER = 1

class menu:
    def __init__(self, managerNum):
        self.managerNum = managerNum
        self.root = tkinter.Tk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title('管理员')
        self.root.resizable(False, False)
        # 子区域
        self.query = tkinter.Frame(self.root)
        self.new = tkinter.Frame(self.root)
        self.course = tkinter.Frame(self.root)
        # 菜单栏
        self.menu = tkinter.Frame(self.root)
        self.mgr_query = tkinter.Button(self.menu, text='账号查询', command=self.mgr_query)
        self.mgr_new = tkinter.Button(self.menu, text='新建账号', command=self.mgr_new)
        self.mgr_course = tkinter.Button(self.menu, text='安排课程', command=self.mgr_course)
        # 控件布局
        self.initialize()

    def initialize(self):
        self.menu.place(relheight=1, relwidth=RADIO)
        self.mgr_query.place(rely=0.0, relheight=1/3, relwidth=1)
        self.mgr_new.place(rely=1/3, relheight=1/3, relwidth=1)
        self.mgr_course.place(rely=2/3, relheight=1/3, relwidth=1)

    def mgr_query(self):
        self.new.place_forget()
        self.course.place_forget()
        mgrQuery(self.query, self.managerNum)

    def mgr_new(self):
        self.query.place_forget()
        self.course.place_forget()
        mgrNew(self.new, self.managerNum)

    def mgr_course(self):
        self.new.place_forget()
        self.query.place_forget()
        mgrCourse(self.course)

    def start(self):
        self.root.mainloop()


# 账号查询区域
class mgrQuery:
    def __init__(self, frame, managerNum):
        self.manager = managerNum
        self.frame = frame
        # 选择的表项
        self.selected = None
        # 选择的是学生还是教师
        self.type = TEACHER

        self.queryFrame = tkinter.Frame(self.frame)

        self.numLabel = tkinter.Label(self.frame, text='学(工)号：')
        self.nameLabel = tkinter.Label(self.frame, text='姓名：')

        self.num_Entry = tkinter.Entry(self.frame, text='学(工)号：')
        self.name_Entry = tkinter.Entry(self.frame)

        self.queryButton = tkinter.Button(self.frame, text='查询', command=self.queryInfo)
        # 提示信息
        self.promptLabel = tkinter.Label(self.frame, text='输入一项或输入两项，不能为空')

        self.infoScrollbar = tkinter.Scrollbar(self.frame)
        self.infoTable = ttk.Treeview(self.frame,
                                        height=10,
                                        columns=['姓名', '学号', '性别'],
                                        show='headings',
                                        yscrollcommand=self.infoScrollbar.set)
        # 显示查询到的账号信息
        self.infoScrollbar = tkinter.Scrollbar(self.frame)
        self.infoTable = ttk.Treeview(self.frame,
                                      height=10,
                                      columns=[1, 2, 3, 4],
                                      show='headings',
                                      yscrollcommand=self.infoScrollbar.set)

        self.infoTable.heading(1, text='姓名')
        self.infoTable.heading(2, text='学(工)号')
        self.infoTable.heading(3, text='性别')
        self.infoTable.heading(4, text='教师/学生')

        self.infoTable.column(1, width=50, anchor='s')
        self.infoTable.column(2, width=50, anchor='s')
        self.infoTable.column(3, width=50, anchor='s')
        self.infoTable.column(4, width=50, anchor='s')

        # 显示学生（老师）选择的（教授）的课
        self.courseScrollbar = tkinter.Scrollbar(self.frame)
        self.courseTable = ttk.Treeview(master=self.frame,
                                        height=10,
                                        columns=[1, 2, 3, 4],
                                        show='headings',
                                        yscrollcommand=self.courseScrollbar.set)

        self.courseTable.heading(1, text='课程号')
        self.courseTable.heading(2, text='课程名')
        self.courseTable.heading(3, text='课序号')
        self.courseTable.heading(4, text='学分')

        self.courseTable.column(1, width=50, anchor='s')
        self.courseTable.column(2, width=75, anchor='s')
        self.courseTable.column(3, width=50, anchor='s')
        self.courseTable.column(4, width=50, anchor='s')

        # 控件布局
        self.initialize()

    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1-RADIO)

        self.frame.update()
        self.numLabel.place(x=0, y=0)
        self.frame.update()
        self.num_Entry.place(x=self.numLabel.winfo_x() + self.numLabel.winfo_width(), y=0)

        self.frame.update()
        self.nameLabel.place(x=self.num_Entry.winfo_x() + self.num_Entry.winfo_width() + 5, y=0)
        self.frame.update()
        self.name_Entry.place(x=self.nameLabel.winfo_x() + self.nameLabel.winfo_width(), y=0)

        self.frame.update()
        self.queryButton.place(x=self.name_Entry.winfo_x() + self.name_Entry.winfo_width(), y=0)

        self.frame.update()
        self.promptLabel.place(x=self.queryButton.winfo_x() + self.queryButton.winfo_width(), y=0)

        # 放置信息框
        self.frame.update()
        self.infoTable.place(y=self.numLabel.winfo_y() + self.numLabel.winfo_height() + 10,
                             relheight=0.9,
                             relwidth=0.5)

        self.frame.update()
        self.courseTable.place(y=self.infoTable.winfo_y(),
                               x=self.infoTable.winfo_width(),
                               relheight=0.9,
                               relwidth=0.5)


    def queryInfo(self):
        if len(self.num_Entry.get()) == 0 and len(self.name_Entry.get()) == 0:
            self.promptLabel.configure(text='至少一项不为空！！')
            return
        else:
            if len(self.num_Entry.get()) == 0:
                self.displayInfo(name=self.name_Entry.get())
            elif len(self.name_Entry.get()) == 0:
                self.displayInfo(ID=self.num_Entry.get())
            else:
                self.displayInfo(name=self.name_Entry.get(), ID=self.num_Entry.get())


    def displayInfo(self, ID=None, name=None):
        self.clear_table_info([self.infoTable, self.courseTable])

        info = self.get_acc_info(ID, name)
        if len(info) != 0:
            self.promptLabel.configure(text='查询成功')
        else:
            self.promptLabel.configure(text='未查询到记录')

        for x in info:
            self.infoTable.insert('', tkinter.END, values=x)

        self.infoTable.bind('<ButtonRelease-1>', self.click_acc)

    # 显示课程
    def displayCourse(self):
        self.clear_table_info([self.courseTable])

        info = self.selected['values']
        info = self.get_acc_course(info[1], info[3])

        for x in info:
            self.courseTable.insert('', tkinter.END, values=x)

    # 点击账号
    def click_acc(self, event):
        self.get_selected_acc(event)
        self.displayCourse()


    # 查询账号信息，以及学生0/教师1
    def get_acc_info(self, ID=None, name=None):
        if ID == None and name == None:
            return None
        else:
            if ID == None:
                sql1 = f'select teacherName, teacherID, teacherSex ' \
                       f'from tb_teacher ' \
                       f'where teacherName like \'%{name}%\''
                sql2 = f'select studentName, studentID, studentSex ' \
                       f'from tb_student ' \
                       f'where studentName like \'%{name}%\''
            elif name == None:
                sql1 = f'select teacherName, teacherID, teacherSex ' \
                       f'from tb_teacher ' \
                       f'where teacherID = \'{ID}\''
                sql2 = f'select studentName, studentID, studentSex ' \
                       f'from tb_student ' \
                       f'where studentID = \'{ID}\''
            else:
                sql1 = f'select teacherName, teacherID, teacherSex ' \
                       f'from tb_teacher ' \
                       f'where teacherName like \'%{name}%\' and teacherID = \'{ID}\''
                sql2 = f'select studentName, studentID, studentSex ' \
                       f'from tb_student ' \
                       f'where studentName like \'%{name}%\' and studentID = \'{ID}\''

            db = connect()
            cursor = db.cursor()
            # 先查教师再查学生
            cursor.execute(sql1)
            result = cursor.fetchall()
            res = []
            if len(result) != 0:
                for x in result:
                    res.append((x[0], x[1], x[2], '教师'))

            cursor.execute(sql2)
            result = cursor.fetchall()
            if len(result) != 0:
                for x in result:
                    res.append((x[0], x[1], x[2], '学生'))

            db.close()
            return res

    # 查询账号(老师/学生)对应课程
    def get_acc_course(self, ID, type):
        if type == '学生':
            sql = f'select c.courseID, c.courseName, c.courseNum, c.courseCredit ' \
                  f'from tb_course as c, tb_student_course as sc ' \
                  f'where c.courseID = sc.courseID and c.courseNum = sc.courseNum and sc.studentID = \'{ID}\''
        else:
            sql = f'select c.courseID, c.courseName, c.courseNum, c.courseCredit ' \
                  f'from tb_course as c, tb_teacher_course as tc ' \
                  f'where c.courseID = tc.courseID and c.courseNum = tc.courseNum and tc.teacherID = \'{ID}\''

        db = connect()
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    def get_selected_acc(self, event):
        curItem = self.infoTable.focus()
        self.selected = self.infoTable.item(curItem)


    def clear_table_info(self, tables):
        for table in tables:
            for x in table.get_children():
                table.delete(x)


class mgrNew:
    def __init__(self, frame, managerNum):
        self.manager = managerNum
        self.frame = frame

        self.nameLabel = tkinter.Label(self.frame, text='姓名：')
        self.idLabel = tkinter.Label(self.frame, text='学(工)号：')
        self.sexLabel = tkinter.Label(self.frame, text='性别：')
        self.pswdLabel = tkinter.Label(self.frame, text='密码：')
        self.ageLabel = tkinter.Label(self.frame, text='年龄：')

        self.nameEntry = tkinter.Entry(self.frame)
        self.idEntry = tkinter.Entry(self.frame)
        self.sexEntry = tkinter.Entry(self.frame)
        self.pswdEntry = tkinter.Entry(self.frame)
        self.ageEntry = tkinter.Entry(self.frame)

        self.var = tkinter.IntVar()
        self.tcButton = tkinter.Radiobutton(self.frame, text='教师', variable=self.var, value=1)
        self.stuButton = tkinter.Radiobutton(self.frame, text='学生', variable=self.var, value=2)

        self.enterButton = tkinter.Button(self.frame, text='创建账号', command=self.createAccount)
        self.promptLabel = tkinter.Label(self.frame, text='教师可以不用输入年龄')

        self.initialize()

    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1-RADIO)

        self.nameLabel.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 0, anchor='ne')
        self.idLabel.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE *1, anchor='ne')
        self.sexLabel.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 2, anchor='ne')
        self.pswdLabel.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 3, anchor='ne')
        self.ageLabel.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 4, anchor='ne')

        self.nameEntry.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 0)
        self.idEntry.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 1)
        self.sexEntry.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 2)
        self.pswdEntry.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 3)
        self.ageEntry.place(x=INFO_TEXT_INDENT, y=INFO_TEXT_LINE_SPACE * 4)

        self.tcButton.place(x=10, y=INFO_TEXT_LINE_SPACE * 5)
        self.tcButton.select()
        self.frame.update()
        self.stuButton.place(x=self.tcButton.winfo_width() + 10, y=INFO_TEXT_LINE_SPACE * 5)

        self.enterButton.place(x=self.ageEntry.winfo_x() + self.ageEntry.winfo_width() + 10, y=INFO_TEXT_LINE_SPACE * 4)

        self.promptLabel.place(x=15, y=INFO_TEXT_LINE_SPACE * 6)



    def createAccount(self):
        name, id, sex, pswd, age = \
            self.nameEntry.get(), self.idEntry.get(), self.sexEntry.get(), self.pswdEntry.get(), self.ageEntry.get()
        if self.var.get() == 1:
            if len(name)!=0 and len(id)!=0 and len(sex)!=0 and len(pswd)!=0:
                if self.insert_teacher_account(name, id, sex, pswd) == 0:
                    self.promptLabel.configure(text='教师账号创建成功')
                else:
                    self.promptLabel.configure(text='教师账号创建失败')

            else:
                self.promptLabel.configure(text='教师年龄不用输入，请确认信息输入完全')
        else:
            if len(name) != 0 and len(id) != 0 and len(sex) != 0 and len(pswd) != 0 and len(age) != 0:
                if self.insert_student_account(name, id, sex, pswd, age) == 0:
                    self.promptLabel.configure(text='学生账号创建成功')
                else:
                    self.promptLabel.configure(text='学生账号创建失败')
            else:
                self.promptLabel.configure(text='请确认信息输入完全')

    def insert_teacher_account(self, name, id, sex, pswd):
        db = connect()
        cursor = db.cursor()
        sql = f'INSERT INTO tb_teacher(teacherID, teacherName, teacherSex, teacherPswd)' \
              f'VALUES(\'{id}\', \'{name}\', \'{sex}\', \'{pswd}\') '
        try:
            cursor.execute(sql)
        except:
            return 1
        try:
            db.commit()
            db.close()
            return 0
        except:
            db.rollback()
            db.close()
            return 1

    def insert_student_account(self, name, id, sex, pswd, age):
        db = connect()
        cursor = db.cursor()
        sql = f'INSERT INTO tb_student(studentID, studentName, studentSex, studentPswd, studentAge)' \
              f'VALUES(\'{id}\', \'{name}\', \'{sex}\', \'{pswd}\', {age}) '
        try:
            cursor.execute(sql)
        except:
            return 1
        try:
            db.commit()
            db.close()
            return 0
        except:
            db.rollback()
            db.close()
            return 1


class mgrCourse:
    def __init__(self, frame):
        self.frame = frame
        # 信息放置处, 滚动条
        self.courseScrollbar = tkinter.Scrollbar(self.frame)
        self.courseTable = ttk.Treeview(self.frame,
                                        height=10,
                                        columns=['课程号', '课程名', '课序号', '学分'],
                                        show='headings',
                                        yscrollcommand=self.courseScrollbar.set)
        self.teacherScrollbar = tkinter.Scrollbar(self.frame)
        self.teacherTable = ttk.Treeview(self.frame,
                                         height=10,
                                         columns=['工号', '姓名'],
                                         show='headings',
                                         yscrollcommand=self.teacherScrollbar.set)
        # 确认排课按钮
        self.comfirmButton = tkinter.Button(self.frame, text='确认排课', command=self.comfirmCourse)
        # 提示信息
        self.promptLabel = tkinter.Label(self.frame, text='请同时选上课程信息和老师信息')
        # 选中的课程
        self.selected_course = None
        # 选中的老师
        self.selected_teacher = None

        self.initialize()

    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1 - RADIO)
        # 放置组件
        self.frame.update()
        self.frame.update()
        self.courseTable.place(height=self.frame.winfo_height(),
                               relwidth=0.39)
        self.frame.update()
        self.teacherTable.place(relx=0.4, height=self.frame.winfo_height(),
                                relwidth=0.3)
        self.frame.update()
        self.promptLabel.place(x=self.teacherTable.winfo_x() + self.teacherTable.winfo_width() + 5,
                               y=self.teacherTable.winfo_y() + self.teacherTable.winfo_height(), anchor='sw')
        self.comfirmButton.place(x=self.teacherTable.winfo_x() + self.teacherTable.winfo_width() + 5,
                                 y=self.teacherTable.winfo_y() + self.teacherTable.winfo_height() - 30, anchor='sw')

        self.displayInfo()

    def displayInfo(self):
        self.clear_course_info()
        self.courseTable.heading('课程号', text='课程号', anchor='w')
        self.courseTable.heading('课程名', text='课程名')
        self.courseTable.heading('课序号', text='课序号')
        self.courseTable.heading('学分', text='学分')

        self.courseTable.column('课程号', width=60, minwidth=60)
        self.courseTable.column('课程名', width=100, minwidth=100)
        self.courseTable.column('课序号', width=30, minwidth=30)
        self.courseTable.column('学分', width=30, minwidth=30)

        self.teacherTable.heading('工号', text='工号')
        self.teacherTable.heading('姓名', text='姓名')

        self.teacherTable.column('工号', width=100, minwidth=100)
        self.teacherTable.column('姓名', width=100, minwidth=100)

        info_valid_course = self.get_class_optional()
        for x in info_valid_course:
            self.courseTable.insert('', tkinter.END, values=x)

        info_valid_teacher = self.get_teacher_optional()
        for y in info_valid_teacher:
            self.teacherTable.insert('', tkinter.END, values=y)

        self.courseTable.bind('<ButtonRelease-1>', self.get_selected_courseItem)
        self.teacherTable.bind('<ButtonRelease-1>', self.get_selected_teacherItem)

    # 确认排课按钮
    def comfirmCourse(self):
        if self.selected_course is None:
            self.promptLabel.configure(text='还未选择课程!')
        elif self.selected_teacher is None:
            self.promptLabel.configure(text='还未选择老师!')
        else:
            if self.insert_teacher_course(self.selected_teacher['values'][0], self.selected_course['values'][0],
                                          self.selected_course['values'][2]) == 0:
                self.promptLabel.configure(text='排课成功!')
            else:
                self.promptLabel.configure(text='排课失败!')
        # 更新列表
        self.displayInfo()

    # 获得选中课程信息
    def get_selected_courseItem(self, event):
        curItem = self.courseTable.focus()
        self.selected_course = self.courseTable.item(curItem)
        # print(self.selected_course)

    # 获得课程信息
    def get_class_optional(self):
        db = connect()
        cursor = db.cursor()
        sql = f'select courseID, courseName, courseNum, courseCredit from tb_course ' \
              f'where (courseID, courseNum) not in (select courseID, courseNum from tb_teacher_course) '
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    # 获得选中老师信息
    def get_selected_teacherItem(self, event):
        curItem = self.teacherTable.focus()
        self.selected_teacher = self.teacherTable.item(curItem)
        # print(self.selected_teacher)

    # 获得老师信息
    def get_teacher_optional(self):
        db = connect()
        cursor = db.cursor()
        sql = f'select teacherID, teacherName from tb_teacher '
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    # 排课信息提交
    def insert_teacher_course(self, teacherID, courseID, courseNum):
        db = connect()
        cursor = db.cursor()
        sql = f'INSERT INTO tb_teacher_course (teacherID, courseID, courseNum) VALUES (\'{teacherID}\', \'{courseID}\', \'{courseNum}\')'
        cursor.execute(sql)
        try:
            db.commit()
            db.close()
            return 0
        except:
            db.rollback()
            db.close()
            return 1

    # 课程、老师信息清除
    def clear_course_info(self):
        for x in self.courseTable.get_children():
            self.courseTable.delete(x)
        for y in self.teacherTable.get_children():
            self.teacherTable.delete(y)


if __name__ == '__main__':
    c = menu('C1')
    c.start()