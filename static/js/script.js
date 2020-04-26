let el = document.getElementById('people-indicator');
let input_range = document.getElementById('input-range')

input_range.addEventListener("input", 
	function() { el.innerHTML = input_range.value })