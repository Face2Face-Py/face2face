function returnObj(a) {
     b = [];
     for (i=0;i<a.length;i++){
       if ($(a[i]).isVisible()){
         c = [];
         c[0] = a[i];
         b.push(c);
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

function countVisible(){
  z = returnObj($('a.UFILikeLink._4x9-._4x9_:visible'));
  visible_count = 0;
  for (i=0;i<z.length;i++){
    visible_count ++;
  }
  return visible_count;
}

function clickReaction(btnindex,reaction){
  z = returnObj($('a.UFILikeLink._4x9-._4x9_:visible'));
  btns = [];
  for (i=0;i<z.length;i++){
    reactkey = Object.keys(z[i][0])[1];
    z[i][0][reactkey].onMouseEnter();
  }

  btns = [];
  reactions = [];

  setTimeout(function(){

    spanlist = $("._iuw:visible");
    for (i=0;i<spanlist.length;i++){
      if ($(spanlist[i]).isVisible()){
        btns.push(spanlist[i]);
      }
    }

    for (i=0;i<z.length;i++){
      z[i][0][reactkey].onMouseLeave();
    }

    if (btns.length == 7){
      reactions.push(btns);
    } else if (btns.length == 14){
      reactions.push(btns.slice(0,7));
      reactions.push(btns.slice(7,14));
    } else {
      reactions.push(btns.slice(0,7));
      reactions.push(btns.slice(7,14));
      reactions.push(btns.slice(14,21));
    }

    // finally clicks
    if (reaction == "curtir"){
      ri = 0;
    } else if (reaction == "amei"){
      ri = 1;
    } else if (reaction == "gratidao"){
      ri = 2;
    } else if (reaction == "haha"){
      ri = 3;
    } else if (reaction == "uau"){
      ri = 4;
    } else if (reaction == "triste"){
      ri = 5;
    } else if (reaction == "grr"){
      ri = 6;
    } else {
      console.log("Invalid reaction");
    }
    console.log("Clicking on button "+btnindex+" on the reaction "+reaction );
    reactions[btnindex][ri].click();

  },600);
};
