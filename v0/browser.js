const WIDTH = 1000;
const SVG_NS = "http://www.w3.org/2000/svg";

let genes = [];
let chromSizes = {};
let chrom = "";
let viewStart = 0;
let viewEnd = 0;

function toPixel(pos) {
  return (pos - viewStart) / (viewEnd - viewStart) * WIDTH;
}

function draw() {
  const svg = document.getElementById("track");
  svg.innerHTML = "";

  const line = document.createElementNS(SVG_NS, "line");
  line.setAttribute("x1", 0);
  line.setAttribute("y1", 60);
  line.setAttribute("x2", WIDTH);
  line.setAttribute("y2", 60);
  line.setAttribute("stroke", "gray");
  svg.appendChild(line);

  const visible = genes.filter(g =>
    g.chrom === chrom && g.end > viewStart && g.start < viewEnd
  );

  for (const g of visible) {
    const x1 = toPixel(g.start);
    const x2 = toPixel(g.end);

    const rect = document.createElementNS(SVG_NS, "rect");
    rect.setAttribute("x", x1);
    rect.setAttribute("width", Math.max(1, x2 - x1));
    rect.setAttribute("y", g.strand === "+" ? 40 : 65);
    rect.setAttribute("height", 15);
    rect.setAttribute("fill", g.biotype === "protein_coding" ? "steelblue" : "darkorange");
    svg.appendChild(rect);
  }

  document.getElementById("region").textContent = `${chrom}: ${visible.length} genes`;
}

function showChrom(name) {
  chrom = name;
  viewStart = 0;
  viewEnd = chromSizes[name];
  draw();
}

async function main() {
  const response = await fetch("../data/genes.json");
  genes = await response.json();

  const sizesResponse = await fetch("../data/chrom.sizes");
  const sizesText = await sizesResponse.text();
  for (const row of sizesText.trim().split("\n")) {
    const [name, size] = row.split("\t");
    chromSizes[name] = Number(size);
  }

  const select = document.getElementById("chromSelect");
  for (const name of Object.keys(chromSizes)) {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    select.appendChild(option);
  }
  select.addEventListener("change", () => showChrom(select.value));

  showChrom(select.value);
}

main();