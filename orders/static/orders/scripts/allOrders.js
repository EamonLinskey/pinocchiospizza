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
			let ticketId = button.classList[2]
			let ticketDict = {orderId: button.classList[2]};
			completedOrder(ticketDict);
			document.querySelector(".ticket"+ticketId).remove();
			ordersCount = document.querySelectorAll(".ticket").length
			document.querySelector(".orders-count").innerHTML = "There are currently " + ordersCount + " orders";
		}
	}
});