"use strict";
document.addEventListener("DOMContentLoaded", setup);

let global = {};

/**
    The setup function is invoked when the DOM content is loaded.
    It sets the global object variables, such as the div that contains the
    stars for the rating and the paragraph that contains the average rating.
    It then calls setStars() to initialize the stars and
    adds an event listener for the onclick event on the div.
    @author David Pizzolongo
 **/
function setup(){
    global.starsDiv = document.querySelector("#starsContainer");
    global.ratingPara = document.querySelector("#rating").textContent;

    // maximum rating
    let numStars = 5;
    setStars(numStars);

    global.starsDiv.addEventListener("click", changeRating);
}

/**
    This method retrieves the rating from ratingPara and sets the textContent of
    the stars based on the rating. If the rating is not 0 or 5 stars, a count is used to
    keep track of the number of stars that are full (the rest will be empty). It then calls
    the displayStars function to display them on the webpage.
    @param numStars maximum project rating
    @author David Pizzolongo
 **/
function setStars(numStars){
    let count = 0;
    let indexRating = global.ratingPara.indexOf(":") + 2;
    let ratingNum = parseFloat(global.ratingPara.slice(indexRating));

    for (let i=0; i < numStars; i++){
       let star = document.createElement("span");

       // sets constants representing the minimum and maximum ratings
       const FIVE_STARS = 5;
       const ZERO_STARS = 0;

       if(ratingNum == FIVE_STARS){
        star.textContent = "\u2605";
       }
       else if (ratingNum == ZERO_STARS){
        star.textContent = "\u2606";
       }
       else{
            // ensures that ratings with decimals do not count as an extra star. Ex: Rating 2.9 --> 2 stars.
            let difference =  ratingNum - count;
            if (count <= ratingNum && difference >= 1){
                star.textContent = "\u2605";
                count++;
            }
            else{
                star.textContent = "\u2606";
            }
       }
       displayStars(star);
    }
}

/**
    The displayStars method sets all spans of stars to be associated with
    the .stars class. They are then added to the div container.
    @param star created by setStars
    @author David Pizzolongo
 **/
function displayStars(star){
    star.setAttribute("class", "stars");
    global.starsDiv.appendChild(star);
}

/**
    This function is called when the onclick event is triggered on the stars. It
    sets the star to be empty or full depending on its previous text content.
    @author David Pizzolongo
 **/
function changeRating(e){
   let starContent = e.target.textContent;
   // validates that the event was triggered on the spans rather than on the div
   if (e.target != e.currentTarget) {

       // full star becomes empty
       if(starContent === "\u2605"){
        e.target.textContent = "\u2606";
       }
       // empty star becomes full
       else{
        e.target.textContent = "\u2605";
       }
   }
}