const addExpenseButton = document.querySelector("#add-exp-form");
const addConditionButton = document.querySelector("#add-cond-form");

const expenseForm = document.getElementsByClassName("expForm");
const conditionForm = document.getElementsByClassName("condForm");
const mainForm = document.querySelector("#main-form");

const expFormMeta = document.getElementById("expFormMetadata");
const condFormMeta = document.getElementById("condFormMetadata");
const expTotalForms = expFormMeta.children[1];
const condTotalForms = condFormMeta.children[1];

let expFormCount = expenseForm.length - 1;
let condFormCount = conditionForm.length - 1;

addExpenseButton.addEventListener("click", function(event){
    event.preventDefault();
    const newExpenseForm = expenseForm[0].cloneNode(true);
    const formRegex = RegExp(`form-(\\d){1}-`, 'g');
    expFormCount++;

    newExpenseForm.innerHTML = newExpenseForm.innerHTML.replace(formRegex, `form-${expFormCount}-`);
    mainForm.insertBefore(newExpenseForm,addExpenseButton);
    expTotalForms.setAttribute('value', `${expFormCount + 1}`);
});

addConditionButton.addEventListener("click", function(event){
    event.preventDefault();
    const newConditionForm = conditionForm[0].cloneNode(true);
    const formRegex = RegExp(`form-(\\d){1}-`, 'g');
    condFormCount++;

    newConditionForm.innerHTML = newConditionForm.innerHTML.replace(formRegex, `form-${condFormCount}-`);
    mainForm.insertBefore(newConditionForm,addConditionButton);
    condTotalForms.setAttribute('value', `${condFormCount + 1}`);
});

mainForm.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-exp-form")) {
        event.preventDefault();
        event.target.parentElement.remove();
        expFormCount--;
        expTotalForms.setAttribute('value', `${expFormCount + 1}`);
    }
    else if(event.target.classList.contains("remove-cond-form")) {
        event.preventDefault();
        event.target.parentElement.remove();
        condFormCount--;
        condTotalForms.setAttribute('value', `${condFormCount + 1}`);
    }
});
