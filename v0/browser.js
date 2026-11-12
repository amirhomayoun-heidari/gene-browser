const WIDTH = 1000;
const SVG_NS = "http://www.w3.org/2000/svg";

let viewStart = 0;
let viewEnd = 0;

function toPixel(pos) {
  return (pos - viewStart) / (viewEnd - viewStart) * WIDTH;
}

async function main() {
  const response = await fetch("../data/genes.json");
  const genes = await response.json();

  const chrom = "chr1";
  viewStart = 0;
  viewEnd = 63108402;

  const visible = genes.filter(g =>
    g.chrom === chrom && g.end > viewStart && g.start < viewEnd
  );
  console.log("genes on", chrom, ":", visible.length);

  const svg = document.getElementById("track");

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
}

main();