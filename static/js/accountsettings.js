document.addEventListener("DOMContentLoaded", function(){
    $('.right-col textarea, .right-col input').on("focus", function() {
        $(this).parent().toggleClass('accountsettings-edit')
    }).on("blur", function() {
        $(this).parent().toggleClass('accountsettings-edit');
    })
});
