$( document ).ready(function() {
    console.log( "ready!" );
});


function returnObj(a) {
     b = [];
     for (i=0;i<a.length;i++){
       if ($(a[i]).isVisible()){
         c = [];
         c[0] = a[i];
         if (a[i].tabIndex == '0'){
            b.push(a[i]);
         }
        //  b.push(a[i]);
       }
 }
    return b;
};

$.fn.isVisible = function() {
    var rect = this[0].getBoundingClientRect();
    return (
        (rect.height > 0 || rect.width > 0) &&
        rect.bottom >= 0 &&
        rect.right >= 0 &&
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.left <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

var reactions = [];
var spanlist = [];
var btns = [];
var z = [];

function onPageLoaded(){
  console.log("injecting custom css class");
  $("<style type='text/css'> .selected { border-color:#3b5998 !important; border-width:thick !important} </style>").appendTo("head");
// $("<div/>").addClass("selected").text("SOME NEW TEXT").appendTo("body");
}

function showSelected(){
  visible_count = 0;
  y = returnObj($('._4-u2.mbm._4mrt._5v3q._4-u8'));

  

  // $(y).removeClass("selected");

  $(y[1]).addClass("selected");

  try {
    $(y[0]).removeClass("selected");
    $(y[2]).removeClass("selected");
  } catch(err) {
    console.log("Error when catching post index");
  }

  return visible_count;
}

function clickReaction(reaction){
  let likeBtn = $("div._5jmm._5pat[tabindex='0']:visible")
    .find('a._6a-y._3l2t._18vj[role="button"]')
  // let likeBtn = $("div._5jmm._5pat._3lb4[tabindex='0']:visible")
  //   .find('.UFILikeLink._4x9-._4x9_:visible')
  let reactKey = Object.keys(likeBtn['0'])[0]
  likeBtn[0][reactKey].pendingProps.onMouseEnter()
  setTimeout(() => {
    let reactionsMenu = $('._iu-._628b._1ef3:visible')
    let reactions = $(reactionsMenu[reactionsMenu.length-1]).children()
    let ri
    // finally clicks
    if (reaction == "curtir"){
      ri = 0;
    } else if (reaction == "amei"){
      ri = 1;
    } else if (reaction == "haha"){
      ri = 2;
    } else if (reaction == "uau"){
      ri = 3;
    } else if (reaction == "triste"){
      ri = 4;
    } else if (reaction == "grr"){
      ri = 5;
    } else {
      console.log("Invalid reaction");
    }

    console.log("Clicking on the reaction "+reaction );
    console.log(reactions, ri)
    reactions[ri].click()

    setTimeout(() => {
      likeBtn[0][reactKey].pendingProps.onMouseLeave()
    }, 200)

  }, 800)
}
