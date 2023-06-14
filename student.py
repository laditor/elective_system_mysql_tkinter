import tkinter
from tkinter import ttk
import pymysql
from utils import *

RADIO = 0.1
WINDOW_SIZE = '800x500+200+100'
TEXT_INDENT = 60
TEXT_LINE_SPACE = 30

class menu:
    def __init__(self, StudentNum):
        self.studentNum = StudentNum
        self.root = tkinter.Tk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title('学生')
        self.root.resizable(False, False)
        # 子区域
        self.info = tkinter.Frame(self.root)
        self.choose = tkinter.Frame(self.root)
        self.drop = tkinter.Frame(self.root)
        self.grade = tkinter.Frame(self.root)
        # 菜单栏
        self.menu = tkinter.Frame(self.root)
        self.stu_info = tkinter.Button(self.menu, text='个人信息', command=self.stu_info)
        self.stu_choose = tkinter.Button(self.menu, text='选课', command=self.stu_choose)
        self.stu_drop = tkinter.Button(self.menu, text='退课', command=self.stu_drop)
        self.stu_grade = tkinter.Button(self.menu, text='课程成绩', command=self.stu_grade)
        # 控件布局
        self.initialize()

    def initialize(self):
        self.menu.place(relheight=1, relwidth=RADIO)
        self.stu_info.place(rely=0.0, relheight=0.25, relwidth=1)
        self.stu_choose.place(rely=0.25, relheight=0.25, relwidth=1)
        self.stu_drop.place(rely=0.5, relheight=0.25, relwidth=1)
        self.stu_grade.place(rely=0.75, relheight=0.25, relwidth=1)

    def stu_info(self):
        self.info.place_forget()
        self.choose.place_forget()
        self.drop.place_forget()
        self.grade.place_forget()
        stuInfo(self.info, self.studentNum)

    def stu_choose(self):
        self.info.place_forget()
        self.choose.place_forget()
        self.drop.place_forget()
        self.grade.place_forget()
        stuChoose(self.choose, self.studentNum)

    def stu_drop(self):
        self.info.place_forget()
        self.choose.place_forget()
        self.drop.place_forget()
        self.grade.place_forget()
        stuDrop(self.drop, self.studentNum)

    def stu_grade(self):
        self.info.place_forget()
        self.choose.place_forget()
        self.drop.place_forget()
        self.grade.place_forget()
        stuGrade(self.grade, self.studentNum)

    # 启动窗口
    def start(self):
        self.root.mainloop()

# 个人信息区域
class stuInfo:
    def __init__(self, frame, studentNum):
        self.frame = frame
        self.studentNum = studentNum
        # 个人信息
        self.numLabel = tkinter.Label(self.frame, text='学号：')
        self.nameLabel = tkinter.Label(self.frame, text='姓名：')
        self.sexLabel = tkinter.Label(self.frame, text='性别：')
        self.ageLabel = tkinter.Label(self.frame, text='年龄：')
        self.pswdLabel = tkinter.Label(self.frame, text='密码：')
        # 个人信息显示
        self.num_Label = tkinter.Label(self.frame)
        self.name_Label = tkinter.Label(self.frame)
        self.sex_Label = tkinter.Label(self.frame)
        self.age_Label = tkinter.Label(self.frame)
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
        self.ageLabel.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 3, anchor='ne')
        self.pswdLabel.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 4, anchor='ne')
        # 获取信息
        info = self.get_student_info(self.studentNum)[0]
        # 设置要显示的信息，及修改密码的函数
        self.num_Label.configure(text=info[0])
        self.name_Label.configure(text=info[1])
        self.sex_Label.configure(text=info[2])
        self.age_Label.configure(text=info[3])
        self.pswd_Entry.insert(tkinter.INSERT, info[4])
        self.commitButton.configure(command=lambda :self.change_pswd(info[4], self.pswd_Entry.get()))
        # 放置组件，显示信息
        self.num_Label.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 0)
        self.name_Label.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 1)
        self.sex_Label.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 2)
        self.age_Label.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 3)
        self.pswd_Entry.place(x=TEXT_INDENT, y=TEXT_LINE_SPACE * 4)
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
        self.set_student_pswd(pswd)
        return

    def get_student_info(self, studentID):
        db = connect()
        cursor = db.cursor()
        sql = f'select distinct * from tb_student where studentID = \'{studentID}\''
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    def set_student_pswd(self, pswd):
        db = connect()
        cursor = db.cursor()
        sql = f'UPDATE tb_student SET studentPswd= \'{pswd}\' WHERE studentID = \'{self.studentNum}\''
        cursor.execute(sql)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        db.close()

# 选课区域
class stuChoose:
    def __init__(self, frame, studentNum):
        self.frame = frame
        self.studentNum = studentNum
        # 信息放置处, 滚动条
        self.resultScrollbar = tkinter.Scrollbar(self.frame)
        self.resultTable = ttk.Treeview(self.frame,
                                        height=10,
                                        columns=['课程号', '课程名', '课序号', '学分'],
                                        show='headings',
                                        yscrollcommand=self.resultScrollbar.set)
        # 选课按钮
        self.chooseButton = tkinter.Button(self.frame, text='选课', command=self.chooseCourse)
        # 提示信息
        self.promptLabel = tkinter.Label(self.frame, text='一次选一门课，已选的课不出现在列表里')
        # 选中的课程
        self.selected = None

        self.initialize()

    # frame和button的布局
    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1-RADIO)
        # 放置组件
        self.frame.update()
        self.frame.update()
        self.resultTable.place(height=self.frame.winfo_height(),
                               relwidth=0.6)
        self.frame.update()
        self.promptLabel.place(x=self.resultTable.winfo_x() + self.resultTable.winfo_width() + 5,
                               y=self.resultTable.winfo_y() + self.resultTable.winfo_height(), anchor='sw')
        self.chooseButton.place(x=self.resultTable.winfo_x() + self.resultTable.winfo_width() + 5,
                                y=self.resultTable.winfo_y() + self.resultTable.winfo_height() - 30, anchor='sw')

        self.displayInfo()

    # 显示选课信息
    def displayInfo(self):
        self.clear_course_info()
        self.resultTable.heading('课程号', text='课程号', anchor='w')
        self.resultTable.heading('课程名', text='课程名')
        self.resultTable.heading('课序号', text='课序号')
        self.resultTable.heading('学分', text='学分')

        self.resultTable.column('课程号', width=100, minwidth=100)
        self.resultTable.column('课程名', width=150, minwidth=150)
        self.resultTable.column('课序号', width=50, minwidth=50)
        self.resultTable.column('学分', width=100, minwidth=100)

        info_valid = self.get_class_optional()
        for x in info_valid:
            self.resultTable.insert('', tkinter.END, values=x)
        
        # print('以下是暂未安排老师的课程,不支持选择')
        # info_invalid = self.get_invalid_class_optional()
        # for x in info_invalid:
        #     self.resultTable.insert('', tkinter.END, values=x)

        self.resultTable.bind('<ButtonRelease-1>', self.get_selected_item)

    # 选课按钮
    def chooseCourse(self):
        if self.selected is None:
            self.promptLabel.configure(text='还未选择课程!')
        else:
            if self.insert_student_course(self.studentNum, self.selected['values'][0], self.selected['values'][2]) == 0:
                self.promptLabel.configure(text='选课成功！')
            else:
                self.promptLabel.configure(text='选课失败！')
        # 选课完成后更新选课列表
        self.displayInfo()

    # 获得选中课程信息
    def get_selected_item(self, event):
        curItem = self.resultTable.focus()
        self.selected = self.resultTable.item(curItem)
        print(self.selected)

    # 获取有效选课信息
    def get_class_optional(self):
        db = connect()
        cursor = db.cursor()
        sql = f'select C.courseID, C.courseName, C.courseNum, C.courseCredit ' \
              f'from tb_course as C, tb_teacher_course as TC ' \
              f'where C.courseID = TC.courseID and C.courseNum = TC.courseNum ' \
              f'and C.courseID not in (select courseID from tb_student_course where studentID = \'{self.studentNum}\')'
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    # 获取无效选课信息（没有分配老师的课程）
    def get_invalid_class_optional(self):
        db = connect()
        cursor = db.cursor()
        sql = f'select C.courseID, C.courseName, C.courseNum, C.courseCredit ' \
              f'from tb_course as C ' \
              f'where C.courseID not in \
                (select C.courseID \
                from tb_course as C, tb_teacher_course as TC, tb_student_course as SC \
                where C.courseID = TC.courseID and C.courseNum = TC.courseNum and SC.studentID = \'{self.studentNum}\') ' 
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result
    
    # 选课信息提交
    def insert_student_course(self, studentID, courseID, courseNum):
        db = connect()
        cursor = db.cursor()
        sql = f'INSERT INTO tb_student_course (studentID, courseID, courseNum, grade) VALUES (\'{studentID}\', \'{courseID}\', \'{courseNum}\', -1)'
        cursor.execute(sql)
        try:
            db.commit()
            db.close()
            return 0
        except:
            db.rollback()
            db.close()
            return 1

    # 选课信息清除
    def clear_course_info(self):
        for x in self.resultTable.get_children():
            self.resultTable.delete(x)

# 退课区域
class stuDrop:
    def __init__(self, frame, studentNum):
        self.studentNum = studentNum
        self.frame = frame
        # 信息放置处, 滚动条
        self.resultScrollbar = tkinter.Scrollbar(self.frame)
        self.resultTable = ttk.Treeview(self.frame,
                                        height=10,
                                        columns=['课程号', '课程名', '课序号', '学分'],
                                        show='headings',
                                        yscrollcommand=self.resultScrollbar.set)
        # 退课按钮
        self.dropButton = tkinter.Button(self.frame, text='退课', command=self.dropCourse)
        # 提示信息
        self.promptLabel = tkinter.Label(self.frame, text='一次退一门课，已退的课不出现在列表里')
        # 选中的课程
        self.selected = None

        self.initialize()

    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1-RADIO)
        # 放置组件
        # self.frame.update()
        self.frame.update()
        self.resultTable.place(height=self.frame.winfo_height(),
                               relwidth=0.6)
        self.frame.update()
        self.promptLabel.place(x=self.resultTable.winfo_x() + self.resultTable.winfo_width() + 5,
                               y=self.resultTable.winfo_y() + self.resultTable.winfo_height(), anchor='sw')
        self.dropButton.place(x=self.resultTable.winfo_x() + self.resultTable.winfo_width() + 5,
                                y=self.resultTable.winfo_y() + self.resultTable.winfo_height() - 30, anchor='sw')

        self.displayInfo()

    # 显示选课信息
    def displayInfo(self):
        self.clear_course_info()
        self.resultTable.heading('课程号', text='课程号', anchor='w')
        self.resultTable.heading('课程名', text='课程名')
        self.resultTable.heading('课序号', text='课序号')
        self.resultTable.heading('学分', text='学分')

        self.resultTable.column('课程号', width=50, minwidth=50)
        self.resultTable.column('课程名', width=120, minwidth=120)
        self.resultTable.column('课序号', width=50, minwidth=50)
        self.resultTable.column('学分', width=50, minwidth=50)
        info = self.get_class_optional()
        for x in info:
            self.resultTable.insert('', tkinter.END, values=x)

        self.resultTable.bind('<ButtonRelease-1>', self.get_selected_item)

    # 退课按钮
    def dropCourse(self):
        if self.selected is None:
            self.promptLabel.configure(text='还未选择课程!')
        else:
            if self.drop_student_course(self.studentNum, self.selected['values'][0], self.selected['values'][2]) == 0:
                self.promptLabel.configure(text='退课成功！')
            else:
                self.promptLabel.configure(text='退课失败！')
        # 选课完成后更新选课列表
        self.displayInfo()

    # 获得选中课程信息
    def get_selected_item(self, event):
        curItem = self.resultTable.focus()
        self.selected = self.resultTable.item(curItem)
        print(self.selected)

    # 获取已选信息
    def get_class_optional(self):
        db = connect()
        cursor = db.cursor()
        sql = f'select C.courseID, C.courseName, C.courseNum, C.courseCredit ' \
              f'from tb_course as C, tb_student_course as SC ' \
              f'where SC.studentID = \'{self.studentNum}\' and C.courseID =  SC.courseID and C.courseNum = SC.courseNum'
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    # 退课信息提交
    def drop_student_course(self, studentID, courseID, courseNum):
        db = connect()
        cursor = db.cursor()
        sql = f'DELETE FROM tb_student_course WHERE studentID = \'{studentID}\' ' \
              f'and courseID = \'{courseID}\' and courseNum = \'{courseNum}\''
        cursor.execute(sql)
        try:
            db.commit()
            db.close()
            return 0
        except:
            db.rollback()
            db.close()
            return 1

    # 课程信息清除
    def clear_course_info(self):
        for x in self.resultTable.get_children():
            self.resultTable.delete(x)

# 课程成绩区域
class stuGrade:
    def __init__(self, frame, studentNum):
        self.studentNum = studentNum
        self.frame = frame
        # 信息放置处, 滚动条
        self.resultScrollbar = tkinter.Scrollbar(self.frame)
        self.resultTable = ttk.Treeview(self.frame,
                                        height=10,
                                        columns=['课程号', '课程名', '课序号', '教师', '学分', '成绩'],
                                        show='headings',
                                        yscrollcommand=self.resultScrollbar.set)

        self.initialize()

    def initialize(self):
        self.frame.place(relx=RADIO, relheight=1, relwidth=1-RADIO)
        # 放置组件
        self.frame.update()
        self.frame.update()
        self.resultTable.place(height=self.frame.winfo_height(),
                               relwidth=0.8)

        self.displayInfo()

    # 显示选课信息
    def displayInfo(self):
        self.clear_course_info()
        self.resultTable.heading('课程号', text='课程号', anchor='w')
        self.resultTable.heading('课程名', text='课程名')
        self.resultTable.heading('课序号', text='课序号')
        self.resultTable.heading('教师', text='教师')
        self.resultTable.heading('学分', text='学分')
        self.resultTable.heading('成绩', text='成绩')

        self.resultTable.column('课程号', width=50, minwidth=50)
        self.resultTable.column('课程名', width=120, minwidth=120)
        self.resultTable.column('课序号', width=50, minwidth=50)
        self.resultTable.column('教师', width=50, minwidth=50)
        self.resultTable.column('学分', width=50, minwidth=50)
        self.resultTable.column('成绩', width=50, minwidth=50)

        info = self.get_class_selected()
        for x in info:
            self.resultTable.insert('', tkinter.END, values=x)

    # 获取已选课程
    def get_class_selected(self):
        db = connect()
        cursor = db.cursor()
        sql = f'select SC.courseID, C.courseName, SC.courseNum, T.teacherName, C.courseCredit, SC.grade ' \
              f'from tb_student_course as SC, tb_teacher as T, tb_teacher_course as TC, tb_course as C ' \
              f'where SC.studentID = \'{self.studentNum}\' and SC.courseNum = C.courseNum and SC.courseID = C.courseID ' \
                        'and T.teacherID = TC.teacherID and TC.courseID = C.courseID and TC.courseNum = C.courseNum'
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        return result

    def clear_course_info(self):
        for x in self.resultTable.get_children():
            self.resultTable.delete(x)

if __name__ == '__main__':
    c = menu('202101')
    c.start()
