function calculateNeededAmount(){
    var income = document.getElementById("income").innerHTML;
    const expenses = document.getElementsByClassName("exp");
    var expSum = 0
    for (let i = 0;i<expenses.length;i++){
        expSum += expenses[i].innerText.split(" ")[1];
    }
    return Math.abs(income - expSum)
}

function creditSuggestion(){
    const annotation = document.getElementById("base_line_annotation").innerText;
    if (annotation.includes("LOSS")){
        var neededAmount = calculateNeededAmount();
        alert("Spending target for this budget cycle is not achievable without loan.\nYou need a loan of at least: " + neededAmount + " of your currency of choice.");
    } 
}

creditSuggestion()