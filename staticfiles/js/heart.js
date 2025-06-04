document.addEventListener("DOMContentLoaded", function () {
  const svgNS = "http://www.w3.org/2000/svg";
  const xlinkNS = "http://www.w3.org/1999/xlink";

  // Skapa SVG-element
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("width", "400");
  svg.setAttribute("height", "400");
  svg.setAttribute("viewBox", "0 0 500 500");

  // Skapa path (hjärtat)
  const path = document.createElementNS(svgNS, "path");
  path.setAttribute("id", "heartPath");
  path.setAttribute("d", `
    M 250,300
    C 150,200 100,100 250,100
    C 400,100 350,200 250,300
    Z
  `);
  path.setAttribute("fill", "#ffe6e6");
  path.setAttribute("stroke", "#ff4d4d");
  path.setAttribute("stroke-width", "3");
  svg.appendChild(path);

  // Skapa text som följer path
  const text = document.createElementNS(svgNS, "text");
  text.setAttribute("font-size", "18");
  text.setAttribute("fill", "#cc0000");
  text.setAttribute("font-family", "Arial");
  text.setAttribute("font-weight", "bold");

  const textPath = document.createElementNS(svgNS, "textPath");
  textPath.setAttributeNS(xlinkNS, "xlink:href", "#heartPath");
  textPath.setAttribute("startOffset", "50%");
  textPath.setAttribute("text-anchor", "middle");
  textPath.textContent = "✨ Welcome to Handcraft Show Off ✨";

  text.appendChild(textPath);
  svg.appendChild(text);

  // Lägg till SVG i DOM
  const container = document.getElementById("heart-container");
  if (container) {
    container.appendChild(svg);
  } else {
    console.error("❌ Hittade inte #heart-container i DOM");
  }
});
