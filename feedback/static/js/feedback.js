$('#sub').on('submit', function (event) {
    event.preventDefault();
    console.log("submitted");
    savefeedback();
});

function savefeedback() {
    console.log("save feedback bisa");
    $.ajax({
        url: "savefeedback/",
        type: "POST",
        data:
        {
            nama: $('#nama').val(),
            email: $('#email').val(),
            isi: $('#isi').val(),
            csrfmiddlewaretoken: window.CSRF_TOKEN
        },
        success: function (data) {
            $('#nama').val('');
            $('#email').val('');
            $('#isi').val('');
            console.log(data);
            console.log("success");

            var html = "";
            html += '<div class="alert alert-success" style="text-align: center;">';
            html += 'Terima kasih telah mengirim feedback!';
            html += '</div>';
            $('#respons').append(html);
        },

        error: function (error) {
            var html = "";
            html += '<div class="alert alert-warning" style="text-align: center;">';
            html += 'Oops! Terdapat error saat mengirim feedback';
            html += '</div>';
            console.log(error);
        }
    });
};

$('.submit-button').mouseenter( function(){ 
    $(this).css('background-color','#3d6869');
}).mouseleave(function() {
    $(this).css('background-color','#4F8A8B');
});