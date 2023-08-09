
var data_CB = window.data_CB;
var data_AT = window.data_AT;
var dataBudget = window.data_budget;

var ctx = document.getElementById('myChart').getContext('2d');
var data = data_CB;
var myChart = new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
        maintainAspectRatio: false,
        responsive: true
    }
});

var ctx = document.getElementById('myChart2').getContext('2d');
var data = data_AT;
var myChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
        maintainAspectRatio: false,
        responsive: true
    }
});


var ctx = document.getElementById('myChart3').getContext('2d');
var data = dataBudget
var myChart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
        maintainAspectRatio: false,
        responsive: true
    }
});