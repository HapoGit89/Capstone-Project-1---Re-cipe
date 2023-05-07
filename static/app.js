const stars = document.querySelectorAll('#star');
for (let i = 0; i < stars.length; i++) {
    stars[i].addEventListener("click", starClick)
}

async function starClick(e){
    if (e.target.classList.contains('fa-regular')){
        try{
        const resp = await axios.post(`/recipes/favourites/${e.target.dataset.recipe}/add`)
            e.target.classList.remove('fa-regular')
            e.target.classList.add('fa-solid')
            return resp
        }
        catch(e) {
         e.target.classList.remove('fa-solid')
        e.target.classList.add('fa-regular')
        }
        
    }
    else {
        try{
        const resp = await axios.post(`/recipes/favourites/${e.target.dataset.recipe}/remove`)
            e.target.classList.remove('fa-solid')
            e.target.classList.add('fa-regular')
            return resp
        }
        catch(e){
            e.target.classList.remove('fa-regular')
            e.target.classList.add('fa-solid')
        }
        
        
    }
}


