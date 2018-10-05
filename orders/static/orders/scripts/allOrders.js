function completedOrder(data){
	$.ajax({
	    url: '/completedOrder',
	    dataType: "text json",
	    type: "POST",
	    data: data,
	    success: function(jsonObject,status) {
	    	console.log(jsonObject)
	        console.log("function() ajaxPost : " + status);
	    }
	});
}

document.addEventListener("DOMContentLoaded", function(event) {
	let buttons = document.querySelectorAll(".btn");
	console.log(buttons)
	for(let button of buttons){
		button.onclick = () => {
			let ticketDict = {orderId: button.id};
			completedOrder(ticketDict);
			document.querySelector(".ticket"+button.id).remove();
			ordersCount = document.querySelectorAll(".ticket").length
			document.querySelector(".orders-count").innerHTML = "There are currently " + ordersCount + " orders";
		}
	}
});