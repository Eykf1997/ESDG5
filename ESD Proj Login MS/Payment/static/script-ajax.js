var increasebutton = document.getElementsByClassName('quantity-right-plus')
for(let i=0; i<increasebutton.length;i++){
    increasebutton[i].addEventListener('click',increasing)}
function increasing(i){
    i.target.parentNode.children[1].value = Number(i.target.parentNode.children[1].value) + 1}

var decreasebutton = document.getElementsByClassName('quantity-left-minus')
for(let i=0; i<decreasebutton.length;i++){
    decreasebutton[i].addEventListener('click',decreasing)}
function decreasing(i){
    if(i.target.parentNode.children[1].value > 1){
    i.target.parentNode.children[1].value = Number(i.target.parentNode.children[1].value) - 1}}

var buybutton = document.getElementsByClassName('buy_now_btn')
for(let i=0; i<buybutton.length;i++){
    buybutton[i].addEventListener('click',stripepay)
}
function stripepay(i){
    var quantity = i.target.parentNode.parentNode.children[1].value
    var product = i.target.id
    fetch('/stripe_pay',{
        method:"POST",
        headers:{
            'Content-Type':'application/json',
        }
        ,
        body:JSON.stringify({
            'quantity':quantity,
            'product': product
        })
    })
    .then((result) => { return result.json(); })
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            sessionId: data.checkout_session_id
        }).then(function (result) {
        });
    })
}

