// Zooming and moving of the diagram on the "Schema diagram" page.
//
// Mermaid scales a diagram down to the space that it gets, which leaves the
// diagram of the whole schema too small to read.
document.addEventListener("DOMContentLoaded", function () {
  var box = document.querySelector(".schema-diagram");
  if (!box || !window.svgPanZoom) {
    return;
  }

  function enable(svg) {
    var panZoom = svgPanZoom(svg, {
      controlIconsEnabled: true,
      // with the default of 0.1 it takes some twenty turns of the wheel to get
      // from the whole diagram to text that can be read
      zoomScaleSensitivity: 0.3,
    });
    window.addEventListener("resize", function () {
      panZoom.resize();
      panZoom.fit();
      panZoom.center();
    });
  }

  // mermaid draws the diagram after the page has loaded
  var observer = new MutationObserver(function () {
    var svg = box.querySelector("svg");
    if (svg) {
      observer.disconnect();
      enable(svg);
    }
  });
  observer.observe(box, { childList: true, subtree: true });
});
