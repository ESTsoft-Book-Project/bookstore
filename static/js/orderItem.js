import {
    elementResponseMapper as mapper,
    orderElementOrder as order,
} from "./constants.js";

/**
 * 
 * @param {JSON} item 
 * @returns 장고 키값으로 이루어진 JSON 객체를 이쁘게 만들어준다.
 * 
 * 참고: `static/js/constants.js` :: `elementResponseMapper`
 */
export function convertToJsObject(item) {
    let ret = new Object();
    for (const frontEndKey of Object.keys(mapper)) {
        ret[frontEndKey] = item[mapper[frontEndKey]];
    }
    return ret;
}

/**  
 * 아이템의 초기값을 가지고 테이블 한 행을 만든다.
*/
export function itemHtmlMapper(item) {
    const tr = document.createElement("tr");
    const handle = item.productHandle;

    for (const key of order) {
        const value = item[key];

        const td = document.createElement("td");
        switch (key) {
            case "quantity":
                td.innerHTML = `
        <a 
          key="${key}"
          id="quantity-${handle}" 
          type="number" 
          label="cartItem">
          ${value}
        </a>
        `;
                break;
            case "productName":
                td.innerHTML = `
        <a 
          key="${key}">
          ${item.productName}
        </a>
        `;
                break;
            case "productPrice":
                td.setAttribute("key", key);
                td.id = `price-${handle}`;
                td.innerText = `${value} 원`;
                break;
            case "imageUrl":
                td.innerHTML = `
        <img 
          key="${key}"
          src="${item.imageUrl}" 
          alt="image-${handle}"
          width="200"
        >
        `;
                break;
            case "product_total":
                td.innerHTML = `
        <a 
          key="${key}"
          id="productTotal-${handle}" 
          type="number" 
          >
          ${item.productPrice * item.quantity}
        </a>
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

/**
 * HTML 원소의 자식들을 Object로 반환한다. 
 * @param {HTMLElement} element 
 */
export function getChildDictFrom(element) {
    return Object.fromEntries(
        order.map((key) => [key, element.querySelector(`[key=${key}]`)])
    );
}

/**
 * sum of checked products price multiplied by quantity
 */
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
