function changeArrow($element) {
    if ($element.hasClass('fa-chevron-down')) {
        $element.removeClass('fa-chevron-down');
        $element.addClass('fa-chevron-up');
    } else {
        $element.removeClass('fa-chevron-up');
        $element.addClass('fa-chevron-down');
    }
}

$('#favorites-nav').on('click',()=>{
    $('#favorites-section').slideToggle();
    changeArrow($('#favorites-arrow'));
});

$('#completed-nav').on('click',()=>{
    $('#completed-section').slideToggle();
    changeArrow($('#completed-arrow'));
});

$('#reviews-nav').on('click',()=>{
    $('#reviews-section').slideToggle();
    changeArrow($('#reviews-arrow'));
});

$('#photos-nav').on('click',()=>{
    $('#photos-section').slideToggle();
    changeArrow($('#photos-arrow'));
});