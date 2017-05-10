function returnObj(a) {
     b = {};
     for (i=0;i<a.length;i++){
         c = [];
         c[0] = a[i]
         c[1] = $(a[i]).isVisible()
         b[i] = c;
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

var lastbt = null;
var btnid = 1;
var reactions = {};

function doStuff(){
  z = returnObj($('.UFILikeLink._4x9-._4x9_._48-k:visible'))
  visible_count = 0
  console.log("The following like buttons are visible")

  for (i=0;i<Object.keys(z).length;i++){
    if (z[i][1] == true){
      z[i][0].id = btnid;
      // console.log(z[i][0]);
      console.log("Visible button ID: "+btnid);
      lastbt = z[i][0];
      reactkey = Object.keys(lastbt)[1];
      console.log(reactkey[1]);
      visible_count ++;
      btnid++;
    }
    // && z[i][0].nextElementSibling != undefined)
    if (z[i][1] == true && $(z[i][0]).attr("data-testid") == "fb-ufi-likelink"){
          // z[i][0].click();
          console.log("Clicking on the reactions trigger sibling");
          // console.log(z[i][0].nextElementSibling);
          z[i][0][reactkey].onMouseEnter();
          // z[i][0].nextElementSibling.click();
          setTimeout(function(){
          $("._1oxk").hide();
          },200);
      }
  }
  console.log("There were "+visible_count+" visible buttons");

  setTimeout(function(){
    spanlist = $("._iuw");

    if (spanlist.length == 6){
      var reactions = spanlist
      // setTimeout(function(){
      //   sliced[0].click();
      // },150);
    } else {
      var sliced = Array.prototype.slice.call(spanlist, spanlist.length-visible_count*6);
      reactions = sliced;
      // setTimeout(function(){
      //   sliced[0].click();
      // },150);
      // setTimeout(function(){
      //   sliced[6].click();
      // },150);
    }

    console.log(spanlist);
    console.log(reactions);
    console.log("=============================");
  },1000);

  // var spanlist = $("._iuw");
  // console.log(spanlist);

  // if (spanlist.length == 6){
  //   var sliced = spanlist;
  // } else {
  //   var sliced = Array.prototype.slice.call(spanlist, spanlist.length-visible_count*6);
  // }
  //
  // console.log("Sliced");
  // console.log(sliced);

};
