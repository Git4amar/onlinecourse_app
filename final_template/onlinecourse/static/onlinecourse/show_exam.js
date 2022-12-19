"use strict";

function show_exam(event) {
    if (event.target.checked == false) {
        document.querySelector('#exam').classList.add('show');
        window.scrollBy({
            top: window.innerHeight,
            behavior: 'smooth',
        });
    }
    else {
        document.querySelector('#exam').classList.remove('show');
    }
}