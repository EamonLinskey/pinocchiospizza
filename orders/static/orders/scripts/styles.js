// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



function loadModal(food) {
	// Remove Active class from prevoious modals
	let prevActive = document.querySelector(".active")
	if (prevActive){
		prevActive.classList.remove("active")
	}

	// Show modal and mark as active
	let modalId = food.split(' ').join('')+'-modal'
	let modal = document.getElementById(modalId);
	modal.classList.add("active")
	modal.style.display = "block";

	// Check the first size checkbox if no box is checked yet
	if (modal.querySelectorAll('.size-radio:checked').length == 0 && 
			modal.querySelectorAll('.size-radio').length > 0){
				modal.querySelectorAll('.size-radio')[0].checked="true"
		}
	}

function hideModals() {
	for(let modal of document.querySelectorAll('.modal')){
		modal.style.display = "none"
	}
}

function updateCartDisplay() {
	console.log("cart updated")
}

function getFoodData() {
	let size = "small"
	if (document.querySelector('.active input[type="radio"]:checked')){
		size = document.querySelector('.active input[type="radio"]:checked').id
	}
	let toppings = Array.prototype.slice.call(document.querySelectorAll('.active input[type="checkbox"]:checked'));
	let numChecked = toppings.length
	let food = window.location.pathname.split('/').pop()
	let style = document.querySelector('.active .style').innerHTML
	let quantity = document.querySelector('.active .quantity').value
	let numToppings = (function(num){
		switch(num) {
			case 0:
				return "noExtra";
				break; 
			case 1:
				return "oneExtra";
				break; 
			case 2:
				return "twoExtra";
				break; 
			case 3:
				return "threeExtra";
				break; 
			default: 
				return "special";
		}
	}) (numChecked);

	for (var i = 0; i < toppings.length; i++) {
		toppings[i] = toppings[i].id
	}

	return [size, food, style, toppings, numToppings, quantity]
}

function arrayIsEqual(arr1, arr2){
	if (arr1 === arr2) return true;
  	if (arr1 == null || arr2 == null) return false;
  	if (arr1.length != arr2.length) return false;
  	for (let i = 0; i < arr1.length; i++) {
  		console.log(i)
  		if (typeof arr1[i] == "object" && typeof arr2[i] == "object"){
  			if (!arrayIsEqual(arr1[i], arr2[i])){
  				return false
  			}
  		}
  		else if(arr1[i] !== arr2[i]){
  			return false
  		}
  	}
  	return true
}

function addToCart() {
	let foodData = getFoodData()
	//console.log(foodData)
	//console.log((JSON.stringify(foodData)))
	if(localStorage.getItem("order")){
		orders = JSON.parse(localStorage.getItem("order"))
		let isUnique = true
		for(let order of orders){
			//console.log(order.slice(0, -1))
			if(arrayIsEqual(order.slice(0, -1), foodData.slice(0, -1))){
				order[order.length - 1 ] = parseInt(order[order.length - 1 ]) + parseInt(foodData[order.length -1])
				isUnique = false
			}

		}
		
		if(isUnique){
			newOrders = orders.concat([foodData])
		}
		else{
			newOrders = orders
		}
	}
	else{
		newOrders = [foodData]
	}
	localStorage.setItem("order", JSON.stringify(newOrders))

	order = localStorage.getItem("order")
	updateCartDisplay()
	// $.ajax({
	//     url: '/updateCart',
	//     dataType: "text json",
	//     type: "POST",
	//     data: { size: size,
	//     		food: food,
	//     		style: style,
	//     		quantity: quantity,
	//     		toppings: toppings,
	//     		numToppings: numToppings
	//     },
	//     success: function(jsonObject,status) {
	//     	console.log(jsonObject)
	//         console.log("function() ajaxPost : " + status);
	//         updateCartDisplay()
	//     }
	// });

}

function updatePrice() {
	// Get data for creating API url
	let [size, food, style, toppings, numToppings, quantity] =  getFoodData()

	// Build API url
	let url = `/prices/${food}/${style}/${size}/${numToppings}`

	// Fetch price from API
	fetch(url).then(
		function(response){
     		return response.json();
    	})
		.then(function(jsonData){
			// Update price in modal
    		document.querySelector('.active .current-price').innerHTML = "$" + (jsonData * quantity).toFixed(2)
		});
	
}



document.addEventListener("DOMContentLoaded", function(event) {
	// Get the modal
	let modals = document.querySelectorAll('.modal');
	
	for (var i = 0; i < modals.length; i++) {
		let span = modals[i].querySelector(".close");
		if (span){
			span.onclick = function() {
				hideModals()
			}
		}
	}
	
    let foods = document.querySelectorAll(".food-container")
    for(let food of foods){
    	food.onclick = () => {
    		loadModal(food.querySelector(".food-link").innerHTML)
    		updatePrice()
    	}
   	} 

   	let changers = document.querySelectorAll(".extra-check, .size-radio, .quantity")
   	for(let changer of changers){
    	changer.onchange = () => {
    		updatePrice()
    	}
   	} 

   	let buttons = document.querySelectorAll(".addToCart")
   	for(let button of buttons){
    	button.onclick = () => {
    		addToCart()
    		hideModals()
    	}
   	} 

});