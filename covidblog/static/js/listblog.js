// animation effect

$(document).ready((e) => {
	$(".col-md-4").hover(function(){
		$(this).animate({
			marginTop: "-=50px",
		},200)
	},
	function(){
		$(this).animate({
			marginTop:"+=50px"
		},200)
	}
	)
})