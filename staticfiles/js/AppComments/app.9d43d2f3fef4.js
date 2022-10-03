$(document).ready(function () {

  // alert( "$(this).text()" );

  var showChar = 120;
  var ellipsestext = "...";
  var moretext = "Lire Plus";


  $.each( $('p[id^=text-]'), function () {

    var content = $(this).html();

    if(content.length > showChar) {

      var c = content.substr(0, showChar);
      var html =   c  + ellipsestext + '<button type="button" class="btn   btn-link btrm " style="color: blue;">' 
      +moretext+'</button>  ' ;

      $(this).html(html); 
    }

  });


  $.mynamespace = {};
  $.mynamespace.myVar = [];
  $.mynamespace.myVar2 = "somethingElse";


              
});


             

  function FuriousCall(id)   { 

      $("#btnsave").attr('disabled', false);
      $("#btncancel").attr('disabled', false);


        var item = { "id" : id, "reponse" : "furieux"};
        $.mynamespace.myVar.push(item);
        $(`#reponse-${id}`).text('votre reponse : furieux');
        $(`#furImg-${id}`).addClass('img');
        $(`#badImg-${id}`).removeClass('img');
        $(`#norImg-${id}`).removeClass('img');
  };


  function BadCall(id) {

    var item = { "id" : id, "reponse" : "offensif"};
    $.mynamespace.myVar.push(item);              
    $(`#reponse-${id}`).text('votre reponse : offensif');
    $(`#furImg-${id}`).removeClass('img');
    $(`#badImg-${id}`).addClass('img');
    $(`#norImg-${id}`).removeClass('img');

    $("#btnsave").attr('disabled', false);
    $("#btncancel").attr('disabled', false);
 
  };


  function NormalCall(id){ 

    var item = { "id" : id, "reponse" : "normal"};
    $.mynamespace.myVar.push(item);             
    $(`#reponse-${id}`).text('votre reponse : normal');
    $(`#furImg-${id}`).removeClass('img');
    $(`#badImg-${id}`).removeClass('img');
    $(`#norImg-${id}`).addClass('img');

    $("#btnsave").attr('disabled', false);
    $("#btncancel").attr('disabled', false);

  };

              

              function save(){ 

                $.ajax({

                    data : {"items" : $.mynamespace.myVar },
                    url: 'save',
                    // on success
                    success: function(response) { 
                        // alert("succes");  
                         window.setTimeout(function () {
                            window.location.href = '/';
                        }, 0);

                    },
                    // on error
                    error: function(response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });

                return false;
              };

  function cancel(){

    $.each( $('.img'), function () {

     $(this).removeClass('img');

  });

    $("#btnsave").attr('disabled', true);
    $("#btncancel").attr('disabled', true);
  }


              function logout()
              {


                   window.setTimeout(function () {
                            window.location.href = 'auth/logout_user';
                        }, 0);


              };

              function listResult()
              {


                   window.setTimeout(function () {
                            window.location.href = '/list_result';
                        }, 0);

              };

               function main()
              {


                   window.setTimeout(function () {
                            window.location.href = '/';
                        }, 0);

              };

              function admin()
              {


                   window.setTimeout(function () {
                            window.location.href = '/admin';
                        }, 0);

              };

 



     