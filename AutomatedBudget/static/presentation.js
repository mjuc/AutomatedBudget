function extractText(html){
    return html.textContent || html.innerText
}
 
function parseDocument(){
    var budgetHeaders = document.getElementsByClassName("budget-header");
    let length = budgetHeaders.length;
    for(let i=0;i<length;i++){
        let html = extractText(budgetHeaders[i]);
        if (html.includes("MONTH")){
            budgetHeaders[i].innerHTML = "Monthly budget";
        }
        else if (html.includes("QUART")){
            budgetHeaders[i].innerHTML = "Quarterly budget";
        }
        else if (html.includes("YEAR")){
            budgetHeaders[i].innerHTML = "Yearly budget";     
        }
    }
}

parseDocument()