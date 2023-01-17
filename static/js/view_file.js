document.addEventListener("DOMContentLoaded", function(){
    // Export file as PDF
    const exportBtn = document.querySelector("#exportPDF-btn");
    var name = document.querySelector('.file-name').innerHTML;
    exportBtn.addEventListener("click", ()=>{
        const printouter = document.querySelector("#print-outer-div")
        var opt = {
            filename: name,
            margin: 10,
            html2canvas: { scrollY: 0, width: 1040, height: 1471 }
        }
        html2pdf().set(opt).from(printouter).save()
    });
});
