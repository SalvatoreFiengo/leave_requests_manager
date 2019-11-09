
let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

let startDate = new Date(2018,1,1);
let endDate = new Date(startDate.getFullYear()+1,12,0);
let months = ['January','February','March','April','May','June','July','August','September','October','November','Dicember'];
let weekDays = ['Sunday','Monday','Tuesday','Wensday','Thursday','Friday','Saturday'];

let startDateMillSec = startDate.getTime();
let lastDateMillSec = endDate.getTime();
let yearDays= [];
let monthDays = [];
let lastDayOfMonth;
let weeksInAMonth;

function getMonthDays(month, year=currentYear){
    end = new Date(year, month, 0);
    for(i=0; i< end.getDate();i++){
        monthDays.push(new Date(year,month,i))
    } 
    return i
};

let year = 2018;
let endyear=2019;

let month=0;
let day=0;
let dayName;
let weeksNumber=1;

function getYearDays(){
    if(year == endyear){
        return
    }

    day++
    yearDays.push(new Date(year,month,day))
    if(day == new Date(year,month+1,0).getDate()){
        month++
        day=0;
        if(month == 12){
            year++
            month=0
        }
    }
    getYearDays();
}
function get_weeksNumber(){
    for(i=0;i<yearDays.length;i++){
        if(i%7==0){
            weeksNumber++
        }
    }
    return weeksNumber
}
getYearDays();
weeksNumber=get_weeksNumber();

lastDayOfMonth=getMonthDays(currentMonth+1);
weeksInAMonth=Math.ceil(lastDayOfMonth/7);




