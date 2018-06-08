
var ws;  //websocket global variable
var findChat;
// Accordion
var profile_pic;

		function send_message() {



		message = $("#sendmessage input").val();

        if($.trim(message) == '') {
		 
            return false;
	    }

		$(".chatmessages[data-person = '"+findChat+"']").append(
			`
			
                    <div class="message w3layouts">
						<img src="${profile_pic}">
						<div class="bubble">
							${message}
						</div>
					</div>
			
			`

		);


	    $("#sendmessage input").val("");

	    //The below line is to make sure that whenever the newmsg comes we scroll to the bottom
		//$(".chatmessages[data-person = '"+findChat+"']").animate({ scrollTop: $('.endOfMsg').offset().top }, 'slow');

		var height = $(".chatmessages[data-person = '"+findChat+"']").prop('scrollHeight');
		$(".chatmessages[data-person = '"+findChat+"']").animate({ scrollTop: height }, 'slow');


		//Now we finally send the message to the chatServer

		  var json= {
		  	"msgType":"message",
			  "text": message,
			  "msgTo" : findChat
		  };
		  var string = JSON.stringify(json); //the data needs to converted from json to string before sending to server
		  ws.send(string);

		  	//save chat history in local browser storage to have persistence of messages
			//for the current session as we are not storing any chat messages in the
			//chat server. So if dont store it locally then on a page reload the chat
			//History will be gone which we dont want to happen.

			//alert("sending msg to : " + findChat);
			localStorage.setItem("chatHistory-"+findChat, $(".chatmessages[data-person = '"+findChat+"']").html());
			console.log("set the chatHistory after sending message");


        //newMessage();
    		return false;


        }

		function onlineStatusList(friendList) {
			console.log("inside status list function" + friendList[0] + " len is " + friendList.length);

			var i;

			for (i=0; i<friendList.length; i++){
				 $(".status[person='"+friendList[i]+"']").removeClass("inactive");
                 $(".status[person='"+friendList[i]+"']").addClass("available");
			}
			return;
        }
		function updateStatusSingle(status,friendEmail){

			console.log("inside updatestatusSingle function and friend email is " + friendEmail);


			if(status== "online") {
				console.log("status was online");
                $(".status[person='"+friendEmail+"']").removeClass("inactive");
                $(".status[person='"+friendEmail+"']").addClass("available");
            }
            if(status== "offline") {
                $(".status[person='"+friendEmail+"']").removeClass("available");
                $(".status[person='"+friendEmail+"']").addClass("inactive");
            }
		}

		function findOnlineFriends(){

			var outerDiv, li;
			var friendsList = [];

			$( ".friend" ).each(function( index ) {
			  friendsList.push($( this ).attr('person')) ;  //push email of each friend into the friendsList array
			});
			//$("#test").attr('bobby')
			//alert("friends are " + friendsList);

			var list=friendsList.toString();
			var packet= {"msgType": "checkOnlineStatus", "listOfFriends" : list};

			ws.send(JSON.stringify(packet));
		}

		function appendMsgToChat(from, text){

			 var friend_img= $(".friend[person = '"+from+"']").children("img").attr('src');
				$(".chatmessages[data-person = '"+from+"']").append(
			`
			
                    <div class="message right agileits">
						<img src="${friend_img}">
						<div class="bubble">
							${text}
						</div>
					</div>
			
			`

		);

		var height = $(".chatmessages[data-person = '"+from+"']").prop('scrollHeight');
		//$(".chatmessages[data-person = '"+from+"']").animate({ scrollTop: $('.endOfMsg').offset().top }, 'slow');
		$(".chatmessages[data-person = '"+from+"']").animate({ scrollTop: height }, 'slow');


		}
        function connect_with_chat_server() {
            $.ajax({
                type: "GET",
                url: "/chat_auth_token",
                async: true,
                dataType: "json",

                success: function (json) {
                    //location.reload(true);
                    //increment the like number in the Like button]
                    //  alert("Got 200 response")
                    console.log("Got the auth token from server");
                    console.log(json);
                    ws = new WebSocket("ws://localhost:8888/ws?token=" + json.token);

                    // Handle incoming websocket message callback
                    ws.onmessage = function (evt) {
                        var msg = JSON.parse(evt.data); //convert string to json obj

                        console.log(msg);
                        //TODO: make sure to check if json object contains the below fields. RIght now im not checking that
                        console.log("Message Received from: " + msg.msgFrom);
                        //alert("message received: " + msg.msgFrom);


                        console.log("Message text is: " + msg.msgText);
                        //alert("message received: " + msg.msgText);

                        if (msg.msgText != "" && msg.msgType == "message") {


                            if(($("#chatbox").css('display') == "none") || ($("#chatview").css('display') == "none") || ($(".chatmessages[data-person = '"+msg.msgFrom+"']").hasClass("hidden1")) ){

                            	      if ($("#new_msg_outer_notification").length == 0) {
											$("#chat-button123").append(
												`<span id="new_msg_outer_notification" class="w3-badge w3-right w3-small w3-green">New</span>`
											)


											localStorage.setItem("new_msg_outer_notification", `<span id="new_msg_outer_notification" class="w3-badge w3-right w3-small w3-green">New Message</span>`);
										}


                            	if($(".new_msg_notification[person= '"+msg.msgFrom+"']").length == 0) {
                                    $(".friend[person = '" + msg.msgFrom + "']").append(
                                        `<span class="new_msg_notification w3-badge w3-right w3-small w3-green" person="${msg.msgFrom}">New</span>`
                                    );


                                    $(".friend[person = '" + msg.msgFrom + "']").prependTo("#friends"); //move the conversation to the top of friends list. This is done to prioritize

                                    localStorage.setItem("new-msg-notification-" + msg.msgFrom, "1");

                                    var count = localStorage.getItem("new-msg-notification-count");

                                    localStorage.setItem("new-msg-notification-count", count + 1);

                                    console.log("set the newmsgnotification in storage after receiving message");
                                }
                                else{
                            		console.log("Notification already exists for this friend. Hence not doing anything")
								}

							}

                            appendMsgToChat(msg.msgFrom, msg.msgText);

                            //save chat history in local browser storage to have persistence of messages
                            //for the current session as we are not storing any chat messages in the
                            //chat server. So if dont store it locally then on a page reload the chat
                            //History will be gone which we dont want to happen. We want session Storage instead of localStorage because of
							//Security reasons. If person A logs in and chats with person B the chat hist is set. Now person A logs out and
							//person C logs in from the same browser (assuming cache and local storage has not been cleared by browser or user A.
							// Then person C chats with person B. Now person C can see the message history between A and B

							//alert("msg is from : " + msg.msgFrom);

                            localStorage.setItem("chatHistory-" + msg.msgFrom, $(".chatmessages[data-person = '" + msg.msgFrom + "']").html());

                            console.log("set the chatHistory after receiving message");
                        }

                        if (msg.msgType == "status_update_singleClient") {
                            updateStatusSingle(msg.status, msg.friendEmail);
                        }
                        if (msg.msgType == "online_status_list") {
                            onlineStatusList(msg.friendList);
                        }


                    };

                    // Close Websocket callback
                    ws.onclose = function (evt) {
                        //console.log("***Connection Closed***");
                       // alert("Connection close");

                    };

                    // Open Websocket callback
                    ws.onopen = function (evt) {
                        //console.log("***Connection Opened123***");

                        //On page reload or a different page load the websocket closes and opens again
                        //Hence we must reload the state of the chat on the previous window if its saved in local storage

                        $(".friend").each(function (index) {
                            var person = $(this).attr('person');  //get person's email

                            if (localStorage.getItem("chatHistory-" + person) != null) {  //see if that person has a chat history. If yes then retrieve it and persist it
                                console.log("retrieved chat history. Now persisting it onto the chatbox");
                                //document.getElementById("chatbox").innerHTML = localStorage.getItem("chatHistory");
                                var hist = localStorage.getItem("chatHistory-" + person);
								$(".chatmessages[data-person = '" + person + "']").html("");

								console.log("Chat history is:" )+hist;

                                $(".chatmessages[data-person = '" + person + "']").html(hist);
								//alert("reloaded page and chat histr");

                            }

                            var innerNewMsgNotification = localStorage.getItem("new-msg-notification-" + person);

                            if (innerNewMsgNotification != null) {

                            	$(".friend[person = '"+person+"']").append(
									`<span class=" new_msg_notification w3-badge w3-right w3-small w3-green" person="${person}">New</span>`

								  );

                            	  $(".friend[person = '"+person+"']").prependTo("#friends"); //move the conversation to the top of friends list. This is done to prioritize

							}

							});

                            var notification = localStorage.getItem("new_msg_outer_notification");
                            if (notification != null) {
                                $("#chat-button123").append(notification);

                            }


                            findOnlineFriends();




                    };
                    /*    error: function(xhr, status, err) {
                        // This time, we do not end up here!
                        alert("error happened and status is");
                        alert(status);

                    }*/
                },
            });
        }

$(document).ready(function(){

	profile_pic= $("#profile_pic123").val();

        connect_with_chat_server();


  var preloadbg = document.createElement("img");
  preloadbg.src = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/245657/timeline1.png";

	$("#searchfield").focus(function(){
		if($(this).val() == "Search contacts..."){
			$(this).val("");
		}
	});
	$("#searchfield").focusout(function(){
		if($(this).val() == ""){
			$(this).val("Search contacts...");

		}
	});

	$("#sendmessage input").focus(function(){
		if($(this).val() == "Send message..."){
			$(this).val("");
		}
	});
	$("#sendmessage input").focusout(function(){
		if($(this).val() == ""){
			$(this).val("Send message...");

		}
	});

	$("#send").click(function(e){
		send_message();
	});

	$("#sendmessage input").on('keydown', function(e) {
    if (e.which == 13) {

    	send_message();

    }
    });





	$(".friend").each(function(){
		$(this).click(function(){
			var childOffset = $(this).offset();
			var parentOffset = $(this).parent().parent().offset();
			var childTop = childOffset.top - parentOffset.top;
			var clone = $(this).find('img').eq(0).clone();
			var top = childTop+12+"px";

			//parts added by me:


			findChat = $(this).attr('person');
			 //$('.innerMsg[person = '+findChat+']').addClass('active-chat');


			//remove new_msg_notification
			$(".new_msg_notification[person = '"+findChat+"']").remove();
			//also remove from localstorage once the message is seen
			localStorage.removeItem("new-msg-notification-"+findChat);
			var count = localStorage.getItem("new-msg-notification-count");

			if(count != null && count > 0) {
                count = count - 1;
                localStorage.setItem("new-msg-notification-count", count);

                if (localStorage.getItem("new-msg-notification-count") == 0) { //if all notifications are gone then remove outer notifcation
                    localStorage.removeItem("new_msg_outer_notification");

                      if($('#new_msg_outer_notification').length){ //if new message notification exists then remove it
                       $('#new_msg_outer_notification').remove();
                   }
                }
            }

			$(clone).css({'top': top}).addClass("floatingImg").appendTo("#chatbox");

			setTimeout(function(){$("#profile p").addClass("animate");$("#profile").addClass("animate");}, 100);
			setTimeout(function(){
				//$('.innerMsg[person = '+findChat+']').addClass("animate");
				//$(".chat-messages[person = '+findChat+']").removeClass("hidden");

				//$(".statuslight[title='" + currentStatus + "']");
				//alert("person is " + findChat);
				//$(".chatmessages[person = 'batman@batman.com']").removeClass('hidden');
				//$(".chatmessages[data-person = '"+findChat+ " ']").removeClass("hidden1");
				$(".chatmessages[data-person = '"+findChat+"']").removeClass("hidden1");
				$(".chatmessages[data-person = '"+findChat+"']").addClass("animate");

				//move the location of scroll box to all the way to the bottom where the new message is
				var height = $(".chatmessages[data-person = '"+findChat+"']").prop('scrollHeight');
				$(".chatmessages[data-person = '"+findChat+"']").animate({ scrollTop: height }, 'slow');


				//$("div[data-person='+findChat+']").removeClass('hidden');
				//$("div[data-person='+findChat+']").addClass('animate');
				$('.cx, .cy').addClass('s1');
				setTimeout(function(){$('.cx, .cy').addClass('s2');}, 100);
				setTimeout(function(){$('.cx, .cy').addClass('s3');}, 200);
			}, 150);

			$('.floatingImg').animate({
				'width': "68px",
				'left':'108px',
				'top':'20px'
			}, 200);

			var name = $(this).find("p strong").html();
			var email = $(this).find("p span").html();
			$("#profile p").html(name );
			$("#profile span").html(email);

			//$(".message").not(".right").find("img").attr("src", $(clone).attr("src"));
			$('#friendslist').fadeOut();
			$('#chatview').fadeIn();



			$('#close').unbind("click").click(function(){
				//$(".chat-messages[person = ' "+findChat+" ']").hide();
				$(".chatmessages[data-person = '"+findChat+"']").addClass("hidden1");
				$(".chatmessages, #profile, #profile p").removeClass("animate");
				$('.cx, .cy').removeClass("s1 s2 s3");
				$('.floatingImg').animate({
					'width': "40px",
					'top':top,
					'left': '12px'
				}, 200, function(){$('.floatingImg').remove()});

				setTimeout(function(){
					$('#chatview').fadeOut();
					$('#friendslist').fadeIn();
				}, 50);
			});

		});
	});


	//Logic to handle search and filter for search contacts in chat box

	$( "#searchfield" ).keyup(function() {

			  var input, filter, outerDiv, li, span, i, str;
				input = document.getElementById("searchfield");
				filter = input.value.toUpperCase();

				outerDiv = document.getElementById("friends");
				li = outerDiv.getElementsByClassName("friend");
				//alert("number of friends are " + li.length);
				for (i = 0; i < li.length; i++) {
					str = li[i].getElementsByTagName("strong")[0];
					span = li[i].getElementsByTagName("span")[0];

					if ((span.innerHTML.toUpperCase().indexOf(filter) > -1) || str.innerHTML.toUpperCase().indexOf(filter) > -1) {
						li[i].style.display = "";
					} else {
						li[i].style.display = "none";

					}
				}
	});


	//prepare and send friendlist to chat server to findout who is online/offline



});