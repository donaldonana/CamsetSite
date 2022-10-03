 $(document).ready(function () {
      
      const cards = document.getElementsByClassName("card-text");
      const popup = document.querySelector(".popup-box")
      const popupCloseBtn = popup.querySelector(".popup-close-btn");
      const popupCloseIcon = popup.querySelector(".popup-close-icon");


       for (var i = 0; i < cards.length; i++) {
         cards[i].addEventListener("click",function(event){

          if(event.target.tagName.toLowerCase() == "button"){
            // alert(event.target.parentElement.parentElement.innerHTML)

            $.each( $('.popup-box .popup-content'), function () { 


               $(this).css({       
                  'width': '350px',
                });

             });
             var item = event.target.parentElement.parentElement ;
             const readMoreCont = item.querySelector(".read-more-cont").innerHTML;
             popup.querySelector(".popup-body").innerHTML = readMoreCont;
             item = item.parentElement;
             const h3 = item.querySelector("h3").innerHTML;
             popup.querySelector("h4").innerHTML = h3;
             popupBox();


          }

       });
      }

      popupCloseBtn.addEventListener("click", popupBox);
      popupCloseIcon.addEventListener("click", popupBox);

      popup.addEventListener("click", function(event){
         if(event.target == popup){
          popupBox();
         }
      });



              
  });





function LirePlus( texte, id, post, url, cat  ) {

  $.each( $('.popup-box .popup-content'), function () { 

    $(this).css({
                         
      'width': '600px',
    });

  });

  var html = '';
  html = html  + '<strong>  Commentaire Id : </strong>  ' + id + '<br><br>' ;

  html = html  + '<strong>  Post : </strong>  ' + post + '<br><br>' ;
  html = html  + '<strong> Commentaire : </strong> ' + texte + '<br> <br>';
  html = html  + '<strong> Lien vers le Post : </strong> ' + '<a href = ' + url + '> Vers Le Post</a>' + '<br>';

  $(".popup-body").html(html); 
  
  $(".popup-header").html('<h4 class="font-italic">' + cat   + '</h4>');
  popupBox();

};






function popupBox(){


  const popup = document.querySelector(".popup-box");
  
 
  popup.classList.toggle("open");

  };