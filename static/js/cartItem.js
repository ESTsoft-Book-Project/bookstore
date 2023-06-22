import {
  elementResponseMapper as mapper,
  cartElementOrder as order,
} from "./contants.js";

// 아이템의 초기값을 가지고 테이블 한 행을 만든다.
export function itemHtmlMapper(item) {
  const tr = document.createElement("tr");
  const handle = item[mapper.productHandle];
  const name = item[mapper.productName];

  for (const frontKey of order) {
    const backKey = mapper[frontKey];
    console.log(`${frontKey}: ${item[backKey]}`);

    const td = document.createElement("td");
    switch (frontKey) {
      case "checked":
        td.innerHTML = `
        <input id="checkbox-${handle}" type="checkbox">
        `;
        break;
      case "quantity":
        td.innerHTML = `
        <input 
          id="quantity-${handle}" 
          type="number" 
          value="${item[mapper.quantity]}">
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
        td.innerText = `${item[mapper.productPrice]} 원`;
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
        <button id="{{ i.product.handle }}-deleteBtn" type="submit">삭제</button>
        `;
        break;
      default:
        console.error(`${frontKey} does not match any predefined mapper!`);
        break;
    }
    console.log(td);
    tr.appendChild(td);
  }

  return tr;
}
