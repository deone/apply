$(function() {
  var $topLoader = $("#topLoader").percentageLoader({
    width: 256, height: 256, controllable: true, progress: 0.5, onProgressUpdate: function (val) {
      this.setValue(Math.round(val * 100.0) + 'kj');
    }
  });

  var topLoaderRunning = false;

  /* Some browsers may load in assets asynchronously. If you are using the percentage
    * loader as soon as you create it (i.e. within the same execution block) you may want to
    * wrap it in the below `ready` function to ensure its correct operation
    */
  $topLoader.percentageLoader({onready: function () {
    if (topLoaderRunning) {
      return;
    }
    topLoaderRunning = true;

    var kb = 0;
    var totalKb = 999;

    var animateFunc = function () {
      kb += 17;
      $topLoader.percentageLoader({progress: kb / totalKb});
      $topLoader.percentageLoader({value: (kb.toString() + 'kb')});

      if (kb < totalKb) {
        setTimeout(animateFunc, 25);
      } else {
        topLoaderRunning = false;
      }
    };

    setTimeout(animateFunc, 25);

  }});
});
