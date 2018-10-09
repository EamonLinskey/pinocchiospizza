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

// Hide display of all modals
function hideModals() {
	for(let modal of document.querySelectorAll('.modal')){
		modal.style.display = "none"
	}
}

// Returns data about food items selected from modal
function getFoodData() {
	// Default to Small size if there is no opotion to mirror database otherwise
	// take the selection
	let size = "Small"
	if (document.querySelector('.active input[type="radio"]:checked')){
		size = document.querySelector('.active input[type="radio"]:checked').id
	}

	// Ititalize values from modal selection
	let toppings = Array.prototype.slice.call(document.querySelectorAll(
						'.active input[type="checkbox"]:checked'));
	let numChecked = toppings.length
	let food = window.location.pathname.split('/').pop()
	let style = document.querySelector('.active .style').innerHTML
	let quantity = parseInt(document.querySelector('.active .quantity').value)
	
	// Database was created using these string to bin types of pricing, thus
	// I used a switch case to get the string to match the database string based
	// on topping number
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

	// Initialize toppings list
	for (var i = 0; i < toppings.length; i++) {
		toppings[i] = toppings[i].id
	}

	return {"size":size, "food":food, "style":style, "toppings":toppings, 
			"numToppings":numToppings, "quantity": quantity}
}

// Checks whether too arrays are exaclty equal
function arrayIsEqual(arr1, arr2){
	// Check corner cases
	if (arr1 === arr2){
		return true;
	}
  	if (arr1 == null || arr2 == null){
  		return false;
  	} 
  	if (arr1.length != arr2.length) {
  		return false;
  	}

  	for (let i = 0; i < arr1.length; i++) {
  		// Recursively calls itself if arrays exist within the array
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
	// Get data from current item being added to cart
	let foodData = getFoodData()

	// Load previous items in order 
	if(localStorage.getItem("order")){
		orders = JSON.parse(localStorage.getItem("order"))

		// Check to see if the new order exactly matches a previous order
		// If it does sum the quantities instead of adding a new order
		// Topping list must be sorted and each topping checked individually
		let isUnique = true
		for(let order of orders){
			if(foodData["food"] == order["food"] && 
				foodData["style"] == order["style"] && 
				foodData["size"] == order["size"] && 
				foodData["numToppings"] == order["numToppings"] &&
				arrayIsEqual(foodData["toppings"].sort(), 
				order["toppings"].sort())){
					order["quantity"] = parseInt(order["quantity"]) + 
						parseInt(foodData["quantity"])
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
	
	// Update order order in local Storage
	localStorage.setItem("order", JSON.stringify(newOrders))
	localStorage.setItem("changed", true)
}

function updatePrice() {
	// Get data for creating API url
	let foodDict =  getFoodData()
	// Build API url
	let url = `/prices/${foodDict["food"]}/${foodDict["style"]}/
				${foodDict["size"]}/${foodDict["numToppings"]}`
	// Fetch price from API
	fetch(url).then(
		function(response){
     		return response.json();
    	})
		.then(function(jsonData){
			// Update price in modal
    		document.querySelector('.active .current-price').innerHTML = "$" + 
    		(jsonData * foodDict["quantity"]).toFixed(2)
		});
	
}


document.addEventListener("DOMContentLoaded", function(event) {
	// Get the modal
	let modals = document.querySelectorAll('.modal');
	
	// Add a close button to all modals
	for (var i = 0; i < modals.length; i++) {
		let span = modals[i].querySelector(".close");
		if (span){
			span.onclick = function() {
				hideModals()
				updateNavbar()
			}
		}
	}
	
	// Load each modal when food is clicked
    let foods = document.querySelectorAll(".food-container")
    for(let food of foods){
    	food.onclick = () => {
    		loadModal(food.querySelector(".food-link").innerHTML)
    		updatePrice()
    	}
   	} 

   	// Update price when ever any of these calues are changed
   	let changers = document.querySelectorAll(
   					".extra-check, .size-radio, .quantity")
   	for(let changer of changers){
    	changer.onchange = () => {
    		updatePrice()
    	}
   	} 

   	// Add to cart and hide modal on submit
   	let buttons = document.querySelectorAll(".addToCart")
   	for(let button of buttons){
    	button.onclick = () => {
    		addToCart()
    		location.href="/orders"
    	}
   	} 

});