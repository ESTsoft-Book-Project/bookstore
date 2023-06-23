import {
  elementResponseMapper as mapper,
  cartElementOrder as order,
} from "./contants.js";

// 아이템의 초기값을 가지고 테이블 한 행을 만든다.
export function itemHtmlMapper(item) {
  const tr = document.createElement("tr");
  const handle = item[mapper.productHandle];
  const name = item[mapper.productName];

  for (const key of order) {
    const value = item[mapper[key]];

    const td = document.createElement("td");
    switch (key) {
      case "checked":
        td.innerHTML = `
        <input 
          id="checkbox-${handle}" 
          type="checkbox" 
          label="cartItem"
          ${value ? "checked" : ""}
        >
        `;
        break;
      case "quantity":
        td.innerHTML = `
        <input 
          id="quantity-${handle}" 
          type="number" 
          label="cartItem"
          value="${value}">
        `;
        break;
      case "productName":
        td.innerHTML = `
        <a href="${item[mapper.bookUrl]}">
          ${name}
        </a>
        `;
        break;
      case "productPrice":
        td.id = `price-${handle}`;
        td.innerText = `${value} 원`;
        break;
      case "imageUrl":
        td.innerHTML = `
        <img 
          src="${item[mapper.imageUrl]}" 
          alt="image-${handle}"
          width="350"
        >
        `;
        break;
      case "delete":
        td.innerHTML = `
        <button id="delete-${handle}" type="submit">삭제</button>
        `;
        break;
      default:
        console.error(`${key} does not match any predefined mapper!`);
        break;
    }
    tr.appendChild(td);
  }

  return tr;
}
