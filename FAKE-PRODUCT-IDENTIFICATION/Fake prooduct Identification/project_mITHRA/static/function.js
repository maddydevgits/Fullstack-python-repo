
function dataSend(key, products){
    let send_data = JSON.stringify(products);
    localStorage.setItem(key,send_data);
}

function dataGet(key){
    let prod_get = localStorage.getItem(key);

    return JSON.parse(prod_get)

}