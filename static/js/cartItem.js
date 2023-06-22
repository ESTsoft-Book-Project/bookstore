function cartItemToTable(item) {
  const tr = document.createElement("tr");

  for (i of item) {
    const td = document.createElement("td");
    tr.appendChild(td);
  }

  return tr;
}
