var video_url =0;

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
                   // console.log("video url of the post is "+ json.data.video_url[0])

                    for(var i=0; i<json.data.post_text.length; i++) {

                        //check if video url is appended in the new post

                        if (json.data.video_url[i] != "0"){
                             var str =   `<iframe width="100%" height="400" src="${json.data.video_url[i]}"
                                       allowfullscreen="allowfullscreen"
                                        mozallowfullscreen="mozallowfullscreen"
                                        msallowfullscreen="msallowfullscreen"
                                        oallowfullscreen="oallowfullscreen"
                                        webkitallowfullscreen="webkitallowfullscreen">
                                        </iframe>`;

                        }
                        else{
                            var str = '';
                        }


                        //check if images are embedded to the post

                        var num_of_images= json.data.pictures_urls[i].length;

                        var images = ``;

                        if(num_of_images>0){
                            var p=0;
                            for(p=0; p< num_of_images; p++) {
                                images = `
                                    <div class="w3-row-padding" style="margin:0 -16px">
                                     <div class="w3-half">
                                <img src="${json.data.pictures_urls[i][p]}" style="width:100%" alt="Northern Lights" class="w3-margin-bottom">
                                    </div>
                                </div>
                                ` + images;
                            }
                        }

                        $("#Top").prepend(
                            ` <div class="Post-Comment-box">
                  <div data="${json.data.post_ID[i]}" class="sample post-bar w3-container w3-card-2 w3-white w3-round w3-margin"><br>
                <img src="${json.data.post_owner_pic[i]}" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="max-width:50px; max-height: 50px;">
                <span class="w3-right w3-opacity">now</span>
                <h4 class="name">${json.data.post_owner[i]}</h4><br>
                <hr class="w3-clear">
                <p class="text">${json.data.post_text[i]}</p>
                
                <br>`
                + str + images +
               
               
                 `<button type="button" data="${json.data.post_ID[i]}" class="heart-button btn btn-danger btn-circle" style="
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
                          data: {'last_postID': postID},
                          url:"/check_new_post" , //"https://app.ticketmaster.com/discovery/v2/events/G5diZfkn0B-bh.json?apikey=27mLqO6JmMfWlES8MKnMVG1tkm75I9cE",
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
                              setTimeout('check_new_post()',5000);  //This timer sets the time for the interval between checking for new posts.

                             },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
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
                          url:"/likedBy" ,
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
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
            });


                    //$(this).slideDown();
                 });
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
                          url:"/like_post" ,
                          async:true,
                          dataType: "json",

                         success: function(json) {
                                //location.reload(true);
                                //increment the like number in the Like button]
                              //  alert("Got 200 response")
                                console.log("Got a positive response from server");
                                //location.reload(true);
                                console.log("post id is  " + postID);

                                //update likes count and change like button to liked

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
                                //alert("count right now is "+count);

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


                $(".post_submit").click(function () {

                    //check if no file is entered here
                    var form = $('#image_form')[0]; // You need to use standard javascript object here

                    console.log("Number of files being sent " +form[1].files.length);

                    var formData = new FormData();
                    //console.log(formData);



                    if(form[1].files.length != 0){

                          console.log("Adding all the files to the form data ");

                        for(var i=0; i< form[1].files.length; i++){

                            formData.append(form[1].files[i].name,form[1].files[i],form[1].files[i].name);

                        }
                    }



                    var text = $('.post_input').text();
                    console.log("text captured is: " +text);


                    //append the post text to the form. This form also contains any uploaded files
                     formData.append("text", text);

                     //append the video url to the post
                     formData.append("video_url", video_url);

                     console.log("reaching ajax last point");
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
                          data: formData,
                          url:"/post_submit" , //"https://app.ticketmaster.com/discovery/v2/events/G5diZfkn0B-bh.json?apikey=27mLqO6JmMfWlES8MKnMVG1tkm75I9cE",
                            processData: false,
                            contentType: false,

                            success: function(json) {
                                location.reload(true);    //dont reload page instead wait for check_new_post function to load the new post

                            },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
                        });


                });



                //Comment submit js code:

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
                          url:"/comment_submit" ,
                          async:true,
                          dataType: "json",

                         success: function(json) {
                                //location.reload(true);

                             var image= $("#profile_pic1").attr("src");
                             var name= $("#profile_name1").text();
                             var id=$("#profile_id1").text();
                             //alert(name);


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





             //////////////// This code is for multiple file uploads



            var input = document.querySelector('#image_uploads');
            var preview = document.querySelector('.preview');

            input.style.opacity = 0;

            input.addEventListener('change', updateImageDisplay);

            function updateImageDisplay() {
              while(preview.firstChild) {
                preview.removeChild(preview.firstChild);
              }

              var curFiles = input.files;
              if(curFiles.length === 0) {
                var para = document.createElement('p');
                para.textContent = 'No files currently selected for upload';
                preview.appendChild(para);
              } else {
                var list = document.createElement('ol');
                preview.appendChild(list);
                for(var i = 0; i < curFiles.length; i++) {
                  var listItem = document.createElement('li');
                  var para = document.createElement('p');
                  if(validFileType(curFiles[i])) {
                    para.textContent = 'File name ' + curFiles[i].name + ', file size ' + returnFileSize(curFiles[i].size) + '.';
                    var image = document.createElement('img');
                    image.src = window.URL.createObjectURL(curFiles[i]);
                    image.style.width= '90px';
                    image.style.height= '90px';


                    listItem.appendChild(image);
                    listItem.appendChild(para);

                  } else {
                    para.textContent = 'File name ' + curFiles[i].name + ': Not a valid file type. Update your selection.';
                    listItem.appendChild(para);
                  }

                  list.appendChild(listItem);
                }
              }
            }

            var fileTypes = [
              'image/jpeg',
              'image/pjpeg',
              'image/png'
            ]

            function validFileType(file) {
              for(var i = 0; i < fileTypes.length; i++) {
                if(file.type === fileTypes[i]) {
                  return true;
                }
              }

              return false;
            }
            function returnFileSize(number) {
              if(number < 1024) {
                return number + 'bytes';
              } else if(number > 1024 && number < 1048576) {
                return (number/1024).toFixed(1) + 'KB';
              } else if(number > 1048576) {
                return (number/1048576).toFixed(1) + 'MB';
              }
            }



            ///////////////// End of multiple file uploads



            //code to handle youtube embedded videos
              $(".yt-button").click(function () {  //when comment is submitted i.e when the button is pressed
                        var popup = document.getElementById("myPopup");
                        popup.classList.add("show");
                        popup.classList.remove("hidden");
              });

              $(".video_ok").click(function () {  //when comment is submitted i.e when the button is pressed
                        var popup = document.getElementById("myPopup");
                        popup.classList.add("hidden");
                        video_url = $('#video_url').val();  //now get the text inputted in the comment box
              });

               $(".video_remove").click(function () {  //when comment is submitted i.e when the button is pressed
                        var popup = document.getElementById("myPopup");
                        popup.classList.add("hidden");
                        $('#video_url').val(null);
                        video_url=0;
              });

        }


        $(document).ready(register_all_callbacks);


