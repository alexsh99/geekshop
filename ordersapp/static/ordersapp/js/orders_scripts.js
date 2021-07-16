window.onload = function () {

    $('.formset_row').formset({
        addText: 'Добавить',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];
    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for(let i=0; i < total_forms; i++){
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',','.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    $('.order_form')
        .on('click', 'input[type=number]', function(){
            orderitem_num = parseInt(this.name.replace('orderitems-', '').replace('-quantity',''));
            if (price_arr[orderitem_num]){
                orderitem_quantity = this.value;
                delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
                quantity_arr[orderitem_num] = orderitem_quantity;
                orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
            }
        })
        .on('click', 'input[type=checkbox]', function(){
            orderitem_num = parseInt(this.name.replace('orderitems-', '').replace('-DELETE',''));
            if (this.checked){
                delta_quantity = -quantity_arr[orderitem_num];
            } else {
                delta_quantity = quantity_arr[orderitem_num];
            }
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        })
        .on('change', 'select', function(){
            let product_pk = $(this).find('option:selected').val();
            let orderitem_num = parseInt(this.name.replace('orderitems-', '').replace('-product', ''));

            if (orderitem_num && product_pk){
                $.ajax({
                url: "/products/" + product_pk,
                success: function(data) {
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price);
                        if (isNaN(quantity_arr[orderitem_num])) quantity_arr[orderitem_num] = 0;
                        let price_span = '<span class="orderitems-' + orderitem_num + '-price">' + data.price.toString().replace('.', ',') + '</span> руб';
                        let cur_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        cur_tr.find('td:eq(2)').html(price_span);
                    }
                }
                });
            }
        });

    function deleteOrderItem(row){
        let target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity',''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').text(order_total_quantity.toString());
        $('.order_total_cost').text(order_total_price.toString())
    };
}