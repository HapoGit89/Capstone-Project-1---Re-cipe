stars = document.querySelectorAll('#star');
for (let i = 0; i < stars.length; i++) {
    stars[i].addEventListener("click", starClick)
}

async function starClick(e){
    if (e.target.classList.contains('fa-regular')){
        console.log(`${e.target.dataset.recipe}`)
        resp = await axios.post(`/recipes/favourites/${e.target.dataset.recipe}/add`)
        e.target.classList.remove('fa-regular')
        e.target.classList.add('fa-solid')
        return resp
    }
    else {
        resp = await axios.post(`/recipes/favourites/${e.target.dataset.recipe}/remove`)
        e.target.classList.remove('fa-solid')
        e.target.classList.add('fa-regular')
        return resp
    }
}
