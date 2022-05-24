const url = "http://127.0.0.1:8000" + document.getElementById("expenseUpdateURL").innerText;
const budgetContainer = document.getElementById("budget-container");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function getExpenseID(container){
    const expID = document.getElementById("exp-id-"+container.id).innerText;
    return expID;
}

function getUserID(container){
    const usrID = document.getElementById("usr-id-"+container.id).innerText;
    return usrID;
}

function getExpenseSpentSum(container){
    const spentSum = document.getElementById("spent-input-"+container.id).value;
    return spentSum;
}

budgetContainer.addEventListener("click",function(event){
    if (event.target.classList.contains("update-expense")){
        const parent = event.target.parentElement;
        spentSum = getExpenseSpentSum(parent);
        expID = getExpenseID(parent);
        usrID = getUserID(parent);
        const data = { "exp_id": expID,"expSpentSum": spentSum,"user_id": usrID};
        console.log(data);
        fetch(url,{method: "POST",
            headers:{"Content-Type": "application/json","X-CSRFToken":  csrftoken},
            mode: 'same-origin',
            body: JSON.stringify(data)}).then(data => data.json()).then((json) => {
                console.log(JSON.stringify(json));
            });
    }  
});
