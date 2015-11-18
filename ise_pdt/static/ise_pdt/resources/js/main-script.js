$(document).ready(function(){
	
	var timer_event;
	
	$('.project-tab').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('.project-tab').removeClass('current');
		$('.tabbed-div').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
	})
	
	$("#start_button").click(function(){
		localStorage.setItem("total_time", 0);
		$("#pause_button").prop('disabled',false);
		$("#start_button").prop('disabled',true);
		timer_event = setInterval(start_timer, 1000);
	})
	
	$("#pause_button").click(function(){
		clearInterval(timer_event);
		$("#start_button").prop('disabled',false);
		$("#pause_button").prop('disabled',true);
		$("#time_record").html("0:00:00");
	})
	

})

function start_timer(){
	var new_time = localStorage.getItem("total_time");
	new_time = parseInt(new_time) + 1;
	localStorage.setItem("total_time", new_time);
	if (new_time < 60)
		$("#time_record").html("0:00:"+new_time);
	else if (new_time < 3600)
		$("#time_record").html("0:"+Math.floor(new_time/60)+":"+new_time%60);
}

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
