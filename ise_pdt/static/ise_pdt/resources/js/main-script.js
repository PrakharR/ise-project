var new_time = 0;
//holding the setInterval event
var timer_event;
var start_time;
var end_time;
var total_time_instance;
var total_project_time_instance;
var overall_total_project_time_instance;
	
$(document).ready(function(){
	localStorage.setItem("time_saved","true");
	//to check whether we should redirect the user to individual task rather than the main page
	localStorage.setItem("location", "");

	start_time = 0;
	end_time = 0;
	// store the total time spent of each task
	var x = parseInt($("#total_dev_time_seconds").html()) + parseInt($("#total_dev_time_minutes").html())*60 + parseInt($("#total_dev_time_hours").html())*3600;
	localStorage.setItem("total_time_dev", x);
	var x = parseInt($("#total_def_time_seconds").html()) + parseInt($("#total_def_time_minutes").html())*60 + parseInt($("#total_def_time_hours").html())*3600;
	localStorage.setItem("total_time_def", x);
	var x = parseInt($("#total_man_time_seconds").html()) + parseInt($("#total_man_time_minutes").html())*60 + parseInt($("#total_man_time_hours").html())*3600;
	localStorage.setItem("total_time_man", x);
	var x = parseInt($("#total_project_time_seconds").html()) + parseInt($("#total_project_time_minutes").html())*60 + parseInt($("#total_project_time_hours").html())*3600;
	localStorage.setItem("total_project_time", x);	
	var x = parseInt($("#overall_total_project_time_seconds").html()) + parseInt($("#overall_total_project_time_minutes").html())*60 + parseInt($("#overall_total_project_time_hours").html())*3600;
	localStorage.setItem("overall_total_project_time", x);
	// store the current task working on 
	// to record whether the most recent time record has been added to total time, in order to avoid double calculation when switching tab
  
    
	
	$('.project-tab').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('.project-tab').removeClass('current');
		$('.tabbed-div').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
	})
    
    $('.project-summary-tab').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('.project-summary-tab').removeClass('current');
		$('.tabbed-summary-div').removeClass('current');

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
	
	$("#dev_tab").click(function(){
		localStorage.setItem("location", "_dev");
		start_onclick()
	})
	
	$("#def_tab").click(function(){
		localStorage.setItem("location", "_def");
		start_onclick()
	})
	
	$("#man_tab").click(function(){
		localStorage.setItem("location", "_man");
		start_onclick()
	})
	
	//check_url_target();
	check_url_target_2();

	window.onbeforeunload = function(){
		pause_onclick();
	}
})

function check_url_target_2(){
	var url_target = location.search.split('task=')[1] ? location.search.split('task=')[1] : 'main';
	
	if (url_target != "main"){
		switch (url_target){
			case "dev":
				$("#dev_tab").click();
				break;
			case "def":
				$("#def_tab").click();
				break;
			case "man":
				$("#man_tab").click();
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
	
	total_time_instance = localStorage.getItem("total_time"+location);
	total_project_time_instance = localStorage.getItem("total_project_time");
	overall_total_project_time_instance = localStorage.getItem("overall_total_project_time");
	
	
	timer_event = setInterval(start_timer, 1000);
}

function start_timer(){
	var location = localStorage.getItem("location");
	//var new_time = localStorage.getItem("current_time");
	new_time = parseInt(new_time) + 1;
	total_time_instance = parseInt(total_time_instance) + 1;
	total_project_time_instance = parseInt(total_project_time_instance) + 1;
	overall_total_project_time_instance = parseInt(overall_total_project_time_instance) + 1;
	
	//localStorage.setItem("current_time", new_time);
	if (new_time < 60)
		$("#time_record"+location).html("00:00:"+pad(new_time,2));
	else if (new_time < 3600)
		$("#time_record"+location).html("00:"+pad(Math.floor(new_time/60),2)+":"+pad(new_time%60,2));
		else
			$("#time_record"+location).html(pad((Math.floor(new_time/3600),2))+":"+pad(Math.floor((new_time%3600)/60),2)+":"+pad(new_time%60,2));
			
	if (total_time_instance < 60)
		$("#total"+location+"_time_seconds").html(pad(total_time_instance,2));
	else if (new_time < 3600){
		$("#total"+location+"_time_minutes").html(pad(Math.floor(total_time_instance/60),2));
		$("#total"+location+"_time_seconds").html(pad(total_time_instance%60,2));
	}
		else{
			$("#total"+location+"_time_hours").html(pad(Math.floor(total_time_instance/3600),2));
			$("#total"+location+"_time_minutes").html(pad(Math.floor(total_time_instance%3600/60),2));
			$("#total"+location+"_time_seconds").html(pad(total_time_instance%60,2));			
		}

		
	if (total_project_time_instance < 60)
		$("#total_project_time_seconds").html(pad(total_project_time_instance,2));
	else if (new_time < 3600){
		$("#total_project_time_minutes").html(pad(Math.floor(total_project_time_instance/60),2));
		$("#total_project_time_seconds").html(pad(total_project_time_instance%60,2));
	}
		else{
			$("#total_project_time_hours").html(pad(Math.floor(total_project_time_instance/3600),2));
			$("#total_project_time_minutes").html(pad(Math.floor(total_project_time_instance%3600/60),2));
			$("#total_project_time_seconds").html(pad(total_project_time_instance%60,2));			
		}
		
		
	if (overall_total_project_time_instance < 60)
		$("#overall_total_project_time_seconds").html(pad(overall_total_project_time_instance,2));
	else if (new_time < 3600){
		$("#overall_total_project_time_minutes").html(pad(Math.floor(overall_total_project_time_instance/60),2));
		$("#overall_total_project_time_seconds").html(pad(overall_total_project_time_instance%60,2));
	}
		else{
			$("#overall_total_project_time_hours").html(pad(Math.floor(overall_total_project_time_instance/3600),2));
			$("#overall_total_project_time_minutes").html(pad(Math.floor(overall_total_project_time_instance%3600/60),2));
			$("#overall_total_project_time_seconds").html(pad(overall_total_project_time_instance%60,2));			
		}		
		
}

function pause_onclick(){
	var location = localStorage.getItem("location");
	clearInterval(timer_event);
	new_time = 0;
	
	if (localStorage.getItem("time_saved") == "false"){
		end_time = new Date().valueOf();
		var time_to_add = Math.floor((end_time - start_time)/1000);
		
		var DataVals = { 
			
			user : $("#user_hidden").val(), 
			project : $("#project_hidden").val(), 
			
			time_worked : time_to_add, 
			work_type : (location.substring(1)).toUpperCase()
		}

		$.ajax({
			  type: 'POST',
			  url: "/ise_pdt/logtime",
			  data: DataVals,
			  dataType: "text",
			  async: false,
			  success: function() {}
		});		
		
		//var time_to_add = parseInt(localStorage.getItem("current_time"));
		var temp_total_time = parseInt(localStorage.getItem("total_time"+location));
		temp_total_time = temp_total_time + time_to_add;
		localStorage.setItem("total_time"+location, temp_total_time);
		
		localStorage.setItem("total_project_time", total_project_time_instance);
		localStorage.setItem("overall_total_project_time", overall_total_project_time_instance);
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

function delete_project_prompt() {
  
  var user = document.getElementById("userjs").value;
  var project = document.getElementById("projectjs").value;
  
  if(confirm("Are you sure you want to delete this project?")) {
    window.location="/ise_pdt/manager/"+user+"/"+project+"/deleteproject/";
  } else {
      // do something
  }
  
}

function delete_iteration_prompt() {
  
  var user = document.getElementById("userjs_i").value;
  var project = document.getElementById("projectjs_i").value;
  var iteration = document.getElementById("iterationjs").value;
  
  if(confirm("Are you sure you want to delete this iteration?")) {
    window.location="/ise_pdt/manager/"+user+"/"+project+"/"+iteration+"/deleteiteration/";
  } else {
      // do something
  }
  
}


