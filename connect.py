import psycopg2

conn = psycopg2.connect(dbname='pd', user='postgres', password='password', host='localhost', port=5432)

cur = conn.cursor()


def id_lesson_by_id_para(id_para):  # Получить id урока по id пары
    cur.execute("select id_lesson from para where id_para = " + str(id_para))
    return cur.fetchall()[0][0]


def get_lesson_by_id_lesson(id_lesson):  # Получить название урока по id урока
    cur.execute("select lesson_name from lesson where id_lesson = " + str(id_lesson))
    return cur.fetchall()[0][0]


def get_all_lessons(exceptions):  # Получить все уроки
    res = []
    cur.execute('SELECT lesson_name FROM lesson')
    lessons = cur.fetchall()
    for lesson in lessons:
        if lesson[0] not in exceptions:
            res.append(lesson[0])
    return res


def get_para(teacher_id, lesson_id):  # Получить пару по id учителя и урока
    cur.execute("select id_para from para where id_teacher = " + str(teacher_id) + " and id_lesson =" + str(lesson_id))
    return cur.fetchall()[0][0]


def get_groups_and_paras_by_id_para(id_para):  # Получить пары по id препода
    res = []
    cur.execute("select * from groups_and_paras where id_para = " + str(id_para))
    groups_id = cur.fetchall()
    for i in groups_id:
        cur.execute("select group_number from groups where id_group = " + str(i[0]))
        for j in cur.fetchall():
            res.append(j[0])
    return res


def get_teacher_by_teacher_id(teacher_id):
    cur.execute("select * from teacher where id_teacher =" + str(teacher_id))
    res = cur.fetchall()
    res = res[0][2] + " " + res[0][1] + " " + res[0][3]
    return res


def get_teacher_groups(teacher):  # Получить группы препода по id препода
    res = []
    cur.execute('select * from para where id_teacher= ' + str(teacher))
    para = cur.fetchall()
    for i in para:
        cur.execute("select * from groups_and_paras where id_para =" + str(i[0]))
        for j in cur.fetchall():
            cur.execute("select group_number from groups where id_group=" + str(j[0]))
            for a in cur.fetchall():
                if a[0] not in res:
                    cur.execute("select lesson_name from lesson where id_lesson = " + str(id_lesson_by_id_para(i[0])))
                    lesson = cur.fetchall()
                    res.append([a[0], lesson[0][0]])
    return res


def get_id_para_by_teacher(id_teacher, id_lesson):  # Получить пару по id учителя и урока
    cur.execute(
        "select id_para from para  where id_teacher = " + str(id_teacher) + " and id_lesson = " + str(id_lesson))
    return cur.fetchall()[0][0]


def get_id_paras_by_group(id_group):  # Получить пары по id группы
    res = []
    cur.execute(
        "select * from groups_and_paras where id_group =" + str(id_group))

    for i in cur.fetchall():
        res.append(i[1])
    return res


# def get_para_tacher_and_lesson(id_para):  # Получить имя учителя и название урока по паре
#     res = []
#     cur.execute('select id_teacher,id_lesson from para where id_para = ' + str(id_para))
#     groups = cur.fetchall()


def get_all_groups(exceptions):  # Получить все группы
    res = []
    cur.execute('SELECT group_number FROM groups')
    groups = cur.fetchall()
    for group in groups:
        if group[0] not in exceptions:
            res.append(group[0])
    return res


def add_para_for_teacher(id_teacher, id_lesson):
    cur.execute("select id_para from para")
    all_id_mass = cur.fetchall()
    all_id = []
    for id in all_id_mass:
        all_id.append(id[0])
    i = 0
    id_para = 0
    while True:
        if i not in all_id:
            id_para = i
            break
        i += 1
    cur.execute(
        "insert into para (id_para,id_teacher,  id_lesson) values (" + str(id_para) + "," + str(
            id_teacher) + "," + str(
            id_lesson) + " )"
    )
    conn.commit()


def add_group_for_teacher(id_group, id_para):
    cur.execute("insert into groups_and_paras (id_group,  id_para) values (" + str(id_group) + "," + str(id_para) + ")")
    conn.commit()


def add_teacher(teacher_name, teacher_surname, teacher_otchestvo, login, password):
    id = get_id_teacher()
    cur.execute("insert into teacher(id_teacher,teacher_name,teacher_surname,teacher_otchestvo,login,password) "
                "VALUES (" + str(id) + ",'" + teacher_name + "','" + teacher_surname + "','"
                + teacher_otchestvo + "','" + login + "','" + password + "')")
    conn.commit()


def check_teacher(login, password):
    cur.execute(" select * from teacher where login = '" + str(login) + "' and password = '" + str(password) + "' ")
    teacher = cur.fetchall()
    if teacher:
        return teacher[0][0]


def check_teacher_for_id(id):
    cur.execute(" select * from teacher where id_teacher = " + str(id))
    teacher = cur.fetchall()
    if teacher:
        return teacher


def check_student_in_group(group_id, student_id):
    cur.execute("select * from students where id_group = " + str(group_id) + " and id_sudent = " + str(student_id))
    return cur.fetchall()


def get_lessons(teacher):  # Получить уроки по преподавателю
    res = []
    cur.execute("select * from para where id_teacher =" + str(teacher))
    id_lessons = cur.fetchall()
    for i in id_lessons:
        cur.execute("select lesson_name from lesson where id_lesson = " + str(i[2]))
        res.append(cur.fetchall()[0][0])
    return res


def get_lesson_by_text(text):  # Получить id урока по названию
    cur.execute("select id_lesson from lesson where lesson_name= '" + text + "'")
    return cur.fetchall()[0][0]


def get_teachers_by_lesson(id_lesson):  # Получить id преподавателей по id урока
    res = []
    cur.execute("select id_teacher from para where id_lesson = " + str(id_lesson))
    for i in cur.fetchall():
        res.append(i[0])
    return res


def get_group_by_text(text):  # Получить id группы по названию
    cur.execute("select id_group from groups where group_number = '" + text + "'")
    resp = cur.fetchall()
    if resp:
        return resp[0][0]
    else:
        return []


def get_id_teacher():
    cur.execute("select id_teacher from teacher ORDER BY id_teacher")
    j = 0
    all = cur.fetchall()
    for i in all:
        if j != i[0]:
            return j
        j += 1
    return len(all)


def add_work_for_table(id_para, work_name, work_type):
    cur.execute("select id_work from works")
    id_works = []
    for i in cur.fetchall():
        id_works.append(i[0])
    index = 0
    while True:
        if index not in id_works:
            break
        else:
            index += 1
    cur.execute("insert into works (id_work,id_para,work_name,work_type)"
                "values ( " + str(index) + ", '" + str(id_para) + "','" + str(work_name) + "', ' " + str(
        work_type) + "')")
    conn.commit()


def add_submit_work(id_student, id_work):
    cur.execute(
        "insert into submitted_works (id_student,id_work) values ( " + str(id_student) + " , " + str(id_work) + ")")
    print("Принято")
    conn.commit()


def submit_work(student_id, para_id):
    res = []
    cur.execute('SELECT * FROM submitted_works where id_student =' + str(student_id))
    for work in cur.fetchall():
        cur.execute(
            'SELECT id_work,work_name,work_type FROM works WHERE id_work=' + str(work[1]) + 'and id_para = ' + str(
                para_id))
        result = cur.fetchall()
        if result:
            res.append(result)
    return res


def get_works_for_para_id_1(id_para):  # Получить работы по id пары
    res = []
    cur.execute('select work_name,work_type from works where id_para = ' + str(id_para))
    return cur.fetchall()


def get_works_for_para_id(id_para):  # Получить работы по id пары
    res = []
    cur.execute('select work_name,work_type from works where id_para = ' + str(id_para))
    for i in cur.fetchall():
        res.append(i[0] + " : " + i[1])

    return res


def get_works_id_for_para_id(id_para):  # Получить id всех работы по id пары
    res = []
    cur.execute('select id_work from works where id_para = ' + str(id_para))
    asd = cur.fetchall()
    if asd:
        for i in asd:
            res.append(i[0])
    return res


def get_id_work(para_id, work_name, work_type):  # Получить id работы по id пары
    cur.execute(
        "select id_work from works where id_para = " + str(para_id) + " and "
                                                                      "work_name = '" + str(work_name) + "' "
                                                                                                         "and work_type = '" + str(
            work_type) + "'"
    )
    return cur.fetchall()[0][0]


def get_students_by_group(id_group, exceptions=[]):  # Получить ФИО студентов по id группы (с исключениями)
    res = []
    cur.execute("select name,surname,otchestvo from students where id_group = " + str(id_group))
    for i in cur.fetchall():
        fio = str(i[0]) + " " + str(i[1]) + " " + str(i[2])
        if fio not in exceptions:
            res.append(fio)
    return res


def get_students_id_by_group(id_group, exceptions=[]):  # Получить id студентов по id группы (с исключениями)
    res = []
    cur.execute("select id_sudent from students where id_group = " + str(id_group))
    for i in cur.fetchall():
        if i[0] not in exceptions:
            res.append(i[0])
    return res


def get_students_FIO_which_submit_work(work_id):  # Получить ФИО студентов сдавших работу по id работы
    res = []
    cur.execute('select id_student from submitted_works where id_work = ' + str(work_id))
    id_std = cur.fetchall()
    if id_std:
        for i in id_std:
            cur.execute("select name,surname,otchestvo from students where id_sudent = " + str(i[0]))
            for j in cur.fetchall():
                fio = str(j[0]) + " " + str(j[1]) + " " + str(j[2])
                res.append(fio)
    return res


def get_student_id(name, surname, otchestvo, id_group):  # Получить id студента по ФИО и группе
    res = None
    cur.execute("select id_sudent from students where id_group = " + str(id_group) + " and "
                                                                                     "name = '" + str(name) + "'"
                                                                                                              "and surname = '" + str(
        surname) + "' "
                   "and otchestvo = '" + str(otchestvo) + "'")
    res = cur.fetchall()
    if res:
        return res[0][0]


def get_teacher_id(surname, name, otchestvo):  # Получить id преода по ФИО
    res = None
    cur.execute("select id_teacher from teacher where teacher_name = '" + str(name) + "' and teacher_surname = '" + str(
        surname) + "' and teacher_otchestvo = '" + str(otchestvo) + "'")
    res = cur.fetchall()
    if res:
        return res[0][0]


def get_work_id_in_submitted_works(id_student):  # Получить сданные работа по id студента
    res = []
    cur.execute('select id_work from submitted_works where id_student = ' + str(id_student))
    wrks = cur.fetchall()
    if wrks:
        for i in wrks:
            res.append(i[0])
    return res


def get_work_by_id(id_work):  # Получить название работы по id
    cur.execute("select work_name,work_type from works where id_work = " + str(id_work))
    return cur.fetchall()[0]
