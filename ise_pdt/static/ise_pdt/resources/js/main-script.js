$('.click-to-collapse').on('click', function(e) {
  var hello = $('.click-to-collapse').index(this);

  $('.project-nav-div').eq(hello).toggleClass("show");

  if ($('.click-to-collapse i').eq(hello).hasClass('ion-ios-arrow-right')) {
    $('.click-to-collapse i').eq(hello).removeClass('ion-ios-arrow-right');
    $('.click-to-collapse i').eq(hello).addClass('ion-ios-arrow-down');
  } else {
    $('.click-to-collapse i').eq(hello).removeClass('ion-ios-arrow-down');
    $('.click-to-collapse i').eq(hello).addClass('ion-ios-arrow-right');
  }
});
