$(document).ready(function () {


  

  // $.each( $('p[id^=text-]') 

 

  $.mynamespace = {};
  $.mynamespace.myVar = [];
  $.mynamespace.len = 0 ;
  $.mynamespace.myVar2 = "somethingElse";


              
});


             

  function FuriousCall(id)   { 

     


    if ($.mynamespace.len >= 15) {

      alert("Vous avez atteint la limite en Enregistrer ou Annuler vos votes pour pouvoir continuer");

      return false
    }

      $("#btnsave").attr('disabled', false);
      $("#btncancel").attr('disabled', false);


        var item = { "id" : id, "reponse" : "furieux"};
        $.mynamespace.myVar.push(item);
        $.mynamespace.len = $.mynamespace.len + 1;
        $(`#reponse-${id}`).text('votre réponse : furieux');
        $(`#furImg-${id}`).addClass('img');
        $(`#badImg-${id}`).removeClass('img');
        $(`#norImg-${id}`).removeClass('img');
  };


  function BadCall(id) {

    if ($.mynamespace.len >= 15) {

      alert("Vous avez atteint la limite en Enregistrer ou Annuler vos votes pour pouvoir continuer");

      return false
    }

    var item = { "id" : id, "reponse" : "offensif"};
    $.mynamespace.myVar.push(item);      
    $.mynamespace.len = $.mynamespace.len + 1;
    $(`#reponse-${id}`).text('votre réponse : offensif');
    $(`#furImg-${id}`).removeClass('img');
    $(`#badImg-${id}`).addClass('img');
    $(`#norImg-${id}`).removeClass('img');

    $("#btnsave").attr('disabled', false);
    $("#btncancel").attr('disabled', false);
 
  };


  function NormalCall(id){ 

    if ($.mynamespace.len >= 15) {

      alert("Vous avez atteint la limite en Enregistrer ou Annuler vos votes pour pouvoir continuer");

      return false
    }

    var item = { "id" : id, "reponse" : "normal"};
    $.mynamespace.myVar.push(item); 
    $.mynamespace.len = $.mynamespace.len + 1;
    $(`#reponse-${id}`).text('votre réponse : normal');
    $(`#furImg-${id}`).removeClass('img');
    $(`#badImg-${id}`).removeClass('img');
    $(`#norImg-${id}`).addClass('img');

    $("#btnsave").attr('disabled', false);
    $("#btncancel").attr('disabled', false);

  };

              

  function save(next_page){ 

       $.ajax({

            data : {"items" : $.mynamespace.myVar },
            url: 'save',
                    // on success
             success: function(response) { 
                 // alert("succes");  
              window.setTimeout(function () {window.location.href = '/' }, 0);

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


      $.each( $('[id^=reponse-]'), function () {  

       $(this).text('votre réponse :');

      });

      $("#btnsave").attr('disabled', true);
      $("#btncancel").attr('disabled', true);

      $.mynamespace.myVar = [];
  }


function filters(){

    var texte = $('#filter').val()

    if (texte != "") {

      $.ajax({

                    data : {"filter" : texte },
                    url: 'admin',
                    // on success
                    success: function(response) { 
                        // alert("succes");  
                        //  window.setTimeout(function () {
                        //     window.location.href = '';
                        // }, 0);

                    },
                    // on error
                    error: function(response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });


    }

    else {

      $('#filter').css({
                             
          'border-color': 'red',
        });
    }
    
 

}

function logout(){

    window.setTimeout(function () { window.location.href = 'auth/logout_user'; }, 0);

};

function stats(){ 

  window.setTimeout(function () { window.location.href = '/stats'; }, 0);

};

function main(){

  window.setTimeout(function () { window.location.href = '/'; }, 0);

};

function admin(){
  
  window.setTimeout(function () { window.location.href = '/admin'; }, 0);

};

function help(){
  
  window.setTimeout(function () { window.location.href = '/help'; }, 0);

};
