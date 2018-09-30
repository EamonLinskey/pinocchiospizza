document.addEventListener("DOMContentLoaded", function(event) {
    let current_path = window.location.pathname.split("/")[1]
    if (current_path == ""){
    	current_path = "index"
    }

    let prevActive = document.querySelector('.active')
    if (prevActive){
    	prevActive.classList.remove("active");
    }
  	
    let active = document.querySelector(`.${current_path}`);
    if (active){
    	active.classList.add("active");
    }
	

	if(localStorage.getItem("order")){
		document.querySelector(".order-number").innerHTML = JSON.parse(localStorage.getItem("order")).length
	}
	

});