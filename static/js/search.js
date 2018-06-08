$( document ).ready(function() {
    console.log( "ready!" );

        function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                  }
                  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

                $(".friend-request").click(function () {
                     var email=$(this).attr('email');
                    console.log("email captured is: " +email);
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
                          data: {'email': email},
                          url:"/sendFriendRequest" , //"https://app.ticketmaster.com/discovery/v2/events/G5diZfkn0B-bh.json?apikey=27mLqO6JmMfWlES8MKnMVG1tkm75I9cE",
                          async:true,
                          dataType: "json",
                          success: function(json) {
                     location.reload(true); //true tells the browser to fetch the page from the server rather than the cache

                },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
            });


                });



});