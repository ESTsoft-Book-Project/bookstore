import {
  elementResponseMapper as mapper,
  cartElementOrder as order,
} from "./constants.js";

export function convertToJsObject(item) {
  let ret = new Object();
  for (const frontEndKey of Object.keys(mapper)) {
    ret[frontEndKey] = item[mapper[frontEndKey]];
  }
  return ret;
}

// 아이템의 초기값을 가지고 테이블 한 행을 만든다.
export function itemHtmlMapper(item) {
  const tr = document.createElement("tr");
  const handle = item.productHandle;

  for (const key of order) {
    const value = item[key];

    const td = document.createElement("td");
    switch (key) {
      case "checked":
        td.innerHTML = `
        <input 
          key="${key}"
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
          key="${key}"
          id="quantity-${handle}" 
          type="number" 
          label="cartItem"
          value="${value}">
        `;
        break;
      case "productName":
        td.innerHTML = `
        <a 
          key="${key}"
          href="${item.bookUrl}">
          ${item.productName}
        </a>
        `;
        break;
      case "productPrice":
        td.setAttribute("key", key);
        td.id = `price-${handle}`;
        td.innerText = `${value * item.quantity} 원`;
        break;
      case "imageUrl":
        td.innerHTML = `
        <img 
          key="${key}"
          src="${item.imageUrl}" 
          alt="image-${handle}"
          width="350"
        >
        `;
        break;
      case "delete":
        td.innerHTML = `
        <button 
          key="${key}"
          id="delete-${handle}" 
          type="submit">
            삭제
        </button>
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

export function getChildDictFrom(element) {
  return Object.fromEntries(
    order.map((key) => [key, element.querySelector(`[key=${key}]`)])
  );
}

export function totalSum(products) {
  return products
    .filter((e) => e.checked)
    .reduce(
      (partialSum, product) => {
        return partialSum +
        parseInt(product.productPrice) * parseInt(product.quantity)
      },
      0
    );
}
