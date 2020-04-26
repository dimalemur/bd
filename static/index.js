window.onload = () => {
  let profile = document.createElement('div');
  profile.className = "Profile";

  let groups = document.createElement('div');
  groups.className = "groups";
  document.body.append(groups);
  
  let authForm = document.getElementsByClassName('entry-content')[0];
  let Add = document.getElementById('Add');
  const AddGroupInpLesson = document.getElementById('AddGroupInpLesson');
  const AddLessonInp = document.getElementById('AddLessonInp');
  const AddGroupInpGroup = document.getElementById('AddGroupInpGroup');

  let login = document.getElementById('login'),
    password = document.getElementById('password'),
    help = document.getElementById('help'),
    groupsAll = document.getElementById('ChangeGroupForLessonInp'),
    groupsAllText = document.getElementById('ChangeGroupForLessonText'),
    lessonsAll = document.getElementById('ChangeLessonForGroupInp'),
    lessonAllText = document.getElementById('ChangeLessonForGroupText');

    ChangeLessonForGroupText

  let data;
  let lessons;
  let setLessons;
  let currntGroups;
  let allGroups;
  let allLessons;
  let lessonsByGroup;
  let groupByLesson;
  const setUserData = async () => {
    allGroups = await asyncGetAllGruops();
    allLessons = await asyncGetAllLessons();
    window.user_id = data.user_id;
    lessons = await asyncGetLessons(window.user_id);
    setLessons = await asyncGetSetLessons(window.user_id);

    AddGroupInpLesson.innerHTML = setLessons.map((element) => `<option>${element}</option>`).join('');
    AddLessonInp.innerHTML = lessons.map((element) => `<option>${element}</option>`).join('');

    currntGroups = await asyncGetGruops(window.user_id, AddGroupInpLesson.value)
    AddGroupInpGroup.innerHTML = currntGroups.map((element) => `<option>${element}</option>`).join('');

    groupsAll.innerHTML = allGroups.map((element) => `<option>${element}</option>`).join('');

    lessonsByGroup = await asyncGetLessonByGroup(groupsAll.value);
    groupsAllText.innerHTML = lessonsByGroup.map((element) => `<div>${element}</div>`).join('');

    lessonsAll.innerHTML = allLessons.map((element) => `<option>${element}</option>`).join('');

    groupByLesson = await asyncGetGroupByLesson(lessonsAll.value);
    lessonAllText.innerHTML = groupByLesson.map((element) => `<div>${element.join(' - ')}</div>`).join(' ');





    document.getElementById("Add").style.display = 'block';
    authForm.style.display = 'none';

    document.getElementById('InfoFirst').innerHTML = `<div class="Profile">
      <p class="Name">
        ${data.name}
      </p>
  
      <div class="Lessons">
        <div class="LessonsTitle">
        Предметы преподавателя:
        </div>
        ${ data.lessons.map(element => `<p class="Lesson">${element}</p>`).join('')}
      </div>
  
      <div class="Groups">
        <div class="GroupsTitle">
          Группы преподавателя:
        </div>
        <div class="GroupElement">
        <div class="Group">
            <b>Группа:</b>
          </div>
          <div class="Lesson">
            <b>Предмет:</b>
          </div>
        </div>
        ${
      data.teacher_groups.map(element => `
          <div class="GroupElement">
          <div class="Group">
            ${element[0]}
          </div>
          <div class="Lesson">
            ${element[1]}
          </div>
        </div>
          `).join('')
      }
      </div>
    </div>`
  }

  document.getElementById("autorize").addEventListener('submit', async (event) => {
    event.preventDefault();

    data = await asyncGetUser(login.value, password.value)
    window.login = login.value;
    window.password = password.value;
    login.value = '';
    password.value = '';

    if (Object.keys(data).length === 0) {
      help.textContent = 'Неверный логин или парооль';
      document.getElementById("Add").style.display = 'none';
      profile.innerHTML = '';
    } else {
      setUserData(data);
    }

  })

  AddGroupInpLesson.addEventListener('change', async (event) => {
    let currntGroups = await asyncGetGruops(window.user_id, event.target.value)
    AddGroupInpGroup.innerHTML = currntGroups.map((element) => `<option>${element}</option>`).join('');
  })


  document.getElementById("AddLesson").addEventListener('submit', async (event) => {

    event.preventDefault();
    let isSuccess = await asyncAddLesson(window.user_id, AddLessonInp.value);
    console.log(isSuccess);
    data = await asyncGetUser(window.login, window.password);
    setUserData()
  })

  document.getElementById("AddGroup").addEventListener('submit', async (event) => {

    event.preventDefault();
    let isSuccess = await asyncAddGroup(window.user_id, AddGroupInpLesson.value, AddGroupInpGroup.value);
    console.log(isSuccess);
    data = await asyncGetUser(window.login, window.password);
    setUserData()

  })

  document.getElementById('ChangeGroupForLessonInp').addEventListener('change', async (event) => {
    lessonsByGroup = await asyncGetLessonByGroup(event.target.value);
    groupsAllText.innerHTML = lessonsByGroup.map((element) => `<p>${element}</p>`).join('');

  })

  document.getElementById('ChangeLessonForGroupInp').addEventListener('change', async (event) => {
    groupByLesson = await asyncGetGroupByLesson(event.target.value);
    lessonAllText.innerHTML = groupByLesson.map((element) => `<div>${element.join(' - ')}</div>`).join(' ');

  })

  function asyncGetAllLessons() {
    return fetch('/sendalllessons', {
      credentials: 'same-origin',
      method: 'GET',
    })
      .then((response) => response.json())
      .then((data) => {
        return data
      })
      .catch((error) => {
        return error
      });
  };

  function asyncGetGroupByLesson(lesson) {
    return fetch('/groupbylesson', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ current_lesson: lesson })
    })
      .then((response) => response.json())
      .then((data) => {
        return data
      })
      .catch((error) => {
        return error
      });
  };

  function asyncGetLessonByGroup(group) {
    return fetch('/lessonbygroup', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ current_group: group })
    })
      .then((response) => response.json())
      .then((data) => {
        return data
      })
      .catch((error) => {
        return error
      });
  };

  function asyncGetAllGruops() {
    return fetch('/allgroups', {
      credentials: 'same-origin',
      method: 'GET',
    })
      .then((response) => response.json())
      .then((data) => {
        return data
      })
      .catch((error) => {
        return error
      });
  };

  function asyncGetUser(login, password) {
    return fetch('/auth', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ login, password }),
    })
      .then((response) => response.json())
      .then((data) => data)
      .catch((error) => error);
  };

  function asyncGetGruops(user_id, current_lesson) {
    return fetch('/gruops', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ user_id, current_lesson }),
    })
      .then((response) => response.json())
      .then((data) => {
        return data
      })
      .catch((error) => {
        return error
      });
  };

  function asyncGetLessons(user_id) {
    return fetch('/lessons', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ user_id }),
    })
      .then((response) => response.json())
      .then((data) => data)
      .catch((error) => error);
  };

  function asyncGetSetLessons(user_id) {
    return fetch('/setlessons', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ user_id }),
    })
      .then((response) => response.json())
      .then((data) => data)
      .catch((error) => error);
  };

  function asyncAddGroup(user_id, current_lesson, current_group) {
    return fetch('/addgroup', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ user_id, current_lesson, current_group }),
    })
      .then((response) => response.json())
      .then((data) => data)
      .catch((error) => error);
  };

  function asyncAddLesson(user_id, current_lesson) {
    return fetch('/addlesson', {
      credentials: 'same-origin',
      method: 'POST',
      body: JSON.stringify({ user_id, current_lesson }),
    })
      .then((response) => response.json())
      .then((data) => data)
      .catch((error) => error);
  };

};
