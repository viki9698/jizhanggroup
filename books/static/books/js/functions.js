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


