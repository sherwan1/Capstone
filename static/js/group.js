

         function appendPeople(json) {

                    //clear any previous list before adding new names
                     $(".people_list").empty();
                    for(var i=0; i<json.data.people.length; i++) {


                          $(".people_list").append(`
                          <div class="name">${json.data.people[i]}</div>
                          `);
                    } //end of for loop
        }




        function myFunction(id)
            {
                var x = document.getElementById(id);
                if (x.className.indexOf("w3-show") == -1) {
                    x.className += " w3-show";
                    x.previousElementSibling.className += " w3-theme-d1";
                } else {
                    x.className = x.className.replace("w3-show", "");
                    x.previousElementSibling.className =
                        x.previousElementSibling.className.replace(" w3-theme-d1", "");
                }
            }

        // Used to toggle the menu on smaller screens when clicking on the menu button
        function openNav() {
            var x = document.getElementById("navDemo");
            if (x.className.indexOf("w3-show") == -1) {
                x.className += " w3-show";
            } else {
                x.className = x.className.replace(" w3-show", "");
            }
        }

        function appendPosts(json) {


                    for(var i=0; i<json.data.post_text.length; i++) {
                        $("#Top").append(
                            ` <div class="Post-Comment-box">
                  <div data="${json.data.post_ID[i]}" class="sample post-bar w3-container w3-card-2 w3-white w3-round w3-margin"><br>
                <img src="/w3images/avatar2.png" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:60px">
                <span class="w3-right w3-opacity">1 min</span>
                <h4 class="name">${json.data.post_owner[i]}</h4><br>
                <hr class="w3-clear">
                <p class="text">${json.data.post_text[i]}</p>
                
                 <button type="button" data="${json.data.post_ID[i]}" class="heart-button btn btn-danger btn-circle" style="
     margin-bottom: 15px;" data-toggle="modal" data-target="#myModal"> <i class="glyphicon glyphicon-heart"></i><span> 0 </span></button>


                <button type="button" class="w3-button w3-theme-d1 w3-margin-bottom"><i class="fa fa-thumbs-up"></i>  Like</button>
                <button data="${json.data.post_ID[i]}" type="button" class="comment-button w3-button w3-theme-d2 w3-margin-bottom"><i class="fa fa-comment"></i>  Comment</button>
              </div>

                <!-- Comment Box starts here -->
                 <div  data="${json.data.post_ID[i]}" class="comments comment-bar w3-container w3-card-2 w3-white w3-round w3-margin" ><br>
                    <p contenteditable="true" class="comment_input w3-border w3-padding"></p>
                     <button data="${json.data.post_ID[i]}"type="button" class="comment_submit w3-button w3-theme"><i class="fa fa-pencil"></i>  Comment</button>
                 </div>
                    <!-- Comment Box starts here -->
             </div>`);


                    } //end of for loop




        }
        
        function check_new_post() {
                console.log("running function again");
                 var postID = jQuery("[name=last_postID]").val();
                 console.log("Last post ID is:" + postID);
                 $.ajax({
                          type:"GET",
                          data: {'last_postID': postID, group_id : $("#group_id").val()},
                          url:"/group_check_new_post" , //"https://app.ticketmaster.com/discovery/v2/events/G5diZfkn0B-bh.json?apikey=27mLqO6JmMfWlES8MKnMVG1tkm75I9cE",
                          async:true,
                          dataType: "json",
                          success: function(json) {
                              if(json.status == 0){

                                  //alert(json.data)
                                    console.log("Got nothing")

                              }
                              else{
                                  console.log(json)
                                  //alert(json.data.post_text[0])

                                  //If there are multiple posts in the array we take the last post's ID and quickly set the
                                  // set the Last_postID variable of the html document
                                  jQuery("[name=last_postID]").val(json.data.post_ID[json.data.post_ID.length-1]);

                                   postID = jQuery("[name=last_postID]").val();

                                   console.log("Last post ID is now set to :" + postID);

                                  appendPosts(json);
                              }
                                //location.reload(true);
                              setTimeout('check_new_post()',60000);  //This timer sets the time for the interval between checking for new posts.

                             },
            });

        }



        function register_all_callbacks() {
                function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                  }
                  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

                check_new_post();


                $(document.body).on('click', '.heart-button' ,function(){  //adding this to deal with dynamic posts when added through push notification. If u use the above line then dynamic posts are not handled
                      var postID = $(this).attr('data');
                      //alert("The post ID is: "+postID);
                     //$('.comment-bar[data = '+postID+']').addClass('activate');
                        //alert("LikedBy");
                      $.ajaxSetup({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        }
                    });
                     $.ajax({
                          type:"POST",
                          data: {'postID':postID},  //We send the server the postID and the comment itself
                          url:"/group_likedBy" ,
                          async:true,
                          dataType: "json",

                         success: function(json) {
                                //location.reload(true);
                                //increment the like number in the Like button]
                                //alert("Got 200 response")
                                console.log("Got a positive response from server");
                                console.log(json.data.people[0]);
                                appendPeople(json);
                                //location.reload(true);
                             },

                    });


                    //$(this).slideDown();
                 });



           
                 
                // $(".comment-button").click(function () { //THis code deals with sliding up/down the comment bar when the comment button is pressed
               

                $(".post_submit").click(function () {
                  //alert($("#group_id").val());
                  var group_id = $(this).attr('group_id');
              

                    var text = $('.post_input').text();
                    
                    //text= {'text': text};
                    $.ajaxSetup({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        }
                    });
                     $.ajax({
                          type:"POST",
                          data: {'text': text, 'group_id' : group_id},
                          url:"/group_post_submit" , //"https://app.ticketmaster.com/discovery/v2/events/G5diZfkn0B-bh.json?apikey=27mLqO6JmMfWlES8MKnMVG1tkm75I9cE",
                          async:true,
                          dataType: "json",
                          success: function(json) {
                           
                            location.reload(true);    //dont reload page instead wait for check_new_post function to load the new post
                            
                            },

                    });


                });



                //Comment submit js code:
                 $(document.body).on('click', '.like-button' ,function(){  //adding this to deal with dynamic posts when added through push notification. If u use the above line then dynamic posts are not handled
                      var postID = $(this).attr('data');
                      //alert("The post ID is: "+postID);
                     //$('.comment-bar[data = '+postID+']').addClass('activate');
                       // alert("Liked");
                      $.ajaxSetup({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        }
                    });
                     $.ajax({
                          type:"POST",
                          data: {'like': 1, 'postID':postID},  //We send the server the postID and the comment itself
                          url:"/group_like_post" ,
                          async:true,
                          dataType: "json",

                         success: function(json) {
                                //location.reload(true);
                                //increment the like number in the Like button]
                              //  alert("Got 200 response")
                                 var count= $('.likes_count[data = '+postID+']').text();

                                if(json.data==1) {
                                    count = parseInt(count) + 1;
                                    $('.like-button[data = '+postID+'] span').html(" Liked");

                                }
                                else{
                                    count = parseInt(count) - 1;
                                    $('.like-button[data = '+postID+'] span').html(" Like");
                                }

                                $('.likes_count[data = '+postID+']').html(" "+count);
                             },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
            });


                    //$(this).slideDown();
                 });

                // $(".comment-button").click(function () { //THis code deals with sliding up/down the comment bar when the comment button is pressed
                $(document.body).on('click', '.comment-button' ,function(){  //adding this to deal with dynamic posts when added through push notification. If u use the above line then dynamic posts are not handled
                      var postID = $(this).attr('data');
                    //  alert("The post ID is: "+postID);
                     //$('.comment-bar[data = '+postID+']').addClass('activate');
                     $('.comment-bar[data = '+postID+']').slideToggle();
                     $('.post-bar[data = '+postID+']').addClass('remove-bottom-margin');
                    //$(this).slideDown();
                 });

                $("#pull-down-chat-bar").click(function () {
                    $("#chatbox").slideToggle();//.addClass('hidden');
                });

                $("#chat-button123").click(function () {



                    $("#chatbox").slideToggle();//.removeClass('hidden');
                });



             $(".comment_submit").click(function () {  //when comment is submitted i.e when the button is pressed

                  //  alert("testing");
                    var postID = $(this).attr('data');   //get the post ID first.
                    var text = $('.comment_input').text();  //now get the text inputted in the comment box

                     console.log("text captured is: " +text);
                     console.log("postID captured is: " +postID);
                    //text= {'text': text};
                    $.ajaxSetup({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        }
                    });
                     $.ajax({
                          type:"POST",
                          data: {'text': text, 'postID':postID},  //We send the server the postID and the comment itself
                          url:"/group_comment_submit" ,
                          async:true,
                          dataType: "json",

                         success: function(json) {
                                //location.reload(true);
                                var image= $("#profile_pic2").attr("src");
                                var name= $("#profile_name2").text();
                                var id = $("#profile_id2").text();

                                 $(".comment_input").html(null);

                                 $('.comments_section[data = '+postID+']').append(`<div class="w3-container w3-card-2 w3-white w3-round w3-margin" ><br>
              <img src="${image}" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="max-width:40px; max-height: 40px;">
            <span class="w3-right w3-opacity">  now</span>

            <a href="/profile/${id}" style="font-weight: bold;">${name}</a><br>
                    <h4>${text}</h4>
                     </div>`);

                             },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
            });


                });

           
              

        }


        $(document).ready(register_all_callbacks);


