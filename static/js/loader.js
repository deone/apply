$(function() {
  var $topLoader = $("#topLoader").percentageLoader();

  var topLoaderRunning = false;

  /* Some browsers may load in assets asynchronously. If you are using the percentage
    * loader as soon as you create it (i.e. within the same execution block) you may want to
    * wrap it in the below `ready` function to ensure its correct operation
    */
  $topLoader.percentageLoader({onready: function () {
    
    // $topLoader.percentageLoader({progress: 0.1});
    if (topLoaderRunning) {
      return;
    }
    topLoaderRunning = true;

    var kb = 0;
    var totalKb = 999;

    var animateFunc = function () {
      kb += 17;
      progress = kb / totalKb;
      value = 0.2;

      $topLoader.percentageLoader({progress: progress});

      if (kb < totalKb && progress < value) {
        setTimeout(animateFunc, 25);
      } else {
        topLoaderRunning = false;
      }
    };

    setTimeout(animateFunc, 25);

  }});
});
