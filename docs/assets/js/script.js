document.addEventListener("DOMContentLoaded", function() {
  var toc = document.getElementById("toc");
  if (toc) {
    var headings = document.querySelectorAll(".content h1, .content h2, .content h3, .content h4, .content h5, .content h6");
    if (headings.length > 1) {
      headings = Array.from(headings);
      headings.forEach(function(heading) {
        var link = document.createElement("a");
        link.textContent = heading.textContent;
        link.href = "#" + heading.id;
        link.style.display = "block";
        link.style.marginLeft = heading.tagName.toLowerCase() === "h2" ? "0" : "10px";
        toc.appendChild(link);
      });
    } else {
      toc.style.display = "none";
    }
  }
});
