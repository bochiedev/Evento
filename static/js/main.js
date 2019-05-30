
$(document).ready(function() {
//
//   $("#id_username").on("keyup", function () {
//       var username = $(this).val();
//       var form = $("#register_form");
//
//
//       $.ajax({
//         url: form.attr("data-validate-username-url"),
//         data: {
//           'username': username
//         },
//         dataType: 'json',
//         success: function (data) {
//           if (data.username_is_taken) {
//             $(".form-text").html("A user with this username already exists.")
//           }else{
//             $(".form-text").html("Good to go")
//
//           }
//         }
//       });
//
//     });
//
//     $("#id_email").on("keyup", function () {
//         var email = $(this).val();
//         var form = $("#register_form");
//
//         $.ajax({
//           url: form.attr("data-validate-email-url"),
//           data: {
//             'email': email
//           },
//           dataType: 'json',
//           success: function (data) {
//             if (data.email_is_taken) {
//               $(".form-text").html("A user with this email already exists.")
//             }else{
//               $(".form-text").html("Good to go")
//
//             }
//           }
//         });
//
//       });


  $('#id_password').change( function() {

    var password = $(this).val();
    var form = $("#register_form");

      $.ajax({
          url : form.attr("data-validate-password-url"),
          data: {
            'password': password
          },
          dataType: 'json',
          success: function(data) {
            if (data.password_response) {
              $(".password-form-text").removeClass("text-muted text-danger").addClass("text-success");
              $(".password-form-text").html(data.message);

            }else{
              $(".password-form-text").removeClass("text-muted").addClass("text-danger");
              $(".password-form-text").html(data.message);

            }
          }
        });

  });

  $('#register_form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");
    csrf_token = $(this).find('input[name=csrfmiddlewaretoken]').val();

    i = 0;
    setInterval(function() {
        i = ++i % 4;
        $("#register").html("loading"+Array(i+1).join("."));
    }, 500);


    $.ajax({
        url : $(this).attr("action"),
        type : "POST",
        data : {
                  username : $('#id_username').val(),
                  email : $('#id_email').val(),
                  password : $('#id_password').val(),
                  csrfmiddlewaretoken: csrf_token,

                },
        success : function(json) {

          if(json.success){

            $("#results").addClass("alert alert-success");
            $("#results").html("Account created succesfully");
            location.href = "/auth/login/";

          }else{
            if(json.message.username) {
              $(".username-form-text").removeClass("text-muted ").addClass("text-danger");
              $(".username-form-text").html(json.message.username);

            }else if(json.message.email){
              $(".email-form-text").removeClass("text-muted ").addClass("text-danger");
              $(".email-form-text").html(json.message.email);

            }else if(json.message.password){
              $(".password-form-text").removeClass("text-muted ").addClass("text-danger");
              $(".password-form-text").html(json.message.password);

            }

          }


        },

        error : function(xhr,errmsg,err) {

          $("#results").html("Oops! We have encountered an error");

        }
    });
  });



});
