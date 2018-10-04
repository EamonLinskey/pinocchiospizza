let TAX = 0.0625;

function loadOrders(orders){
	let newOrders = [];
	document.querySelector(".orders-container").innerHTML = ""
	if(orders){
		for (var i = 0; i < orders.length; i++) {
			if (orders[i][5] > 0){
				newOrders.push(orders[i])
			}
		}

		if(newOrders.length > 0){
			localStorage.setItem("order", JSON.stringify(newOrders))
		}
		else{
			localStorage.removeItem(orders)
			document.querySelector(".orders-container").innerHTML = "Your Cart is Empty"
		}
		console.log(`---${newOrders}`)
		for (var i = 0; i < newOrders.length; i++) {
			console.log(orders[i])
			if (newOrders[i][5] > 0){
				let markupTop = `
				<div class="order order${i}">
			    	<div>`;
			
				let markupMiddle = `   	
				        	${newOrders[i][0]}  ${newOrders[i][2]} with ${newOrders[i][3].join(", ")}
				        	`;
				if(newOrders[i][3].length == 0){
					markupMiddle = `   	
				        	${newOrders[i][0]}  ${newOrders[i][2]}
				        	`;
				}
				let markupBottom = ` 	
				    	</div>
				    	<div class="clicker order${i}">
				    		<div>Price: <span class="price order${i}"></span></div>
				    		Quantity: 
				    		<span class="add order${i}">+</span>
							<span class="quantity order${i}">${newOrders[i][5]}</span>
				    		<span class="subtract order${i}">-</span>
				    	</div>
				    	<div class="delete order${i}">delete</div>
				 	</div>
				`;
				document.querySelector(".orders-container").innerHTML += markupTop + markupMiddle + markupBottom;
				updatePrice(newOrders[i], i)
				updateTotal(newOrders[i], parseInt(newOrders[i][5]))
			}
		}
	}
	else{
		document.querySelector(".orders-container").innerHTML = "Your Cart is Empty"
	}
}

function updatePrice(order, id) {
	// Get data for creating API url
	let [size, food, style, toppings, numToppings, quantity] =  order
	// Build API url
	let url = `/prices/${food}/${style}/${size}/${numToppings}`
	console.log(url)

	// Fetch price from API
	fetch(url).then(
		function(response){
     		return response.json();
    	})
		.then(function(jsonData){
			// Update price in modal
    		document.querySelector('.price.order'+id).innerHTML = "$" + (jsonData * quantity).toFixed(2)
		});
	
}


function updateTotal(order, change){
	let [size, food, style, toppings, numToppings, quantity] =  order
	let url = `/prices/${food}/${style}/${size}/${numToppings}`
	console.log(url)
	fetch(url).then(
		function(response){
     		return response.json();
    	})
		.then(function(jsonData){
			// Update price in modal
			let subtotal = parseFloat(document.querySelector(".subtotal").textContent)
			console.log(subtotal)
			console.log(change)
			console.log(jsonData)
			let newSubtotal = (jsonData*change) + subtotal;
			let newTax = newSubtotal * TAX;
			let newTotal = newSubtotal + newTax;

			console.log(newSubtotal)
    		document.querySelector(".subtotal").innerHTML = newSubtotal.toFixed(2)
    		document.querySelector(".tax").innerHTML = newTax.toFixed(2)
    		document.querySelector(".total").innerHTML = newTotal.toFixed(2)
		});
}

document.addEventListener("DOMContentLoaded", function(event) {
	let orders = JSON.parse(localStorage.getItem("order"))
	loadOrders(orders)

	for (let button of document.querySelectorAll(".add, .subtract")){
		button.onclick = function() {
				let order = button.classList[1]
				console.log(order)
				let quantity = parseInt(document.querySelector('.quantity.'+order).innerHTML);
				let change = 1
				if(button.classList[0] == "subtract"){
					change = -1
				}

				let orderIndex = parseInt(order.replace("order", ""))
				orders = JSON.parse(localStorage.getItem("order"))

				if(quantity+change >= 0){
					document.querySelector('.quantity.'+order).innerHTML = quantity+change;
					orders[orderIndex][5]= parseInt(orders[orderIndex][5]) + change
					updatePrice(orders[orderIndex], orderIndex)
					localStorage.setItem("order", JSON.stringify(orders))
					updateTotal(orders[orderIndex], change)
				}
				
			}
	}

	for (let deleteButton of document.querySelectorAll(".delete")){
		deleteButton.onclick = function() {
			let order = deleteButton.classList[1]
			let orderIndex = parseInt(order.replace("order", ""))
			let orders = JSON.parse(localStorage.getItem("order"))
			orders.splice(orderIndex, 1)
			localStorage.setItem("order", JSON.stringify(orders))
			location.reload()
		}
	}

	

})