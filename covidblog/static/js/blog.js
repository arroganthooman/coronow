const imgBody = document.querySelector('.isi-blog .body .blog-body img')
imgBody.setAttribute('class', 'img-fluid');
imgBody.removeAttribute('style');

if (window.innerWidth <= 576) {
	const section = document.querySelector('section .isi-blog');
	section.classList.replace('container', 'container-fluid');
}