 $(document).ready(function () {


    $body = $("body");

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


              
   });


 function deleteAllItems() {
    if (confirm("Etes vous sure de vouloir supprimer tous les commentaires?")) {
        
         $.ajax({
                    // data: {"file_name" : str },
                    url: 'DeleteAll',
                    // on success
                    success: function(response) {

                      alert(response.status);
 
                    },
                    // on error
                    error: function(response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });
    }
    return false;
}


 function deleteItems() {
    if (confirm("Are you sure?")) {
        
          var id = [];
          $(':checkbox:checked').each(function(i){

            id[i] = $(this).val();
          })
          if (id.length === 0) {

            alert("Aucun commentaires à supprimer");
          }

          else{

            // alert(id);

            $.ajax({
                    data: {"ids" : id },
                    url: 'delete',
                    // method : "POST",
                    // on success
                    success: function(response) {

                      for (var i = 0; i < id.length; i++) {
                        $('tr#'+id[i]+'').css('background-color' , '#ccc');
                        $('tr#'+id[i]+'').fadeOut('slow');


                      }


                      $(':checkbox:checked').each(function(i){

                        $(this).prop('checked', false);

                      })

                      id = [];
 
                    },
                    // on error
                    error: function(response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });
          }
    }
    return false;
};


 