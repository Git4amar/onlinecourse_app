"use strict";

document.addEventListener('DOMContentLoaded', () => {
    const learnerFormElements = document.querySelector('#add_learner_form').elements;
    const instructorFormElements = document.querySelector('#add_instructor_form').elements;
    const roleElement = document.querySelector('#roles');
    if (roleElement.value === 'default') {
        for (var i = 0; i < learnerFormElements.length; i++) {
            learnerFormElements[i].disabled = true;
        }
        for (var i = 0; i < instructorFormElements.length; i++) {
            instructorFormElements[i].disabled = true;
        }
        roleElement.size = 2;
    }
    else {
        roleElement.size = 0;
    }
});

function changeForm(event) {
    switch (event.target.value) {
        case 'instructor':
            document.querySelector('#add_learner_form').style.display = 'none';
            const instructorForm = document.querySelector('#add_instructor_form');
            const instructorFormElements = instructorForm.elements;
            for (var i = 0; i < instructorFormElements.length; i++) {
                instructorFormElements[i].disabled = false;
            }
            document.querySelector('#add_instructor_form').style.display = '';
            instructorFormElements['id_username'].focus();
            document.querySelector('#option-for-instructor').checked = true;
            break;

        case 'learner':
            document.querySelector('#add_instructor_form').style.display = 'none';
            const learnerForm = document.querySelector('#add_learner_form');
            const learnerFormElements = learnerForm.elements;
            for (var i = 0; i < learnerFormElements.length; i++) {
                learnerFormElements[i].disabled = false;
            }
            document.querySelector('#add_learner_form').style.display = '';
            learnerFormElements['id_username'].focus();
            document.querySelector('#option-for-learner').value = 'student';
            break;
    }
    document.querySelector('#roles').size = 0;
}

