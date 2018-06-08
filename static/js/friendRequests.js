$( document ).ready(function() {
    console.log("ready!");

    function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                  }
                  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();



    $('.accept-button, .reject-button').click(function(){


        var status = $(this).attr('status');


        //$("#accept-button").click(function () { });
      //$("#reject-button").click(function () { status=0});


       var email = $(this).attr('data');


                    console.log("email captured is: " +email);


                     console.log("status is: " +status);

                     //alert("email is "+email);
                     //alert("Status is "+status);

                    $.ajaxSetup({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        }
                    });
                     $.ajax({
                          type:"POST",
                          data: {'email': email, 'status': status},
                          url:"/friendRequests" ,
                          async:true,
                          dataType: "json",
                          success: function(json) {
                     location.reload(true); //true tells the browser to fetch the page from the server rather than the cache

                },

            });

                     });
});


