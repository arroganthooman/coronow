// const imgBody = document.querySelector('.isi-blog .body .blog-body img')
// imgBody.setAttribute('class', 'img-fluid');
// imgBody.removeAttribute('style');
if (window.innerWidth <= 576) {
	const section = document.querySelector('section .isi-blog');
	section.classList.replace('container', 'container-fluid');
}


// Display all Comment with ajax
$(document).ready(function() {
	const pk = window.location.href.split("/")[5].split("?")[0];
	$.ajax({
		url:'/covidBlog/getAllComment/' + pk,
		success: (e) => {
			for (let i = e.length-1; i>=0; i--) {
				$(".list-komen").append(
					`<div class="row">
						<div class="col-auto nama-komentar">
							<span style="z-index:99;" class="spanNama" id=${e[i].pk}>${e[i].fields.nama}</span>
						</div>
					</div>
					
					<div class="row">
						<div class="col-auto komentar-orang">
							${e[i].fields.post_date}<br><br>
							${e[i].fields.komentar}
						</div>
					</div>`
				);
			}
		}
	})
})

// Comment AJAX
$(".postComment").on('submit', (e) => {
	e.preventDefault();
	let pk = window.location.href.split("/")[5].split("?")[0];
	const nama = $("#nama").val();
	const komentar = $("#komentar").val();
	console.log($("input[name=csrfmiddlewaretoken]").attr("value"));

	if (nama !='' && komentar != '') {
	$.ajax({
		url:'/covidBlog/postComment/' + pk,
		type:"POST",
		data: {
			'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
			'nama':nama,
			'komentar': komentar,
			'pk':pk
		},
		success: (e) => {
			$("#nama").val("");
			$("#komentar").val("");
			console.log(e);

			$(".list-komen").empty();
			for (let i=e.length-1; i>=0; i--) {
				$(".list-komen").append(
					`<div class="row">
						<div class="col-auto nama-komentar">
							<span style="z-index:99;" class="spanNama" id=${e[i].pk}>${e[i].fields.nama}</span>
						</div>
					</div>
					
					<div class="row">
						<div class="col-auto komentar-orang">
							${e[i].fields.post_date}<br><br>
							${e[i].fields.komentar}
						</div>
					</div>`
				)
			}
		}
	})
}
})