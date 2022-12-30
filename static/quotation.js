// keyCodesToAllow include: Backspace, Up/Down/Left/Right arrows
const keyCodesToAllow = [8, 37, 38, 39, 40]

$(document).ready(function(){
// Get plain text only when pasting (ps: plain text to include whitespace if possible)
    $('body').on('paste', '.quote-edit', function(e) {
        e.preventDefault()
        let text = (e.clipboardData || e.originalEvent.clipboardData).getData('text/plain')
        document.execCommand('insertText', false, text);
    });

    // Form submit as "EDIT" button
    const editBtn = $('#editQuote-btn')
    editBtn.click(function(e){
        if (editBtn.html() === "EDIT") {
            e.preventDefault();
            $('.quote-edit').attr('contentEditable', true).addClass('quote-edit-box');
            $('.items-plus').show();
            $('.row-delete').css('visibility', 'visible');
            $('#exportPDF-btn').prop('disabled', true).css('opacity', '50%').css('cursor', 'auto');
            editBtn.html("SAVE");
        } else if (editBtn.html() === "SAVE") {
        // as "SAVE" button
            // For all <p> content with the class ".quote-edit", copy from <p>(using id) to respective hidden textarea(using name) to submit to backend
            // INFO: textarea uses '\r\n' for line breaks instead of html <br>
            $('p.quote-edit, #total-money').each(function(){
                let user_input = ($(this).attr('id'))
                let text = this.innerHTML
                if (text.endsWith('</div>')) {
                    text = text.slice(0, -6);
                }
                $(`[name=${user_input}]`).html(text.replaceAll('<div>', '\r\n').replaceAll('</div>', '').replaceAll('<br>', '\r\n'));
            })

            // For each row in the table, create textareas with an incremental value in name (e.g. name=row1, name=row2) to send to backend
            let incremental = 1;
            $('#items-table tbody tr').each(function() {
                console.log($(this))
                $(this).find('.item-total').html($(this).find('.item-total').html().replace(/\D/g, ''));
                for (let i = 0; i < this.children.length; i++) {
                    // Create a new textarea to submit for each cell
                    let new_row = document.createElement("textarea");
                    new_row.setAttribute('name', `row${incremental}`);
                    new_row.setAttribute('class', 'hidden-form');
                    let text = this.children[i].innerHTML
                    if (text.endsWith('</div>')) {
                        text = text.slice(0, -6);
                    }
                    new_row.innerHTML = text.replaceAll('<div>', '').replaceAll('</div>', '\r\n').replaceAll('<br>', '\r\n');
                    $('#submit').append(new_row);
                }
                incremental++;
            });
        };
    });


    // ADD ROW BUTTON
    const addRowBtn = document.getElementById('items-plus');
    const tbodyRef = document.getElementById('items-table').getElementsByTagName('tbody')[0];
    addRowBtn.addEventListener('click', function() {
        const previousIndex = $('#items-table tbody tr:last').find('.item-index').html();
        const newIndex = parseInt(previousIndex) + 1 || '#';
        let newRow = tbodyRef.insertRow();
        let Cell1 = newRow.insertCell();
        Cell1.innerHTML = newIndex.toLocaleString('en-US', {minimumIntegerDigits: 2});
        Cell1.className = 'item-index quote-edit';
        let Cell2 = newRow.insertCell();
        Cell2.innerHTML = '[Line Item Here]'
        Cell2.className = 'item-description quote-edit';
        let Cell3 = newRow.insertCell();
        Cell3.innerHTML = '1';
        Cell3.className = 'item-unit quote-edit';
        let Cell4 = newRow.insertCell();
        Cell4.innerHTML =  0;
        Cell4.className = 'item-rate quote-edit';
        let Cell5 = newRow.insertCell();
        Cell5.className = 'item-total'
        let Cell6 = newRow.insertCell();
        Cell6.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.2.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M160 400C160 408.8 152.8 416 144 416C135.2 416 128 408.8 128 400V192C128 183.2 135.2 176 144 176C152.8 176 160 183.2 160 192V400zM240 400C240 408.8 232.8 416 224 416C215.2 416 208 408.8 208 400V192C208 183.2 215.2 176 224 176C232.8 176 240 183.2 240 192V400zM320 400C320 408.8 312.8 416 304 416C295.2 416 288 408.8 288 400V192C288 183.2 295.2 176 304 176C312.8 176 320 183.2 320 192V400zM317.5 24.94L354.2 80H424C437.3 80 448 90.75 448 104C448 117.3 437.3 128 424 128H416V432C416 476.2 380.2 512 336 512H112C67.82 512 32 476.2 32 432V128H24C10.75 128 0 117.3 0 104C0 90.75 10.75 80 24 80H93.82L130.5 24.94C140.9 9.357 158.4 0 177.1 0H270.9C289.6 0 307.1 9.358 317.5 24.94H317.5zM151.5 80H296.5L277.5 51.56C276 49.34 273.5 48 270.9 48H177.1C174.5 48 171.1 49.34 170.5 51.56L151.5 80zM80 432C80 449.7 94.33 464 112 464H336C353.7 464 368 449.7 368 432V128H80V432z"/></svg>'
        Cell6.className = 'row-delete'
        $('td.quote-edit').attr('contentEditable', true).addClass('quote-edit-box');
        $('.row-delete').css('visibility', 'visible');
    });


    // ALLOW ONLY NUMBERS INPUT FOR 'INDEX' AND 'UNIT'
    $('#items-table tbody').on('keydown', '.item-index, .item-unit', function(e){
        if (isNaN(e.key) && !keyCodesToAllow.includes(e.keyCode)) {
            return false;
        }
    });

    // ALLOW ONLY NUMBERS AND "$" SIGN INPUT FOR 'RATE'
    $('#items-table tbody').on('keydown', '.item-rate', function(e){
        if (isNaN(e.key) && !keyCodesToAllow.includes(e.keyCode) && e.key !== "$") {
            return false;
        }
    });

    // UPDATE RATES REAL-TIME
    $('#items-table tbody').on('blur', '.item-unit, .item-rate', function(){
        // FOR CURRENT ROW
        currentRow = $(this).parent()
        let unit = currentRow.find('.item-unit').html().replace(/\D/g, '') || 0;
        let rate = currentRow.find('.item-rate').html().replace(/\D/g, '') || 0;
        let total = unit * rate;
        currentRow.find('.item-total').html(total);

        // FOR WHOLE TABLE
        let totaltotal = 0;
        $('#items-table tbody .item-total').each(function() {
            if ($(this).html()) {
                totaltotal += parseInt($(this).html().replace(/\D/g, ''));
            }
        });
        $('#total-money').html(totaltotal);
    });

    // DELETE ROW BUTTON
    // - Delete Function
    $('tbody').on('click', '.row-delete', function(){
        $(this).parent().remove();
    })

    // - Hover Effects
    $('tbody').on('mouseenter', '.row-delete', function(){
        $(this).parent().find('td').css('background-color', 'rgb(179, 179, 179)')
    }).on('mouseleave', '.row-delete', function() {
        $(this).parent().find('td').css('background-color', '')
    });

});
