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
  // z = returnObj($('a.UFILikeLink._4x9-._4x9_:visible'));
  btns = [];

  y = $("div._5jmm._5pat._3lb4.o_dxf8lagm[tabIndex='0']:visible").children()[1]

  // y = returnObj($('._4-u2.mbm._4mrt._5v3q._4-u8'));

  // $(y).removeClass("selected");

  // $(y[1]).addClass("selected");

  // try{
  //   $(y[0]).removeClass("selected");
  //   $(y[2]).removeClass("selected");
  // } catch(err){
  //   console.log("Error when catching post index");
  // }

  btn =  $(y).find(".UFILikeLink._4x9-._4x9_");
  btnreactkey = Object.keys(btn[0])[1];
  // console.log(btn);
  // console.log(btnreactkey);
  
  btn[0][btnreactkey].onMouseEnter();

  // for (i=0;i<z.length;i++){
  //   reactkey = Object.keys(z[i][0])[1];
  //   z[i][0][reactkey].onMouseEnter();
  // }

  // console.log(z);

  btns = [];
  reactions = [];

  setTimeout(function(){

    // spanlist = returnObj($("._iuw:visible"));
    spanlist = $("._iuw:visible")
    spanlist = spanlist.slice(spanlist.length-6,spanlist.length)
    // console.log(spanlist);
    // for (i=0;i<spanlist.length;i++){

    //   if ($(spanlist[i]).first().isVisible()){
    //     // console.log("O seguinte botão é visivel");
    //     // console.log($(spanlist[i]).first());
    //     btns.push(spanlist[i]);
    //   }
    // }

    // // console.log("botoes validos:")
    // // console.log(btns);

    // if (btns.length == 7){
    //   reactions.push(btns);
    // } else if (btns.length == 14){
    //   reactions.push(btns.slice(0,7));
    //   reactions.push(btns.slice(7,14));
    // } else {
    //   reactions.push(btns.slice(0,7));
    //   reactions.push(btns.slice(7,14));
    //   reactions.push(btns.slice(14,21));
    // }

    // if (z.length == 1){
    //   reactions.splice(0,1)
    // } else if (z.length == 2){
    //
    // } else {
    //
    // }
    // console.log("botões encontrados:");
    // console.log(reactions);

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

    // if ( btn[0].getAttribute("aria-pressed") == 'false'){
    spanlist[ri].click();
    // }
    
    setTimeout(function(){
      // for (i=0;i<z.length;i++){
      // z[i][0][reactkey].onMouseLeave();
      // }
    btn[0][btnreactkey].onMouseLeave();
    },100);


  },600);

};
