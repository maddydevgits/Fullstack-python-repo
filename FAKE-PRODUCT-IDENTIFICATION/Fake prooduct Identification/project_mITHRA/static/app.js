
const add_product_btn = document.getElementById('add_product_btn');
const add_product_box = document.getElementById('add_product_box');
const btn_close       = document.getElementById('btn-close');
const apply           = document.getElementById('apply');
const products_output = document.getElementById('products_output');

add_product_btn.addEventListener('click',function() {
    add_product_box.style.transform="scaleY(1)"
});
btn_close.addEventListener('click',function() {
    add_product_box.style.transform="scaleY(0)";
});

apply.addEventListener('submit', function(e) {

    e.preventDefault();
   let title  = this.querySelector('input[name="title"]').value;
   let img    = this.querySelector('input[name="img"]').value;
   let desc   = this.querySelector('textarea[name="desc"]').value;
   let cat    = document.querySelectorAll('input[name="cate"]:checked');
   let rPrice = this.querySelector('input[name="rPrice"]').value;
   let sPrice = this.querySelector('input[name="sPrice"]').value;

   
   let rp;
   let sp;

   if (sPrice == ''){
    rp = `${rPrice}$`;
   }else{
    rp =`<del class="del_price">${rPrice}$</del>`;
   }


   if (sPrice == ''){
    sp = `<span style="display:none">${sPrice}$</span>`
   }else{
    sp = `<span>${sPrice}$</span>`
   }




   let cat_arr=[];

   for (let i = 0; i < cat.length; i++) {
       cat_arr.push(cat[i].value)}
       

    let products_arr;
    if(dataGet("product")){
        products_arr = dataGet("product"); 
    }else{
        products_arr = [];
    }

products_arr.push({
        title  : title,
        img    : img,
        desc   : desc,
        cat    : cat_arr,
        rPrice : rp,
        sPrice : sp
})
   
    if (rPrice == '') {
        dataSend("Not", products_arr);   
    }else {
        dataSend("product", products_arr);
    }

    if (rPrice == '') {
        alert ('Please Input Your Regular Price')    
    }else{
        product_grid()
    }

  
})



product_grid()
function product_grid(){
    let prod_get = dataGet("product");
    let prod_grid= '';
    
    prod_get.map(data => {
    
    let cat_show = '';
    
    data.cat.map((cat_data) => {
    cat_show += `<span class="cat"> ${cat_data}</span>`
    })
    prod_grid +=`
   
        <div class="col-md-4 mb-3" id="list_items">
        <div id="list_grid">
            <div class="card text-center product-item">
                <div class="card-body">
                    <div id="list_left">
                        <div class="wishlist-addCard text-success">
                            <i class="far fa-heart"></i>
                            <i class="fas fa-cart-plus"></i>
                        </div>
                        <img class="card-img" object-fit="cover" width="200" height="150" src="${data.img}" alt="">
                    </div>
                    <div id="list_right">
                        <h6 class="mt-4">${cat_show}</h6>
                        <h3>${data.title}</h3>
                        <div class="price">
                            <span class="r_price">${data.rPrice}</span>
                            <span class="s_price">${data.sPrice}</span>
                        </div>
                        <button class="btn btn-success mt-2">Add To Card</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
    })
    
    products_output.innerHTML = prod_grid;
    
    }
    



const list       = document.getElementById('list');
const grid       = document.getElementById('grid');
const list_grid  = document.getElementById('list-grid');
const list_left  = document.getElementById('list-left');
const list_right = document.getElementById('list_right');


list.addEventListener('click', function(){
    list_grid.classList.add("row")
    list_left.classList.add("col-md-4")
    list_right.classList.add("col-md-8")
})
grid.addEventListener('click', function(){
    list_grid.classList.remove("row")
    list_left.classList.remove("col-md-4")
    list_right.classList.remove("col-md-8")
})