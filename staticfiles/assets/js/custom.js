$(function () {

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > 10) {
            $('.navnavhome').addClass('active');
        } else {
            $('.navnavhome').removeClass('active');
        }
    });

    // $('#home').click(function () {
    //     $('#home').attr('class', 'active')
    //     console.log("home")
    // })

});