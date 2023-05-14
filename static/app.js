class StarHandler {
  constructor() {
    this.init();
    this.likedClassName = 'fa-solid';
    this.unlikedClassName = 'fa-regular';
  }

  init() {
    const stars = document.querySelectorAll('#star');
    for (const star of stars) {
      star.addEventListener('click', e => this.onStarClick(e));
    }
  }

  isLiked(classList) {
    return classList.contains(this.likedClassName);
  }

  setToLiked(classList) {
    classList.remove(this.unlikedClassName);
    classList.add(this.likedClassName);
  }

  setToUnliked(classList) {
    classList.remove(this.unlikedClassName);
    classList.add(this.likedClassName);
  }

  async onStarClick(e) {
    const starClassList = e.target.classList;
    const recipeId = e.target.dataset.recipe;

    if (!this.isLiked(starClassList)) {
      try {
        this.setToLiked(starClassList);
        await this.saveLike(recipeId);
      } catch (e) {
        this.setToUnliked(starClassList);
      }
    } else {
      try {
        this.setToUnliked(starClassList);
        await this.removeLike(recipeId);
      } catch (e) {
        this.setToLiked(starClassList);
      }
    }
  }

  async saveLike(recipeId) {
    return await axios.post(`/recipes/favourites/${recipeId}/add`);
  }

  async removeLike(recipeId) {
    return await axios.post(`/recipes/favourites/${recipeId}/remove`);
  }
}

class HeartHandler {
  constructor() {
    const hearts = document.querySelectorAll("[id*='rating-heart']");
    for (const heart of hearts) {
      heart.addEventListener('click', e => this.onHeartClick(e));
    }
  }

  async onHeartClick(e) {
    const rating = e.target.dataset.number;
    const recipeId = e.target.dataset.recipe;

    try {
      await axios.post('/recipes/favourites/rating', {
        recipe_id: recipeId,
        rating: rating,
      });

      location.reload();

      // dieser return sollte egal sein, weil du die seite neu lädst
      return null;
    } catch (e) {
      console.error(e);
      location.reload();
    }
  }
}

new StarHandler();
new HeartHandler();
