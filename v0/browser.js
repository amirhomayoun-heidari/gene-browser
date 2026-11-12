async function main() {
  const response = await fetch("../data/genes.json");
  const genes = await response.json();

  console.log("genes loaded:", genes.length);
  console.log("first gene:", genes[0]);
}

main();