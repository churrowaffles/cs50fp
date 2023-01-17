// Open and close a pop-up box (To create files or edit file names)
function popUp(triggerButton, shownElement, displayAction) {
    triggerButton.click(function(){
        shownElement.css("display", displayAction);
    });
};

// Set relative time using library "dayjs"
function relativeTime(timings) {
    (timings).each(function() {
        date = this.innerHTML;
        localdate = new Date(date + "Z");
        this.innerHTML = dayjs(localdate).fromNow();
    });
}

// Directs user to the file they clicked on
function goToRespective(type, triggers) {
    triggers.click(function() {
        id = $(this).find('input[name=id]').val();
        window.location.href = `/${type}s/${id}`;
    });
}


document.addEventListener("DOMContentLoaded", function(){

    // TEXT AREA AUTOSIZE
    autosize($('textarea'));
    $('textarea').css("resize", "none");

    // SIDE BAR
    const sidebarWrapper = document.getElementById("sidebar-wrapper")
    const pageContents = document.querySelector(".page")

    document.getElementById("menuButton").addEventListener("click", function(){
        sidebarWrapper.style.left = "0rem";
        pageContents.style.paddingLeft = "14rem";
    });

    document.getElementById("close-sidebar").addEventListener("click", function(){
        sidebarWrapper.style.left = "-15rem";
        pageContents.style.paddingLeft = "0rem";
    });

    // CREATE QUOTE AND INVOICE - POP-UP BOXES
    createQuotePopUpBox = $('#create_quote_popup')
    popUp($('#create_quote, #index_create_quote, #home_create_quote'), createQuotePopUpBox, "flex");
    popUp($('#close_quote, #popup-btn'), createQuotePopUpBox, "none");
    createInvoicePopUpBox = $('#create_invoice_popup')
    popUp($('#create_invoice, #index_create_invoice, #home_create_invoice'), createInvoicePopUpBox, "flex");
    popUp($('#close_invoice, #popup-btn'), createInvoicePopUpBox, "none");

    // FLASH MESSAGES DURATION
    $('.flash-msg').delay(2000).slideUp(600)

});
