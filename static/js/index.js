document.addEventListener("DOMContentLoaded", function(){
    // Functions defined in main.js
    relativeTime($('.latest-table-date'));
    goToRespective('quotation', $('#quotations tr'))
    goToRespective('invoice', $('#invoices tr'))
});
