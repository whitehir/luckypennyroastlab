  (function() {
    var node = document.querySelector(".htmlmenu-header");
    var stop = node.offsetTop;
    var window_last_position = 0;
    var scroll = window.requestAnimationFrame ||
      window.webkitRequestAnimationFrame ||
      window.mozRequestAnimationFrame ||
      window.msRequestAnimationFrame ||
      window.oRequestAnimationFrame ||
      // IE Fallback, you can even fallback to onscroll
      function(callback) {
        window.setTimeout(callback, 1000 / 60)
      };

    var loop = function() {
      // avoid calculations if not needed
      if (window_last_position === window.pageYOffset) {
        scroll(loop);
        return false;
      } else window_last_position = window.pageYOffset;

      //... calculations
      if (window_last_position > stop) {
        // stick the div
        if (node.className.indexOf(" htmlmenu-header-scrolled") === -1) {
          node.className = node.className + ' htmlmenu-header-scrolled';
        }
      } else {
        // release the div
        node.className = node.className.indexOf(' htmlmenu-header-scrolled') >= 0 ? node.className.replace(' htmlmenu-header-scrolled', '') : node.className;
      }

      scroll(loop);
    };

    // call the loop for the first time
    loop();
  })();
