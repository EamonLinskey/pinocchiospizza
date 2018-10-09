function updateNavbar() {
    // gets current path
    let current_path = window.location.pathname.split("/")[1]
    if (current_path == ""){
        current_path = "index"
    }
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
}

document.addEventListener("DOMContentLoaded", function(event) {
	updateNavbar()
    // Keeps Cart number accurate on page loads
	if(localStorage.getItem("order")){  
        try
        {
            // Adds a flashing animation to give user feedback if the order has changed recently
            if (JSON.parse(localStorage.getItem("changed"))){
                document.querySelector(".order-number").classList.add('order-number-flash')
                localStorage.removeItem("changed")
            }
        }
        finally
        {
		  document.querySelector(".order-number").innerHTML = JSON.parse(localStorage.getItem("order")).length
        }
	}
	

});