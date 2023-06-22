import { elementResponseMapper } from "./contants.js";

export function itemHtmlMapper(item) {
  const tr = document.createElement("tr");

  for (const [frontKey, backKey] of Object.entries(elementResponseMapper)) {
    console.log(`${frontKey}: ${item[backKey]}`);
  }

  return tr;
}
