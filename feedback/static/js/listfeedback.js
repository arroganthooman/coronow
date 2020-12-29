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

                html += '<div class="singles">';
                html += '<p>' + nama + '</p>';
                html += '<p>' + email + '</p>';
                html += '<p>' + isi + '</p>';
                html += '</div>';

                $('#isi').append(html);
            }
            $('#isi').slick({
                mobileFirst: true,
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: true,
                autoplaySpeed: 2000,
                dots: true,
                
            });
        },
        
        error: function(error) {
            console.log(error);
        }
    });
});