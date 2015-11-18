var new_time = 0;

$(document).ready(function(){
	//to check whether we should redirect the user to individual task rather than the main page
	check_url_target();
	
	//holding the setInterval event
	var timer_event;
	var start_time = 0;
	var end_time = 0;
	// store the total time spent of each task
	localStorage.setItem("total_time_dev", 0);
	localStorage.setItem("total_time_def", 0);
	localStorage.setItem("total_time_man", 0);
	// store the current task working on 
	localStorage.setItem("location", "");
	// to record whether the most recent time record has been added to total time, in order to avoid double calculation when switching tab
	localStorage.setItem("time_saved", "true"); 
	
	$('.project-tab').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('.project-tab').removeClass('current');
		$('.tabbed-div').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
	})
	
	$("#start_button_dev").click(function(){
		localStorage.setItem("location", "_dev");
		start_onclick();
	})
	
	$("#start_button_def").click(function(){
		localStorage.setItem("location", "_def");
		start_onclick();
	})
	
	$("#start_button_man").click(function(){
		localStorage.setItem("location", "_man");
		start_onclick();
	})
	
	$("#pause_button_dev").click(function(){
		pause_onclick();
	});
	
	$("#pause_button_def").click(function(){
		pause_onclick();
	});
	
	$("#pause_button_man").click(function(){
		pause_onclick();
	});
	
	$('.change_page').on("click", function() {  
        pause_onclick();
    });	
	

})

function check_url_target(){
	var url_target = location.search.split('task=')[1] ? location.search.split('task=')[1] : 'main';
	console.log(url_target);
	
	if (url_target != "main"){
		
		$("#main_tab").removeClass("current");
		$("#dev_tab").removeClass("current");
		$("#def_tab").removeClass("current");
		$("#man_tab").removeClass("current");
		$("#"+url_target+"_tab").addClass("current");
		
		$("#main").removeClass("current");
		$("#development").removeClass("current");
		$("#defect").removeClass("current");
		$("#management").removeClass("current");
		switch (url_target){
			case "dev":
				$("#development").addClass("current");
				break;
			case "def":
				$("#defect").addClass("current");
				break;
			case "man":
				$("#management").addClass("current");
				break;
		}
	}
}

function start_onclick(){
	start_time = new Date().valueOf();
	var location = localStorage.getItem("location");
	localStorage.setItem("time_saved","false");
	//localStorage.setItem("current_time", 0);
	$("#pause_button"+location).prop('disabled',false);
	$("#start_button"+location).prop('disabled',true);
	timer_event = setInterval(start_timer, 1000);
}

function start_timer(){
	var location = localStorage.getItem("location");
	//var new_time = localStorage.getItem("current_time");
	new_time = parseInt(new_time) + 1;
	//localStorage.setItem("current_time", new_time);
	if (new_time < 60)
		$("#time_record"+location).html("00:00:"+pad(new_time,2));
	else if (new_time < 3600)
		$("#time_record"+location).html("00:"+pad(Math.floor(new_time/60),2)+":"+pad(new_time%60,2));
		else
			$("#time_record"+location).html(pad((Math.floor(new_time/3600),2))+":"+pad(Math.floor((new_time%3600)/60),2)+":"+pad(new_time%60,2));
}

function pause_onclick(){
	var location = localStorage.getItem("location");
	clearInterval(timer_event);
	new_time = 0;
	
	if (localStorage.getItem("time_saved") == "false"){
		end_time = new Date().valueOf();
		var time_to_add = Math.floor((end_time - start_time)/1000);
		
		//var time_to_add = parseInt(localStorage.getItem("current_time"));
		var temp_total_time = parseInt(localStorage.getItem("total_time"+location));
		temp_total_time = temp_total_time + time_to_add;
		localStorage.setItem("total_time"+location, temp_total_time);
		// SEND temp_total_time to Database
		if (temp_total_time < 60)
			$("#total_time_record"+location).html("00:00:"+pad(temp_total_time,2));
		else if (temp_total_time < 3600)
			$("#total_time_record"+location).html("00:"+pad(Math.floor(temp_total_time/60),2)+":"+pad(temp_total_time%60,2));
			else
				$("#total_time_record"+location).html(pad((Math.floor(temp_total_time/3600),2))+":"+pad(Math.floor((temp_total_time%3600)/60),2)+":"+pad(temp_total_time%60,2));
	}
	
	$("#start_button"+location).prop('disabled',false);
	$("#pause_button"+location).prop('disabled',true);
	$("#time_record"+location).html("00:00:00");
	
	localStorage.setItem("time_saved","true");
}
/*
function save_and_clear(){
	var location = localStorage.getItem("location");

	clearInterval(timer_event);
	new_time = 0;
	end_time = new Date().valueOf();
	var time_to_add = Math.floor((end_time - start_time)/1000);
	var temp_total_time = parseInt(localStorage.getItem("total_time"+location));
	temp_total_time = temp_total_time + time_to_add;
	localStorage.setItem("total_time"+location, temp_total_time);
	
	$("#start_button"+location).prop('disabled',false);
	$("#pause_button"+location).prop('disabled',true);
	$("#time_record"+location).html("00:00:00");
}
*/

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
