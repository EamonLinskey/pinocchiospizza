function isNumberKey(evt){
	// Prevents nonnumeric inputs (also allows backspace and enter)
	let charCode = (evt.which) ? evt.which : event.keyCode
		if (charCode > 31 && (charCode < 48 || charCode > 57))
			evt.preventDefault();
}

document.addEventListener("DOMContentLoaded", function(event) {
	// Initialize values
	let cardRadio = document.querySelector(".credit-card")
	let cashRadio = document.querySelector(".cash")

	/*
	// Initial acts as a switch preventing Add stripe from being executed
	// multiple times if the user toggles their payment back and forth
	// AddStripe could be called on page load but it messes with
	// the default stripe animation so this work around is better visuslly
	*/
	let initial = true

	// Append order to form
	document.querySelector(".submit-cash").onclick = () => {
		orderHandeler()
		document.getElementById('payment-form').submit()
	}

	// Prevent alphabetic inputs in number fields
	let needsNums = document.querySelectorAll(".phone, .zip-code")
	for(let num of needsNums){
		num.onkeypress = (event) =>{
			isNumberKey(event);
		}
	}

	// Toggle Display and add stripe if it is the first click
	cardRadio.onclick = function() {
		if(initial){
			addStripe()
			initial = false
		}
		document.querySelector('.stripe-section').style.display = "block"
		document.querySelector('.payment-submit').style.display = "none"
	}

	// Toggle Display	
	cashRadio.onclick = function() {
		document.querySelector('.stripe-section').style.display = "none"
		document.querySelector('.payment-submit').style.display = "block"
	}


})

// Adds the users order to the from to submit to server
function orderHandeler(){
	let form = document.getElementById('payment-form');
	let hiddenOrder = document.createElement('input');
	hiddenOrder.setAttribute('type', 'hidden');
	hiddenOrder.setAttribute('name', 'hidden-order');
	hiddenOrder.setAttribute('value', localStorage.order);
	form.appendChild(hiddenOrder);
}

// From Stripes documentation, edited for my pruposes
function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  let form = document.getElementById('payment-form');
  let hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}

function addStripe(){
	// Create a Stripe client.
	var stripe = Stripe('pk_test_Nu9EpzKBLqT4FpVuepo0pCc9');

	// Create an instance of Elements.
	var elements = stripe.elements();

	// Custom styling can be passed to options when creating an Element.
	// (Note that this demo uses a wider set of styles than the guide below.)
	var style = {
		base: {
			color: '#32325d',
			lineHeight: '18px',
			fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
			fontSmoothing: 'antialiased',
			fontSize: '16px',
			'::placeholder': {
			color: '#aab7c4'
			}
		},
		invalid: {
			color: '#fa755a',
			iconColor: '#fa755a'
			}
	};

	// Create an instance of the card Element.
	var card = elements.create('card', {style: style});

	// Add an instance of the card Element into the `card-element` <div>.
	card.mount('#card-element');

	// Handle real-time validation errors from the card Element.
	card.addEventListener('change', function(event) {
		var displayError = document.getElementById('card-errors');
		if (event.error) {
			displayError.textContent = event.error.message;} 
		else {
			displayError.textContent = '';
		}
	});

	// Handle form submission.
	var form = document.getElementById('payment-form');
		form.addEventListener('submit', function(event) {
		event.preventDefault();

		stripe.createToken(card).then(function(result) {
			if (result.error) {
				// Inform the user if there was an error.
				var errorElement = document.getElementById('card-errors');
				errorElement.textContent = result.error.message;
			} else {
				// Send the token to your server.
				orderHandeler();
				stripeTokenHandler(result.token);
			}
		});
	});
}











