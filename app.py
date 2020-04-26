from flask import Flask, render_template
from flask import request
import json
from connect import *

app = Flask(__name__, static_folder="")


@app.route('/')
def main():
    print(123)
    return render_template('index.html')


@app.route('/auth', methods=['GET', 'POST'])
def get_user():
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        user_data = {}
        user_id = check_teacher(data['login'], data['password'])
        if user_id is not None:
            FIO = check_teacher_for_id(user_id)
            full_name = str(FIO[0][2]) + " " + \
                        str(FIO[0][1]) + " " + str(FIO[0][3])
            lessons = get_lessons(user_id)
            teacher_groups = get_teacher_groups(user_id)
            user_data = {
                'name': full_name,
                'lessons': lessons,
                'teacher_groups': teacher_groups,
                'user_id': user_id
            }

        return json.dumps(user_data)
    else:
        return 0


@app.route('/lessons', methods=['GET', 'POST'])
def get_lesson():
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        print(data)
        lessons = get_all_lessons(get_lessons(data['user_id']))
        return json.dumps(lessons)


@app.route('/setlessons', methods=['GET', 'POST'])
def set_lesson():
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        print(data)
        lessons = get_lessons(data['user_id'])
        return json.dumps(lessons)


@app.route('/gruops', methods=['GET', 'POST'])
def get_gruops():
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        current_id_lesson = get_lesson_by_text(data['current_lesson'])
        current_id_para = get_id_para_by_teacher(
            data['user_id'], current_id_lesson)
        groups = get_groups_and_paras_by_id_para(current_id_para)
        return json.dumps(get_all_groups(groups))


@app.route('/addgroup', methods=['GET', 'POST'])
def add_gruops():
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))
        print(data)
        id_para = get_para(
            data['user_id'], get_lesson_by_text(data['current_lesson']))

        id_group = get_group_by_text(data['current_group'])

        print(id_para, id_group)
        add_group_for_teacher(id_group, id_para)

        return json.dumps("success")


@app.route('/addlesson', methods=['GET', 'POST'])
def add_lesson():
    if request.method == 'POST':
        data = json.loads(request.data.decode("utf-8"))

        teacher_id = data['user_id']
        lesson_id = get_lesson_by_text(data['current_lesson'])
        add_para_for_teacher(teacher_id, lesson_id)

        return json.dumps("success")


@app.route('/allgroups', methods=['GET', 'POST'])
def get_allgroups():
    if request.method == 'GET':
        print(1)
        return json.dumps(get_all_groups([]))


@app.route('/lessonbygroup', methods=['GET', 'POST'])
def get_lessonbygroup():
    if request.method == 'POST':
        res = []
        group = json.loads(request.data.decode("utf-8"))['current_group']
        group_id = get_group_by_text(group)
        for i in get_paras_for_group(group_id):
            res.append(get_lesson_by_id_lesson(get_lesson_by_para(i)))
        return json.dumps(res)


@app.route('/sendalllessons', methods=['GET', 'POST'])
def get_sendalllessons():
    if request.method == 'GET':
        return json.dumps(get_all_lessons([]))


@app.route('/groupbylesson', methods=['GET', 'POST'])
def get_groupbylesson():
    if request.method == 'POST':
        res = []
        lesson = json.loads(request.data.decode("utf-8"))['current_lesson']
        lesson_id = get_lesson_by_text(lesson)
        for i in get_paras_for_lesson(lesson_id):
            teacher = get_teacher_by_teacher_id(i[1])
            if get_groups_and_paras_by_id_para(i[0]) != []:
                for i in get_groups_and_paras_by_id_para(i[0]):
                    res.append([i, teacher])
        return json.dumps(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
