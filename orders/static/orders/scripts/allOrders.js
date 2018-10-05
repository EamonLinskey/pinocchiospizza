// Sends completed order to server to update orders data
function completedOrder(data, buttonId){
	$.ajax({
	    url: '/completedOrder',
	    dataType: "text json",
	    type: "POST",
	    data: data,
	    success: function(jsonObject,status) {
	    	// On success the tickey is removed and the cart count is updated
	    	document.querySelector(".ticket"+buttonId).remove();
			ordersCount = document.querySelectorAll(".ticket").length
			document.querySelector(".orders-count").innerHTML = 
				"There are currently " + ordersCount + " orders";
	    }
	});
}


document.addEventListener("DOMContentLoaded", function(event) {
	let buttons = document.querySelectorAll(".btn");
	// Each button onclick removes item fom order
	for(let button of buttons){
		button.onclick = () => {
			let ticketDict = {orderId: button.id};
			completedOrder(ticketDict, button.id);
		}
	}
});