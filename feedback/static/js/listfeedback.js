// Display all Comment with ajax
$(document).ready(function() {
	$.ajax({
		url:'/feedback/data/',
		success: function(data) {
            console.log(data);
        },
        
        error: function(error) {
            console.log(error);
        }
	});
});