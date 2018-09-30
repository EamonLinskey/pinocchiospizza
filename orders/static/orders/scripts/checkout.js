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

function sendOrder(data){
	$.ajax({
	    url: '/sendOrder',
	    dataType: "text json",
	    type: "POST",
	    data: data,
	    success: function(jsonObject,status) {
	    	console.log(jsonObject)
	        console.log("function() ajaxPost : " + status);
	    }
	});
}

function isNumberKey(evt)
      {
      	console.log("here")
      	console.log(evt.which)
         let charCode = (evt.which) ? evt.which : event.keyCode
         console.log(charCode)
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            evt.preventDefault();
      }

document.addEventListener("DOMContentLoaded", function(event) {
	console.log(document.querySelector(".submit"))

	document.querySelector(".submit").onclick = () => {
		console.log("sent")
		let [address, aptNum, city, zipCode, delInst, phone] = document.querySelectorAll(".input")
		console.log(address)
		let payment = document.querySelector('input[name = "payment"]:checked'); 
		
		let orderInfo = { 	order: localStorage.getItem("order"),
							address: address.value,
							aptNum: aptNum.value,
							city: city.value,
							zipCode: zipCode.value,
							delInst: delInst.value,
							phone: phone.value,
							payment: payment.value
					}
		console.log(orderInfo)
		sendOrder(orderInfo);
	}

	document.querySelector(".phone, .zip-code").onkeypress = (event) =>{
		isNumberKey(event);
	}
})









