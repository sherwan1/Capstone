var curr_chat;
var profile_photo;


$( document ).ready(function() {


    $('#select_file_button').click(function () {
    $("input[type='file']").trigger('click');
    });

    $("input[type='file']").change(function () {
    $('#val1').text(this.value.replace(/C:\\fakepath\\/i, ''))
    });

    profile_photo= $("#profile-img").attr('src');
    $("#btn-file-remove").on('click', function(e){

           var $el = $('#id_file');
           $el.wrap('<form>').closest('form').get(0).reset();
           $el.unwrap();
    });


    function send_file_function(){
      //$( "#file_form" ).submit();

        //check if no file is entered here
        var form = $('#file_form')[0]; // You need to use standard javascript object here

        if(form[1].files.length == 0){

           // alert("No file selected to send!!");
            return;
        }


        var formData = new FormData(form);

        formData.append("msg_To", curr_chat);


            $.ajax( {
              url: "/send_message_file",
              type: 'POST',
              data: formData,
              processData: false,
              contentType: false,

              success: function(json) {
                                //location.reload(true);
                                //increment the like number in the Like button]
                                //alert("Got 200 response")
                                console.log("Got a positive response from server");
                                //delete bell
                                //alert("url returned is "+ json.file_url);
                                  //
                                $('<li class="sent"><img src="'+profile_photo+'" alt="" /><p> <a href="'+json.file_url+'"> ' + form[1].files[0].name + ' </a> </p></li>').appendTo($(".messages[person = '"+curr_chat+"'] ul"));
                                $('.message-input input').val(null);
                                $('.contact.active .preview').html('<span>You: </span>' + '<a href="url returned by server"> ' + form[1].files[0].name + ' </a>');
                                $(".messages").animate({ scrollTop: $(document).height() }, "fast");


                                //location.reload(true);
                             },
            } );

      };

    $(".messages").animate({ scrollTop: $(document).height() }, "fast");

$("#profile-img").click(function() {
	$("#status-options").toggleClass("active");
});

$(".expand-button").click(function() {
  $("#profile").toggleClass("expanded");
	$("#contacts").toggleClass("expanded");
});

$("#chat-btn").click(function() {
  $("#frame").slideToggle();
  $("#chatbar").removeClass("hidden");
  $("#frame").removeClass("hidden");
});


$("#status-options ul li").click(function() {
	$("#profile-img").removeClass();
	$("#status-online").removeClass("active");
	$("#status-away").removeClass("active");
	$("#status-busy").removeClass("active");
	$("#status-offline").removeClass("active");
	$(this).addClass("active");
	
	if($("#status-online").hasClass("active")) {
		$("#profile-img").addClass("online");
	} else if ($("#status-away").hasClass("active")) {
		$("#profile-img").addClass("away");
	} else if ($("#status-busy").hasClass("active")) {
		$("#profile-img").addClass("busy");
	} else if ($("#status-offline").hasClass("active")) {
		$("#profile-img").addClass("offline");
	} else {
		$("#profile-img").removeClass();
	};
	
	$("#status-options").removeClass("active");
});

function msgRead(chat_selected, msgType) {
      var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();


            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
                     $.ajax({
                          type:"POST",
                          data: {'notification_by':chat_selected, 'msgType':msgType},  //We send the server the postID and the comment itself
                          url:"/delete_msg_notification" ,
                          async:true,
                          dataType: "json",

                         success: function(json) {
                                //location.reload(true);
                                //increment the like number in the Like button]
                                //alert("Got 200 response")
                                console.log("Got a positive response from server");
                                //delete bell
                                 $(".bell-ring[person = '"+chat_selected+"']").remove();

                                //location.reload(true);
                             },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
            });

}


function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 }



function sendMessageToServer(message) {
     var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();


            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
                     $.ajax({
                          type:"POST",
                          data: {'msgTo':curr_chat, 'msgText':message},  //We send the server the postID and the comment itself
                          url:"/send_message" ,
                          async:true,
                          dataType: "json",

                         success: function(json) {
                                //location.reload(true);
                                //increment the like number in the Like button]
                                //alert("Got 200 response")
                                console.log("Got a positive response from server");

                                //location.reload(true);
                             },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
            });

}

function newMessage() {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
	    send_file_function();
		return false;
	}
	$('<li class="sent"><img src="'+profile_photo+'" alt="" /><p>' + message + '</p></li>').appendTo($(".messages[person = '"+curr_chat+"'] ul"));
	$('.msg_input_txt').val(null);
	$('.contact.active .preview').html('<span>You: </span>' + message);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");

	sendMessageToServer(message);
	send_file_function();
};

$('.submit').click(function() {
  newMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    newMessage();
    return false;
  }
});
//# sourceURL=pen.js

$('.contact').click(function () {

    $(".messages[person = '"+curr_chat+"']").addClass("hidden");

    var new_Chat = $(this).attr('person');

    $(".contact-name-top").text(new_Chat);

    var imgsrc= $(".contact_photo[person = '"+new_Chat+"']").attr('src');


    $(".contact-img-top").attr("src",imgsrc);

    $(".messages[person = '"+new_Chat+"']").removeClass("hidden");

    curr_chat=new_Chat;

    //when the contact is clicked and window is in focus then the user has seen the message
    //now we need to delete the notification for this chat_room on the server side and remove
    //the bell from client side
    msgRead(curr_chat, "delete_notification");
})



	//Logic to handle search and filter for search contacts in message box

	$( "#search_box" ).keyup(function() {

			  var input, filter, outerDiv, li, span, i, str;
				input = document.getElementById("search_box");
				filter = input.value.toUpperCase();

				outerDiv = document.getElementById("contacts");
				li = outerDiv.getElementsByClassName("contact");
				//alert("number of friends are " + li.length);
				for (i = 0; i < li.length; i++) {
					str = li[i].getElementsByTagName("p")[0];
					span = li[i].getElementsByTagName("p")[0];

					if ((span.innerHTML.toUpperCase().indexOf(filter) > -1) || str.innerHTML.toUpperCase().indexOf(filter) > -1) {
						li[i].style.display = "";
					} else {
						li[i].style.display = "none";

					}
				}
	});


});
