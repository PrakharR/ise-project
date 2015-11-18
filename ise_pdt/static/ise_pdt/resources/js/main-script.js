var new_time = 0;

$(document).ready(function(){
	
	var timer_event;
	var start_time = 0;
	var end_time = 0;
	localStorage.setItem("total_time", 0);
	
	$('.project-tab').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('.project-tab').removeClass('current');
		$('.tabbed-div').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
	})
	
	$("#start_button").click(function(){
		start_time = new Date().valueOf();
		
		//localStorage.setItem("current_time", 0);
		$("#pause_button").prop('disabled',false);
		$("#start_button").prop('disabled',true);
		timer_event = setInterval(start_timer, 1000);
	})
	
	$("#pause_button").click(function(){
		clearInterval(timer_event);
		new_time = 0;
		
		end_time = new Date().valueOf();
		var time_to_add = Math.floor((end_time - start_time)/1000);
		
		//var time_to_add = parseInt(localStorage.getItem("current_time"));
		var temp_total_time = parseInt(localStorage.getItem("total_time"));
		temp_total_time = temp_total_time + time_to_add;
		localStorage.setItem("total_time", temp_total_time);
		// SEND temp_total_time to Database
		if (temp_total_time < 60)
			$("#total_time_record").html("00:00:"+pad(temp_total_time,2));
		else if (temp_total_time < 3600)
			$("#total_time_record").html("00:"+pad(Math.floor(temp_total_time/60),2)+":"+pad(temp_total_time%60,2));
			else
				$("#total_time_record").html(pad((Math.floor(temp_total_time/3600),2))+":"+pad(Math.floor((temp_total_time%3600)/60),2)+":"+pad(temp_total_time%60,2));
		
		$("#start_button").prop('disabled',false);
		$("#pause_button").prop('disabled',true);
		$("#time_record").html("00:00:00");
	})
	

})

function start_timer(){
	//var new_time = localStorage.getItem("current_time");
	new_time = parseInt(new_time) + 1;
	//localStorage.setItem("current_time", new_time);
	if (new_time < 60)
		$("#time_record").html("00:00:"+pad(new_time,2));
	else if (new_time < 3600)
		$("#time_record").html("00:"+pad(Math.floor(new_time/60),2)+":"+pad(new_time%60,2));
		else
			$("#time_record").html(pad((Math.floor(new_time/3600),2))+":"+pad(Math.floor((new_time%3600)/60),2)+":"+pad(new_time%60,2));
}

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
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
