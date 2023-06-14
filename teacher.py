import tkinter
from tkinter import ttk
import pymysql
from utils import *

RADIO = 0.1
WINDOW_SIZE = '800x500+200+100'
TEXT_INDENT = 60
TEXT_LINE_SPACE = 30

# 个人信息区域
class menu:
    def __init__(self, teacherID):
        self.studentNum = teacherID
        self.root = tkinter.Tk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title('教师')
        self.root.resizable(False, False)
        # 子区域
        self.info = tkinter.Frame(self.root)
        self.course = tkinter.Frame(self.root)
        self.grade = tkinter.Frame(self.root)
        self.input = tkinter.Frame(self.root)
        # 菜单栏
        self.menu = tkinter.Frame(self.root)
        self.tc_info = tkinter.Button(self.menu, text='个人信息', command=self.tea_info)
        self.tc_grade = tkinter.Button(self.menu, text='课程成绩', command=self.tea_grade)
        # 控件布局
        self.initialize()

    def initialize(self):
        self.menu.place(relheight=1, relwidth=RADIO)
        self.tc_info.place(rely=0.0, relheight=0.5, relwidth=1)
        self.tc_grade.place(rely=0.5, relheight=0.5, relwidth=1)

    def tea_info(self):
        self.course.place_forget()
        self.grade.place_forget()
        self.input.place_forget()
        tcInfo(self.info, self.studentNum)

    def tea_grade(self):
        self.course.place_forget()
        self.info.place_forget()
        self.input.place_forget()
        tcGrade(self.grade, self.studentNum)

    def start(self):
        self.root.mainloop()

# 个人信息区域
class tcInfo:
    def __init__(self, frame, teacherID):
        self.teacherID = teacherID
        self.frame = frame
        # 个人信息
        self.numLabel = tkinter.Label(self.frame, text='学号：')
        self.nameLabel = tkinter.Label(self.frame, text='姓名：')
        self.sexLabel = tkinter.Label(self.frame, text='性别：')
        self.pswdLabel = tkinter.Label(self.frame, text='密码：')
        # 个人信息显示
        self.num_Label = tkinter.Label(self.frame)
        self.name_Label = tkinter.Label(self.frame)
        self.sex_Label = tkinter.Label(self.frame)
        self.pswdVar = tkinter.StringVar()
        self.pswd_Entry = tkinter.Entry(self.frame, textvariable=self.pswdVar)
        # 修改密码
        self.commitButton = tkinter.Button(self.frame, text='修改密码')
        # 规则提示，修改密码提示信息是同一个标签
        self.promptLabel = tkinter.Label(self.frame, text='密码不少于6位, 不能与原密码相同', font=("TkDefaultFont", 8))
        # 控件布局
        self.initialize()

    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1-RADIO)
        # 放置不变的组件
        self.numLabel.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 0, anchor='ne')
        self.nameLabel.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 1, anchor='ne')
        self.sexLabel.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 2, anchor='ne')
        self.pswdLabel.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 3, anchor='ne')
        # 获取信息
        info = self.get_teacher_info(self.teacherID)[0]
        # 设置要显示的信息，及修改密码的函数
        self.num_Label.configure(text=info[0])
        self.name_Label.configure(text=info[1])
        self.sex_Label.configure(text=info[2])
        self.pswd_Entry.insert(tkinter.INSERT, info[3])
        self.commitButton.configure(command=lambda :self.change_pswd(info[3], self.pswd_Entry.get()))
        # 放置组件，显示信息
        self.num_Label.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 0)
        self.name_Label.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 1)
        self.sex_Label.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 2)
        self.pswd_Entry.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 3)
        # 放置修改密码按钮，和密码提示
        self.frame.update()
        self.promptLabel.place(x=self.pswd_Entry.winfo_x(), y=self.pswd_Entry.winfo_y() + self.pswd_Entry.winfo_height() + 5)
        self.commitButton.place(x=self.pswd_Entry.winfo_x() + self.pswd_Entry.winfo_width() + 5, y=self.pswd_Entry.winfo_y() - 5)

    def change_pswd(self, origPswd, pswd):
        pswd = pswd.strip()
        if pswd == origPswd:
            self.promptLabel.configure(text='密码不能与原密码相同！')
            return
        elif len(pswd) < 6:
            self.promptLabel.configure(text='密码不能小于六位！')
            return
        else:
            self.promptLabel.configure(text='密码修改成功！')
        self.set_teacher_pswd(pswd)
        return


    def get_teacher_info(self, teacherID):
        db = connect()
        cursor = db.cursor()
        sql = f'select distinct * from tb_teacher where teacherID = \'{teacherID}\''
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    def set_teacher_pswd(self, pswd):
        db = connect()
        cursor = db.cursor()
        sql = f'UPDATE tb_teacher SET studentPswd= \'{pswd}\' WHERE teacherID = \'{self.teacherID}\''
        cursor.execute(sql)
        try:
            db.commit()
        except:
            db.rollback()
        db.close()

# 课程成绩区域
class tcGrade:
    def __init__(self, frame, teacherID):
        self.teacherID = teacherID
        self.frame = frame
        # 信息放置处
        self.courseTable = ttk.Treeview(self.frame,
                                        height=10,
                                        columns=['课程号', '课程名', '课序号', '学分', '人数'],
                                        show='headings')
        

        self.studentTable = ttk.Treeview(self.frame,
                                        height=10,
                                        columns=[1, 2, 3],
                                        show='headings')

        # 提示信息
        self.promptLabel = tkinter.Label(self.frame, text='点击列表中的课程，查看成绩')
        self.gradeEntry = tkinter.Entry(self.frame)
        self.enterButton = tkinter.Button(self.frame, text='修改成绩', command=self.inputGrade)
        # 选中的课程
        self.selectedCourse = None
        self.selectedStudent = None

        self.initialize()

    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1-RADIO)
        # 放置组件
        self.frame.update()
        self.courseTable.place(height=self.frame.winfo_height(),
                               relwidth=0.6)

        self.studentTable.place(relx=0.6, relheight=0.8,
                               relwidth=0.4)
        self.frame.update()
        self.promptLabel.place(x=self.courseTable.winfo_x() + self.courseTable.winfo_width() + 5,
                               y=self.courseTable.winfo_y() + self.courseTable.winfo_height(), anchor='sw')

        self.gradeEntry.place(x=self.courseTable.winfo_x() + self.courseTable.winfo_width() + 5,
                               y=self.courseTable.winfo_y() + self.courseTable.winfo_height() - 60, anchor='sw')

        self.enterButton.place(x=self.courseTable.winfo_x() + self.courseTable.winfo_width() + 5,
                               y=self.courseTable.winfo_y() + self.courseTable.winfo_height() - 30, anchor='sw')

        self.displayInfo()

        self.studentTable.heading(1, text='姓名', anchor='w')
        self.studentTable.heading(2, text='学号')
        self.studentTable.heading(3, text='成绩')

        self.studentTable.column(1, width=00)
        self.studentTable.column(2, width=50)
        self.studentTable.column(3, width=50)

    # 显示教授课程信息
    # 只显示已有同学选择的课程
    def displayInfo(self):
        self.clear_table([self.studentTable, self.courseTable])
        self.selectedStudent = None

        self.courseTable.heading('课程号', text='课程号', anchor='w')
        self.courseTable.heading('课程名', text='课程名')
        self.courseTable.heading('课序号', text='课序号')
        self.courseTable.heading('学分', text='学分')
        self.courseTable.heading('人数', text='人数')

        self.courseTable.column('课程号', width=100, minwidth=100)
        self.courseTable.column('课程名', width=150, minwidth=150)
        self.courseTable.column('课序号', width=50, minwidth=50)
        self.courseTable.column('学分', width=50, minwidth=50)
        self.courseTable.column('人数', width=50, minwidth=50)

        info = self.get_class_teached()
        for x in info:
            self.courseTable.insert('', tkinter.END, values=x)

        self.courseTable.bind('<ButtonRelease-1>', self.click_course)
        

    def displayStu(self):
        self.clear_table([self.studentTable])
        info = self.get_class_student(self.selectedCourse['values'][0], self.selectedCourse['values'][2])
        for x in info:
            self.studentTable.insert('', tkinter.END, values=x)

        self.studentTable.bind('<ButtonRelease-1>', self.get_selected_student)

    def click_course(self, event):
        self.selectedStudent = None
        self.get_selected_course(event)
        self.displayStu()


    def inputGrade(self):
        # studentID, courseID, courseNum, grade
        if self.selectedCourse == None:
            self.promptLabel.configure(text='请选择课程')
        elif self.selectedStudent == None:
            self.promptLabel.configure(text='请选择学生')
        else:
            studentID, courseID, courseNum, grade = self.selectedStudent['values'][0], self.selectedCourse['values'][0], \
                                                    self.selectedCourse['values'][2], self.gradeEntry.get()
            if self.set_student_grade(studentID, courseID, courseNum, grade) == 0:
                self.promptLabel.configure(text='成绩录入成功')
                self.displayStu()
            else:
                self.promptLabel.configure(text='成绩录入失败')


    # 获得表中选中课程
    def get_selected_course(self, event):
        curItem = self.courseTable.focus()
        self.selectedCourse = self.courseTable.item(curItem)
        print(self.selectedCourse)

    # 获得表中选中课程
    def get_selected_student(self, event):
        curItem = self.studentTable.focus()
        self.selectedStudent = self.studentTable.item(curItem)
        print(self.selectedStudent)

    # 获取
    def get_class_teached(self):
        db = connect()
        cursor = db.cursor()
        sql = f'select C.courseID, C.courseName, C.courseNum, C.courseCredit, count(distinct SC.studentID) ' \
              f'from tb_course as C, tb_teacher_course as TC, tb_student_course as SC ' \
              f'where TC.teacherID = \'{self.teacherID}\' and TC.courseID = C.courseID '\
              f'and TC.courseNum = C.courseNum and SC.courseID = C.courseID and SC.courseNum = C.courseNum ' \
              f'group by SC.courseID, SC.courseNum'
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result
    
    def get_class_student(self, courseID, courseNum):
        db = connect()
        cursor = db.cursor()
        sql = f'select distinct s.studentID, s.studentName, sc.grade ' \
              f'from tb_student as s, tb_student_course as sc ' \
              f'where s.studentID = sc.studentID and courseID = \'{courseID}\' and courseNum = {courseNum} '
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    def set_student_grade(self, studentID, courseID, courseNum, grade):
        db = connect()
        cursor = db.cursor()
        print(studentID, courseID, courseNum, grade)
        sql = f'update tb_student_course ' \
              f'set grade = {grade} ' \
              f'where studentID = \'{studentID}\' and courseID = \'{courseID}\'and courseNum = {courseNum}'
        cursor.execute(sql)
        try:
            db.commit()
            db.close()
            return 0
        except:
            db.rollback()
            db.close()
            return 1


    def clear_table(self, tables):
        for table in tables:
            for x in table.get_children():
                table.delete(x)

if __name__ == '__main__':
    c = menu('200407')
    c.start()