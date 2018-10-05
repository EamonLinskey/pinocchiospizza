document.addEventListener("DOMContentLoaded", function(event) {
    // gets current path
    let current_path = window.location.pathname.split("/")[1]
    if (current_path == ""){
    	current_path = "index"
    }
    console.log(current_path)
    // Remove active tag from prevously selected button
    let prevActive = document.querySelector('.active')
    if (prevActive){
    	prevActive.classList.remove("active");
    }
  	
    // Adds active tag to the currently selected button
    let active = document.querySelector(`.${current_path}`);
    if (active){
    	active.classList.add("active");
    }
	
    // Keeps Cart number accurate on page loads
	if(localStorage.getItem("order")){
		document.querySelector(".order-number").innerHTML = JSON.parse(localStorage.getItem("order")).length
	}
	

});