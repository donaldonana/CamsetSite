$(document).ready(function () {

  // $.each( $('p[id^=text-]') 

  $.mynamespace = {};
  $.mynamespace.page = 1 ;
   $.mynamespace.myVar = []




  $('#StatsPagination a').click(function(event){
    // preventing default actions
    event.preventDefault();
    var page_no = $(this).attr('href');
    numItems = $(".StatsLi").length;
    lastNum = $('.lasted:last').text() ;


    if (page_no != $.mynamespace.page) {

        // ajax call
      $.ajax({
          // define url name
          url: "StatsPagination", 
          data : {    
          page_no : page_no, 
          current_page : $.mynamespace.page,
          numItems : numItems,
          lastNum : lastNum,
        },
        // handle a successful response
        success: function (response) {

          // alert(response.status)
          $('#StatsItem').html('');
          var index = response.index;  
          // $('#test div.a:last')
           
          // alert($('.lasted').last().text());

          $.each(response.results, function(i, val) {

             const html = '<li class="list-group-item StatsLi"  style=" border-bottom: 1px solid rgba(0, 0, 0, 0.1); margin-bottom: 1px; background-color: rgb(255, 254, 254); " >'
                  + '<div class=" align-items-lg-center">'
                        +'<div class=" order-2 order-lg-1 text-center">'

                             +'<i class="fa fa-user fa-3x" aria-hidden="true"></i><br><br>'   

                             +'<p class="font-italic mb-0 " style="font-size: 15px;  ">'
                             
                                +'Utilisateur : <span class="font-weight-bold"> '+ val.username +  '</span>' + 

                            '</p><br>'
                            +'<p class="font-italic mb-0  " style="font-size: 15px;">' 
                             
                              +'Email : <span class="font-weight-bold">'+val.email+ '</span>' +


                            '</p><br>'     

                            +'<p class="font-italic mb-0  " style="font-size: 15px;">'
                             
                              +'Votes : <span class="font-weight-bold">' + val.vote + ' votes  </span>' +


                            '</p><br>' 

                            +'<p class="font-italic mb-0 font-weight-bold" style="font-size: 16px;  ">' 
                             
                               +'Rang :  ' + '<span class="lasted">' + val.index  + '</span>'+


                            '</p><br>'


                           
                             
                             
                       +' </div>'
                      +' </div>'  
                +'</li>' ;





                    $('#StatsItem').append(html);

                    // index = index + 1;

             // alert(val.email);




           
        });

          $.mynamespace.page = page_no;
          $(window).scrollTop(0);
      },
        error: function () {

          alert(response.responseJSON.errors)

        }
      }); 


    }

    else {

      return false;
    }

    
  });    

 

   


              
});


             

  function FuriousCall(id)   { 


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
      $.mynamespace.len = 0 ;

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
