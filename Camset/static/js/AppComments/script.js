 $(document).ready(function () {
      
      const cards = document.getElementsByClassName("card-text");
      const popup = document.querySelector(".popup-box")
      const popupCloseBtn = popup.querySelector(".popup-close-btn");
      const popupCloseIcon = popup.querySelector(".popup-close-icon");
      popupCloseBtn.addEventListener("click", popupBox);
      popupCloseIcon.addEventListener("click", popupBox);
      popup.addEventListener("click", function(event){
         if(event.target == popup){
          popupBox();
         }
      });            
  });



function detail( texte, id, post, url, cat  ) {


  if ($(window).width() > 500) {

    $.each( $('.popup-box .popup-content'), function () { 

        $(this).css({                   
          'width': '600px',
        });
    });
      
  }

  var html = '';
  html = html  + '<strong>  Id : </strong>  ' + id + '<br><br>' ;
  html = html  + '<strong> Commentaire : </strong> ' + texte + '<br> <br>';
  html = html  + '<strong> Post : </strong>  ' + post + '<br><br>' ;
  html = html  + '<strong> Lien vers le Post : </strong> ' + '<a href = ' + url + '> Vers Le Post</a>' + '<br>';

  $(".popup-body").html(html); 
  
  $(".popup-header").html('<h4 class="font-italic">' + cat   + '</h4>');
  popupBox();

};




function LirePlus( texte, cat  ) {

  $.each( $('.popup-box .popup-content'), function () { 

    $(this).css({
                         
      'width': '350px',
    });

  });

  var html = '';

  html = html   + texte + '<br> <br>';

  $(".popup-body").html(html); 
  
  $(".popup-header").html('<h4 class="font-italic">' + cat   + '</h4>');
  popupBox();

};


function popupBox(){
  const popup = document.querySelector(".popup-box"); 
  popup.classList.toggle("open");
};




function GoTo(path){
  
  // alert($('#quantity').val());
  
  var totalpage =  $('#pagination').data("page");
  const reg = new RegExp('^[0-9]+$');


  if (reg.test(idx)) {

      if (idx != "") {

        if (idx > totalpage) {
          alert("Choisir un entier dans l'interval précisé");
        }
        else
        {
          window.setTimeout(function () { window.location.href = '/'+ path + '?page='+ $('#quantity').val(); }, 0);
        }
      }
  }

  else 
  {
    alert("Entrer un entier dans l'interval précisé");
  }
  
  

};



//  Developed By Yasser Mas
// yasser.mas2@gmail.com




