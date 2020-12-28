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
            console.log(data);
            console.log("success");
        },

        error: function (error) {
            console.log(error);
        }
    });
};