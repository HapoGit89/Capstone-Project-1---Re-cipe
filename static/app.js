stars = document.querySelectorAll('#star');
for (let i = 0; i < stars.length; i++) {
    stars[i].addEventListener("click", starClick)
}

function starClick(e){
    console.log(e.target.dataset.recipe)
}