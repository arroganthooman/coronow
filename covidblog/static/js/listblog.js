// animation effect
$(document).ready((e) => {
	$(".card").hover(function(){
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