document.addEventListener("DOMContentLoaded", function(){
    // Functions have been defined in main.js
    relativeTime($('.latest-table-date'));
    goToRespective('quotation', $('#quotations tr'))
    goToRespective('invoice', $('#invoices tr'))
});
