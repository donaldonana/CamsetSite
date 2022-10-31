 $(document).ready(function () {


    $body = $("body");

     $.space = {};
     $.space.comments = [];
     $.space.nombre = 0 ;
     $.space.myVar2 = "somethingElse";

    $(document).on({
         ajaxStart: function() { $body.addClass("loading");    },
         ajaxStop: function() { $body.removeClass("loading"); 
         // $(".alert-success").addClass("show");

         // setTimeout(function() {
         // $(".alert-success").removeClass("show");
            
         //  }, 4000);
       }    
    });






      $("#myBtn").click(function(){

        var str = "";
         


         $(':radio:checked').each(function(i){

            str =  $(this).val();

            // alert(str);
            
          });


         if (str == '') {

           alert("Choisir un fichier")
         }

         else {

           $.ajax({
                    data: {"file_name" : str },
                    url: 'upload',
                    // on success
                    success: function(response) {

                      // alert(response.status);

                      if (response.status) {

                        alert(response.message);
                      }

                      else {

                        alert(response.message);

                      }
                        

                    },
                    // on error
                    error: function(response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });
        
           
           
           }
           


        });


      $("input[id^='select-']").each(function (i, el) {
        $(this).change(function() {
            id = $(this).data("id");
            var item = { "id" : id};
            if ( $(this).is(':checked') ) {
              $.space.comments.push(item);
              $.space.nombre = $.space.nombre + 1;
            } 
            else { 

              $.space.comments = $.space.comments.filter( obj => obj.id !== id);
              $.space.nombre = $.space.nombre - 1;


            }
       });

      });

       


              
   });


//  function deleteAllItems() {
//     if (confirm("Etes vous sure de vouloir supprimer tous les commentaires?")) {
        
//          $.ajax({
//                     // data: {"file_name" : str },
//                     url: 'auth/DeleteChecked',
//                     // on success
//                     success: function(response) {

 
//                     },
//                     // on error
//                     error: function(response) {
//                         // alert the error if any error occured
//                         console.log(response.responseJSON.errors)
//                     }
//                 });
//     }
//     return false;
// }


function deleteSelectItem( ) {

  if (confirm(`Etes vous sure de vouloir supprimer  ${$.space.nombre} commentaire(s) ? `)) {


   $.ajax({

            data : {"items" : $.space.comments },
            url: 'auth/DeleteChecked',
                    // on success
             success: function(response) { 

                 for (var i = 0; i < $.space.comments.length; i++) {
                    var id = $.space.comments[i].id;
                    $('li#'+id+'').css('background-color' , '#ccc');
                    $('li#'+id+'').fadeOut('slow');
                  }

                  $.space.comments = [];
                  $.space.nombre = 0;

               },
         // on error
         error: function(response) {
               // alert the error if any error occured
            console.log(response.responseJSON.errors)
           }
         });

        return false;

  }
  
}


 function deleteItem(id) {
    if (confirm("Etes vous sure de vouloir supprimer ce commentaire ? ")) {

      $('li#'+id+'').css('background-color' , '#ccc');
      $('li#'+id+'').fadeOut('slow');
        
            // alert(id);

            $.ajax({
                    data: {"id" : id },
                    url: 'delete',
                    // method : "POST",
                    // on success
                    success: function(response) {
 
                      $('li#'+id+'').css('background-color' , '#ccc');
                      $('li#'+id+'').fadeOut('slow');
  
                      // $(':checkbox:checked').each(function(i){
                      //   $(this).prop('checked', false);
                      // })
 
                    },
                    // on error
                    error: function(response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });
    }
    return false;
};



 


 