
let TAX = 0.0625;

function loadOrders(orders){
	// Initialize variables and reset HTML of container
	let newOrders = [];
	document.querySelector(".orders-container").innerHTML = ""

	// Remove any orders that with quantity 0 or lower
	if(orders){
		for (let order of orders) {
			if (order["quantity"] > 0){
				newOrders.push(order)
			}
		}

		// Reset orders in local storage with cleaned orders
		if(newOrders.length > 0){
			localStorage.setItem("order", JSON.stringify(newOrders))
		}
		else{
			localStorage.removeItem(orders)
			document.querySelector(".orders-container").innerHTML = 
				"Your Cart is Empty"
		}
		
		// Becasue we load the order from local storage we create a template
		// using js instead of django templates
		for (var i = 0; i < newOrders.length; i++) {

			// i is used as a temporary id for selecting orders in template
			if (newOrders[i]["quantity"] > 0){
				let markupTop = `
				<div class="order order${i}">
			    	<div>`;
				//Markup Middle has two potential values to account for 
				// gramatical prefrences of listing the topping selections
				let markupMiddle = `   	
				        	${newOrders[i]["size"]}  ${newOrders[i]["style"]} 
				        		with ${newOrders[i]["toppings"].join(", ")}
				        	`;
				if(newOrders[i]["toppings"].length == 0){
					markupMiddle = `   	
				        	${newOrders[i]["size"]}  ${newOrders[i]["style"]}
				        	`;
				}
				let markupBottom = ` 	
				    	</div>
				    	<div class="clicker order${i}">
				    		<div>Price: 
				    			<span class="price order${i}"></span>
				    		</div>
				    		Quantity: 
				    		<span class="add order${i}">+</span>
							<span class="quantity order${i}">
								${newOrders[i]["quantity"]}
							</span>
				    		<span class="subtract order${i}">-</span>
				    	</div>
				    	<div class="delete order${i}">delete</div>
				 	</div>
				`;

				// Add to HTML, update price and iterate Total
				document.querySelector(".orders-container").innerHTML 
					+= markupTop + markupMiddle + markupBottom;
				updatePrice(newOrders[i], i, parseInt(newOrders[i]["quantity"]))
			}
		}
	}
	else{
		document.querySelector(".orders-container").innerHTML = 
			"Your Cart is Empty"
	}
}

function updatePrice(order, id, change) {
	// Build API url
	let url = `/prices/${order["food"]}/${order["style"]}/${order["size"]}/
		${order["numToppings"]}`

	// Fetch price from API
	fetch(url).then(
		function(response){
     		return response.json();
    	})
		.then(function(jsonData){
			console.log(change)
			// Update price in modal
    		document.querySelector('.price.order'+id).innerHTML = 
    			"$" + (jsonData * order["quantity"]).toFixed(2)

    		// Calculate totals
    		let subtotal = parseFloat(document.querySelector(
				".subtotal").textContent)
			let newSubtotal = (jsonData*change) + subtotal;
			let newTax = newSubtotal * TAX;
			let newTotal = newSubtotal + newTax;

			// Update Totals in HTML
    		document.querySelector(".subtotal").innerHTML = 
    			newSubtotal.toFixed(2)
    		document.querySelector(".tax").innerHTML = newTax.toFixed(2)
    		document.querySelector(".total").innerHTML = newTotal.toFixed(2)
		});
	
}




document.addEventListener("DOMContentLoaded", function(event) {
	// load in orders
	let orders = JSON.parse(localStorage.getItem("order"))
	loadOrders(orders)

	for (let button of document.querySelectorAll(".add, .subtract")){
		button.onclick = function() {
				// initialize valuse
				let order = button.classList[1]
				let quantity = parseInt(document.querySelector(
					'.quantity.'+order).innerHTML);

				// if user selected minus change should be negative 
				// if plus it should be positive
				let change = 1
				if(button.classList[0] == "subtract"){
					change = -1
				}

				// Get index from the ticket HTML class. I did not use id's 
				// becasue there would be more than one id
				let orderIndex = parseInt(order.replace("order", ""))
				orders = JSON.parse(localStorage.getItem("order"))

				if(quantity+change >= 0){
					// Update HTML and storage
					document.querySelector('.quantity.'+order).innerHTML = 
						quantity+change;
					orders[orderIndex]["quantity"]= 
						parseInt(orders[orderIndex]["quantity"]) + change
					updatePrice(orders[orderIndex], orderIndex, change)
					localStorage.setItem("order", JSON.stringify(orders))
				}
				
			}
	}

	for (let deleteButton of document.querySelectorAll(".delete")){
		deleteButton.onclick = function() {
			// Initialize values
			let order = deleteButton.classList[1]
			let orderIndex = parseInt(order.replace("order", ""))
			let orders = JSON.parse(localStorage.getItem("order"))

			// Delete item from local storage
			orders.splice(orderIndex, 1)
			localStorage.setItem("order", JSON.stringify(orders))

			// Reload page to make sure tickets update with proper id's
			location.reload()
		}
	}
})