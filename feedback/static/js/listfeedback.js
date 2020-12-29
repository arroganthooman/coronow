// Display all Comment with ajax
$(document).ready(function() {
	$.ajax({
		url:'/feedback/data/',
		success: function(data) {
            console.log(data)
            for (i = 0; i < data.length; i++) {
                var html = "";
                nama = data[i].fields.nama;
                email = data[i].fields.email;
                isi = data[i].fields.isi;

                html += '<div class="singles col-xl-4 col-lg-4 col-md-3">';
                html += '<p>' + nama + '</p>';
                html += '<p>' + email + '</p>';
                html += '<p>' + isi + '</p>';

                $('#isi').append(html);
            }
        },
        
        error: function(error) {
            console.log(error);
        }
	});
});