$(function() {
	$('#navigation ul li:first-child').addClass('first');
	$('.footer-nav ul li:first-child').addClass('first');

	$('#navigation a.nav-btn').click(function(){
		$(this).closest('#navigation').find('ul').slideToggle()
		$(this).find('span').toggleClass('active')
		return false;
	})
    var navTitle = $('#navigation > a').text();
    $('#navigation ul li a').each(function(){
        if ($(this).text() == navTitle)
        {
            $(this).addClass('active');
            return false;
        }
    });
});

$(window).load(function() {
	$('.flexslider').flexslider({
		animation: "slide",
		controlsContainer: ".slider-holder",
		slideshowSpeed: 5000,
		directionNav: false,
		controlNav: true,
		animationDuration: 2000,
		before:function( slider ){
			$('.img-holder').animate({'bottom' : '-30px'},300)
		},

		after:function( slider ){
			$('.img-holder').animate({'bottom' : '0px'},300)
		}
	});
});