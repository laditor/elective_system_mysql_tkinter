# 建表
CREATE SCHEMA `courseselection` ;

CREATE TABLE IF NOT EXISTS tb_student(
    studentID char(6) NOT NULL COMMENT '学号',
    studentName varchar(10) NOT NULL DEFAULT '匿名' COMMENT '姓名',
    studentSex char(2) NOT NULL DEFAULT '男' COMMENT '性别',
    studentAge tinyint NOT NULL DEFAULT '18' COMMENT '年龄',
    studentPswd varchar(20) NOT NULL DEFAULT '123456' COMMENT '密码',
    PRIMARY KEY(studentID) 
)ENGINE=INNODB DEFAULT CHARSET=utf8; 

CREATE TABLE IF NOT EXISTS tb_teacher(
    teacherID char(6) NOT NULL COMMENT '工号',
    teacherName varchar(10) NOT NULL DEFAULT '匿名' COMMENT '姓名',
    teacherSex char(2) NOT NULL DEFAULT '男' COMMENT '性别',
    teacherPswd varchar(20) NOT NULL DEFAULT '123456' COMMENT '密码',
    PRIMARY KEY (teacherID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS tb_manager(
    managerID char(6)NOT NULL COMMENT '工号',
    managerName varchar(10)NOT NULL DEFAULT '匿名' COMMENT '姓名',
    managerPswd varchar(20) NOT NULL DEFAULT '123456' COMMENT '密码',
    PRIMARY KEY (managerID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS tb_course(
    courseID varchar(6) NOT NULL COMMENT '课程号',
    courseName varchar(20) NOT NULL DEFAULT '匿名' COMMENT '课程名',
    courseNum tinyint NOT NULL COMMENT '课序号',
    courseCredit float NOT NULL DEFAULT 0 COMMENT '学分',
    courseDesc text NOT NULL COMMENT '课程介绍',
    PRIMARY KEY (courseID, courseNum)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS tb_student_course(
    studentID char(6) NOT NULL COMMENT '学号',
    courseID char(6) NOT NULL COMMENT '课程号',
    courseNum tinyint NOT NULL COMMENT '课序号',
    grade smallint NULL DEFAULT -1 COMMENT '成绩',
    PRIMARY KEY (studentID, courseID, courseNum),
    FOREIGN KEY (studentID) REFERENCES tb_student(studentID),
    FOREIGN KEY (courseID, courseNum) REFERENCES tb_course(courseID, courseNum)
)ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS tb_teacher_course(
    teacherID char(6)NOT NULL COMMENT '工号',
    courseID char(6) NOT NULL COMMENT '课程号',
    courseNum tinyint NOT NULL COMMENT '课序号',
    PRIMARY KEY (courseID, courseNum),
    FOREIGN KEY (teacherID) REFERENCES tb_teacher(teacherID),
    FOREIGN KEY (courseID, courseNum) REFERENCES tb_course(courseID, courseNum)
)ENGINE=INNODB DEFAULT CHARSET=utf8;


insert into tb_student values('202301','李铭','男','18','123456');
insert into tb_student values('202302','刘晓鸣','男','19','123456');
insert into tb_student values('202201','李明','男','20','123456');
insert into tb_student values('202303','张鹰','女','19','123456');
insert into tb_student values('202304','刘竟静','女','18','123456');
insert into tb_student values('202202','刘成刚','男','19','123456');
insert into tb_student values('202101','王铭','男','20','123456');
insert into tb_student values('202305','宣明尼','女','18','123456');
insert into tb_student values('202306','柳红利','女','19','123456');
insert into tb_student (studentID) values('202307');

insert into tb_teacher values('200015', '陈蓉', '女', '2000cr15');
insert into tb_teacher values('200710', '李晓华', '女', '2007lxh10');
insert into tb_teacher values('200407', '何军', '男', '2004hj07');
insert into tb_teacher values('200305', '熊运余', '男', '2003xyy05');
insert into tb_teacher values('200901', '林兰', '女', '2009ll01');
insert into tb_teacher (teacherID, teacherName, TeacherSex) values('200008', '黄武', '男');

insert into tb_manager values('200101', '李明', '123456');
insert into tb_manager values('200102', '王鹏', '123456');
insert into tb_manager values('200103', '大壮', '123456');

insert into tb_course values('A1-101', '程序开发基础', 1, 4, 'A1-101, Program development foundation.');
insert into tb_course values('A1-101', '程序开发基础', 2, 4, 'A1-101, Program development foundation.');
insert into tb_course values('S1-103', '面向对象程序设计', 1, 4, 'S1-103, Object-oriented programming.');
insert into tb_course values('S1-103', '面向对象程序设计', 2, 4, 'S1-103, Object-oriented programming.');
insert into tb_course values('A2-201', '数据结构与算法', 1, 4, 'A2-201, Data structure and algorithm.');
insert into tb_course values('A2-201', '数据结构与算法', 2, 4, 'A2-201, Data structure and algorithm.');
insert into tb_course values('A2-202', '操作系统', 1, 4, 'A2-202, Operating system.');
insert into tb_course values('A2-202', '操作系统', 2, 4, 'A2-202, Operating system.');
insert into tb_course values('A2-203', '计算机组成', 1, 3, 'A2-203, Computer composition.');
insert into tb_course values('A2-203', '计算机组成', 2, 3, 'A2-203, Computer composition.');
insert into tb_course values('S2-301', '数据库', 1, 4, 'S2-301, database.');
insert into tb_course values('S2-301', '数据库', 2, 4, 'S2-301, database.');
insert into tb_course values('S2-302', '计算机网络', 1, 4, 'S2-302, computer network.');
insert into tb_course values('S2-302', '计算机网络', 2, 4, 'S2-302, computer network.');
insert into tb_course values('S2-303', '软件工程导论', 1, 3, 'S2-303, ntroduction to Software Engineering.');
insert into tb_course values('S2-303', '软件工程导论', 2, 3, 'S2-303, ntroduction to Software Engineering.');

insert into tb_student_course (studentID, courseID, courseNum) values('202301', 'S1-103', 1);
insert into tb_student_course values('202201', 'S2-301', 1, 92);
insert into tb_student_course (studentID, courseID, courseNum) values('202202', 'S2-301', 2);
insert into tb_student_course (studentID, courseID, courseNum) values('202202', 'S2-302', 1);
insert into tb_student_course (studentID, courseID, courseNum) values('202201', 'S2-302', 1);
insert into tb_student_course values('202201', 'S2-303', 1, 90);
insert into tb_student_course values('202202', 'S2-303', 2, 85);

insert into tb_teacher_course values('200407', 'S1-103', 1);
insert into tb_teacher_course values('200710', 'S1-103', 2);
insert into tb_teacher_course values('200015', 'S2-301', 1);
insert into tb_teacher_course values('200407', 'S2-301', 2);
insert into tb_teacher_course values('200901', 'S2-302', 1);
insert into tb_teacher_course values('200305', 'S2-302', 2);
insert into tb_teacher_course values('200710', 'S2-303', 1);
insert into tb_teacher_course values('200015', 'S2-303', 2);

