$(document).ready(function(){
        //var NO_PIC="data:image/jpeg;base64,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";
        var link_url = "localhost:3000/profile_save";
        var interests=$("#interests").val();
        var courses=$("#courses").val();

   function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#profile_pic')
                        .attr('src', e.target.result);
                };

                reader.readAsDataURL(input.files[0]);
            }
        }

    $("#int_add").click( function(){
        
        //$("#mid_col").fadeTo( "slow", .1 );
        //$("#mid_col :input").attr("disabled", true);
        $(".mid_col").css('background-color', 'black');
        $("#in_box").removeClass("hidden");

        $("#in_box").parent().css({position: 'relative'});
        $("#in_box").css({top: 0, left: 50, position:'absolute'});
    }
    );

    $("#cancel_in").click(function(){

        $("#in_box").addClass("hidden");
         $("#interests_in").val("");
    });


   $("#courses_add").click(function(){
        var course = $("#courses_in").val();
        courses=$("#courses").val();
        let id;
        if(courses.length>0){
            courses+=","+course;
            id=courses.split(",").length-1;



            $("#course_list").append('<label style="padding-left:1%" id=\courset'+id+'\">'+course+'</label><button type="button" data-toggle="tooltip" title="Remove course" class="course_rem" id=\"course_rem'+id+'\"> X</button>' );

           alert(id);
        }
        else{
            courses=course;
            id=courses.split(",").length-1;
           $("#course_list").append('<label style="padding-left:1%" id=\"course'+id+'\">'+course+'</label><button type="button" data-toggle="tooltip" title="Remove course" class="course_rem" id=\"course_rem'+id+'\"> X</button>' );

        }
        $("#courses_in").val("");
        $("#courses").val(courses);

         $("#course_rem"+id).click(function(){
            var id = $(this).attr('id');
            id = id.slice(12,id.length);
            id=parseInt(id);

            var courses=$("#courses").val().split(",");
            courses.splice(id,1);
            courses_str = courses.toString();

            $("#courses").val(courses_str);

            $("#course"+id).addClass("hidden");
            $("#course_rem"+id).addClass("hidden");
         });

        });


        $(".course_rem").click(function(){

            var id = $(this).attr('id');
            id = id.slice(12,id.length);
            id=parseInt(id);

            var courses=$("#courses").val().split(",");
            courses.splice(id,1);
            courses_str = courses.toString();
            alert(courses_str);
            $("#courses").val(courses_str);

            $("#course"+id).addClass("hidden");
            $("#course_rem"+id).addClass("hidden");



        });




        $("#interests_add").click(function(){
        var interest = $("#interests_in").val();
        interests=$("#interests").val();
        let id;
        if(interests.length>0){
            interests+=","+interest;
            id=interests.split(",").length-1;



            $("#interest_list").append('<label style="padding-left:1%" id=\"interest'+id+'\">'+interest+'</label><button type="button" data-toggle="tooltip" title="Remove interest" class="interest_rem xbtn" id=\"interest_rem'+id+'\"> X</button>' );

          
        }
        else{
            interests=interest;
            id=interests.split(",").length-1;
           $("#interest_list").append('<label style="padding-left:1%" id=\"interest'+id+'\">'+interest+'</label><button type="button" data-toggle="tooltip" title="Remove interest" class="interest_rem xbtn" id=\"interest_rem'+id+'\"> X</button>' );

        }
        $("#interests_in").val("");
        $("#interests").val(interests);

         $("#interest_rem"+id).click(function(){
            var id = $(this).attr('id');
            id = id.slice(12,id.length);
            id=parseInt(id);

            var interests=$("#interests").val().split(",");
            interests.splice(id,1);
            interests_str = interests.toString();

            $("#interests").val(interests_str);

            $("#interest"+id).addClass("hidden");
            $("#interest_rem"+id).addClass("hidden");
         });

         $("#in_box").addClass("hidden");

        });

        $(".interest_rem").click(function(){

            var id = $(this).attr('id');
            id = id.slice(12,id.length);
            id=parseInt(id);

            var interests=$("#interests").val().split(",");
            interests.splice(id,1);
            interests_str = interests.toString();
            alert(interests_str);
            $("#interests").val(interests_str);

            $("#interest"+id).addClass("hidden");
            $("#interest_rem"+id).addClass("hidden");



        });




        $("#test").click(function(){
        //alert($("#interests").val());
        a=[10,20,30,40];
        a.splice(2,1);
        alert(a);
        });
    });