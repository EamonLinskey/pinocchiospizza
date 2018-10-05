// Whens user hits the sucess page it should empty their cart
document.addEventListener("DOMContentLoaded", function(event) {
	localStorage.removeItem("order")
	document.querySelector(".order-number").innerHTML = "0"
});