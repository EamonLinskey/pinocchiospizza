function loadModal(food) {
	let modal = document.getElementById('modal');
	modal.style.display = "block";
}

document.addEventListener("DOMContentLoaded", function(event) {
	// Get the modal
	let modal = document.getElementById('modal');

	// Get the <span> element that closes the modal
	let span = document.getElementsByClassName("close")[0];

	

	// When the user clicks on <span> (x), close the modal
	if (span){
		span.onclick = function() {
	    modal.style.display = "none";
	}
	}
	

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	    if (event.target == modal) {
	        modal.style.display = "none";
	    }
	}
    let foods = document.querySelectorAll(".food-container")
    for(let food of foods){
    	food.onclick = () => {
    		loadModal(food)
    	}
   	}
    
});