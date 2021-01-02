$(document).ready(function(){
    $(".Namaberita img").hover(function(){
      $(this).animate({
          height: "300px",
          width: "300px",
      },10);
      }, function(){
      $(this).animate({
          height: "250px",
          width:"250px",
      },10);
    });
  });

$(document).ready(function(){
  const pk = window.location.href.split("/")[5].split("?")[0];
  $.ajax({
    url: '/covidnews/getAllComment/'+pk,
    success: (data) =>{
      for(let i = data.length-1;i>=0;i--){
        var nama= data[i].fields.nama;
        var komentar = data[i].fields.komentar
        $(".listkomen").append('<div class="namakomentar"><p><u>'+nama+'</u></p></div><div class="isikomentar"><p>'+komentar+'</p></div>'
        );
      }
    } 
  })
})

$("#formkomentar").on('submit',(e)=>{
  e.preventDefault();
  let pk = window.location.href.split("/")[5].split("?")[0];
  const nama = $("#nama").val();
  const komentar= $("#komentar").val();

  if(nama!=''&& komentar!=''){
    $.ajax({
      url: '/covidnews/postComment/'+pk,
      type: "POST",
      data:{
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        'nama':nama,
        'komentar': komentar,
        'pk':pk
      },
      success: (e)=>{
        $("#nama").val("");
        $("#komentar").val("");
        $(".listkomen").empty();
        for (let index = e.length-1; index>=0; index--) {
          var nama = e[index].fields.nama;
          var komentar =e[index].fields.komentar;
          $(".listkomen").append('<div class="namakomentar"><p><u>'+nama+'</u></p></div><div class="isikomentar"><p>'+komentar+'</p></div>');  
        }
      }
    })
  }
})
