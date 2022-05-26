const m30 = [3,5,8,10];
const m31 = [0,2,4,6,7,9,11];

function getMonthNumber(month){
    if (month.includes("Jan")){
        return 0
    }
    else if(month.includes("Feb")){
        return 1
    }
    else if(month.includes("Mar")){
        return 2
    }
    else if(month.includes("Apr")){
        return 3
    }
    else if(month.includes("May")){
        return 4
    }
    else if(month.includes("Jun")){
        return 5
    }
    else if(month.includes("Jul")){
        return 6
    }
    else if(month.includes("Aug")){
        return 7
    }
    else if(month.includes("Sep")){
        return 8
    }
    else if(month.includes("Oct")){
        return 9
    }
    else if(month.includes("Nov")){
        return 10
    }
    else if(month.includes("Dec")){
        return 11
    }
}

function parseDate(date){
    arr = date.split(" ");
    let day = arr[1].split(",")[0];
    let year = arr[2];
    let month = getMonthNumber(arr[0]);
    var d = new Date();
    d.setFullYear(year,month,day);
    return d
}

function showExpiringNotification(){
    const creationDateText = document.getElementById("creation_date").innerText;
    const creationDate = parseDate(creationDateText);
    const type = document.getElementById("type").innerText;
    let currentDate = new Date();
    var timeDiff = Math.abs(currentDate.getTime() - creationDate.getTime());
    var daysDiff = Math.floor(timeDiff / (1000 * 3600 * 24));
    let message = "";
    let days = 0;
    if (type == "MONTH"){
        if (currentDate.getMonth() == 1){
            if (daysDiff >= 23){
                days = 28 - daysDiff;
            }
        }
        else{
            if (daysDiff >=28){
                if (m30.includes(currentDate.getMonth())){
                    days = 30 - daysDiff;
                }
                else if (m31.includes(currentDate.getMonth())){
                    days = 31 - daysDiff;
                }
            }
        }

    }
    else if (type == "QUART"){
        if (daysDiff >= 87){
            if (currentDate.getMonth >= 9){
                days = 92 - daysDiff;
            }
            else{
                days = 91 -daysDiff;
            }
        }
    }
    else if (type == "YEAR"){
        if (daysDiff >= 359){
            if ((currentDate.getFullYear() % 4) == 0){
                days = 366 - daysDiff;
            }
            else{
                days = 365 - daysDiff;
            }
        }
    }
    if(days == 0){
        message += "Budget expires today.";
    }
    else if (days < 0){
        message += "Budget expired " + Math.abs(days) + " days ago.";
    }
    else{
        message += "Budget expires in " + days + " days.";
    }
    if (daysDiff != 0){
        if (message.includes("Budget")){
            alert(message);
        }
    }
}

showExpiringNotification()