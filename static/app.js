const stars = document.querySelectorAll('#star');
const hearts = document.querySelectorAll("[id*='rating-heart']");


for (let i = 0; i < stars.length; i++) {
    stars[i].addEventListener("click", starClick)
}

for (let i = 0; i < hearts.length; i++) {
    hearts[i].addEventListener("click", heartClick)
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

async function heartClick(e){

    try{
        console.log(e.target.dataset.number)
    resp= axios.post('/recipes/favourites/rating', {recipe_id: e.target.dataset.recipe, rating: e.target.dataset.number})
    location.reload()
        console.log(resp)
    return resp
    }
    catch(e){
        location.reload()

    }
}
