'use strict';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#add_lesson_form').addEventListener('submit', preProcessLessonForm);
})

function autofocusTitle() {
  document.querySelector('#id_title').focus();
}

function preProcessLessonForm(event) {
  event.preventDefault();
  const lessonForm = event.target;

  fetch(`/onlinecourse/course/lesson/add/${lessonForm.dataset['course-id']}`, {
    method: "POST",
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') },
    mode: "same-origin",
    body: JSON.stringify({
      'title': lessonForm.elements['title'].value,
      'content': lessonForm.elements['content'].value,
    })
  })
    .then(res => {
      res.json()
        .then(data => {
          if (data.errors) {
            const titleError = JSON.parse(data.errors).title[0];
            const titleDiv = lessonForm.elements['title'].parentNode;
            document.querySelector("#id_title").classList.add("is-invalid");
            console.log(titleDiv);
            if (document.querySelector('#error_1_id_title') !== null) {
              const errElm = document.querySelector('#error_1_id_title');
              errElm.firstChild.innerHTML = titleError;
            }
            else {
              const errSpan = document.createElement("span");
              errSpan.className = "invalid-feedback"
              errSpan.id = "error_1_id_title";
              const errStrong = document.createElement("strong");
              const errText = document.createTextNode(titleError);
              titleDiv.appendChild(errSpan).appendChild(errStrong).appendChild(errText);
            }
          }
          else {
            location.reload();
          }
        })
        .catch(err => console.error(err.errors));
    });
}