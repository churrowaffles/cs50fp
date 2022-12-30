function editIndex(type) {
    editIndexBtn = $('button[name=edit]');
    editIndexBtn.click(function(){
        id = $(this).siblings('input[name=id]').val();
        $(`#edit_${type}_popup input[name=id]`).val(id);
        quote_name = $(this).parent().parent().siblings('.index-name').html();
        $(`#edit_${type}_popup input[name=name]`).val(quote_name);
        $(`#edit_${type}_popup`).css('display', 'flex');
        return false;
    });
};

document.addEventListener("DOMContentLoaded", function(){

    relativeTime($('tbody .index-date'));

    // Links user to selected row
    goToRespective('quotation', $('#quotation-index tbody tr'))
    goToRespective('invoice', $('#invoice-index tbody tr'))

    $('.payment-status').click(function(e) {
        e.stopPropagation();
    });

    $('.payment-status').on('change', function() {
        $(this).parent().submit();
    });

    $('.payment-status').each(function() {
        if ($(this).val() == 2) {
            $(this).css("background-color", "pink")
        } else if ($(this).val() == 3) {
            $(this).css("background-color", "palegreen")
        } else {
            $(this).css("background-color", "transparent")
        }
    })

    // Edit Quotation Name
    editIndex('quote');
    editIndex('invoice');

    popUp($('#close_quote, #close_invoice, #quote_popup-btn'), $('.popup-full'), "none");
});
