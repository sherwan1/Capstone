
  var images = new Array();

(function ($) {
    "use strict";

    //preload images

			function preload() {
				for (i = 0; i < arguments.length; i++) {
					images[i] = new Image();
					images[i].src = arguments[i];
					console.log("preloding!!");
				}
			}

            preload(
				"/static/images/img11.jpg",
                "/static/images/img03.jpg",
                "/static/images/img04.jpg",
                "/static/images/img05.jpg",
                "/static/images/img06.jpg",
                "/static/images/img07.jpg",
                "/static/images/img08.jpg",
                "/static/images/img02.jpg",
                "/static/images/img09.jpg",
                "/static/images/img10.jpg"
			);

      function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                  }
                  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }


    $("#signup_button").click(function() {
        $("#signup_form").show();
        $("#login_form").hide();
    });

     $("#back_button").click(function(e) {
         e.preventDefault();
        $("#signup_form").hide();
        $("#login_form").show();
    });

      $("#register_button").click(function(e) {
         e.preventDefault();

           var form = $('#signup_form')[0]; // You need to use standard javascript object here

           var formData = new FormData();

           formData.append("firstname",form.firstElementChild.elements.firstname.value);
           formData.append("lastname",form.firstElementChild.elements.lastname.value);
           formData.append("email",form.firstElementChild.elements.email.value);
           formData.append("password",form.firstElementChild.elements.password.value);
           formData.append("first_item",form.firstElementChild.elements.first_item.value);

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
                          url:"/basic_app/register/" ,
                            processData: false,
                            contentType: false,

                         success: function(json) {
                                console.log(json);

                                 $("#signup_form").hide();
                                 $("#login_form").hide();

                                 var string= json.data;
                                 $("#return_message").html(string);


                             },
                /*    error: function(xhr, status, err) {
                    // This time, we do not end up here!
                    alert("error happened and status is");
                    alert(status);

                }*/
            });

    });
     //alert($("#error_type").val());


    //background pic change algorithm

    //$('.container-login100').css("background-image", "url(static/images/img-01.jpg)");

    var i=0;
    var imghead=[
	    "url(static/images/img11.jpg)",
        "url(static/images/img03.jpg)",
        "url(static/images/img04.jpg)",
        "url(static/images/img05.jpg)",
        "url(static/images/img06.jpg)",
        "url(static/images/img07.jpg)",
        "url(static/images/img08.jpg)",
        "url(static/images/img02.jpg)",
        "url(static/images/img09.jpg)",
        "url(static/images/img10.jpg)"
	];//add as many images as you like

function slideimg() {
    setTimeout(function () {
        console.log("change background img");
         $('.container-login100').css('background-image', imghead[i]);
        i++;
        if(i==imghead.length) i=0;
        slideimg();
    }, 3000);
}
slideimg();




})(jQuery);

