var ctx = document.getElementById('chartjs_chart').getContext("2d");

const myChart = new Chart(ctx, {
    type: "doughnut", //ye chart ki type hai
    data: { //ye overall data object hota jo ham pass karty han
        labels: [
            'Marketing',
            'Fuel',
            'Taxes',
            'Earth',
            'Payroll'
        ], //label jo nichy atya han 
        datasets: [{
            data: [13, 25, 6, 34, 45],
            backgroundColor: [
                'rgb(255, 205, 86)',
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(34, 139, 34)',
                'rgb(0, 255, 255)'
            ],
            hoverOffset: 6
        }]
    },
    //configuration for graph
    options: {
        responsive: true, // by default ye true hota jis say responsive rahta hai height or width ma farak nahi parta 
        layout: { //1 property layout ma ham different properties day sakty han like padding,margin
            padding: { //
                // left: 30,
                // right: 5,
                top: 4,
                // bottom: 0,
            },
        },
        tooltips: { //2-property 
            enabled: true, //bydefault ye true hota hai jis say tooltips show hota hai
            //enabled:false, //false say tooltips show nhi hota
            backgroundColor: "Red", // tooltips ka color is say rakhty hai
        },
        plugins: { //3 property
            title: {//3-A-part property
                //  display: true,
                //  text: "This Year",
                //  position: 'top',
                 //fontSize: 40,
                // fontStyle: "italic",
                //padding:20,
            },
            legend: { //3-B-part property jo uper chota color ban k ata
                display: true,
                position: 'bottom',
                align: 'start',
                labels: {
                    // color: 'red',
                    fontSize: 25,
                    boxWidth: 40, // box ki length
                }
            },
        },//yahan pay plugins khatam ho rha 

        animation: { //4 property
            duration: 2000,
            easing: "easeInOutBounce",
        }, //animation khatam ho rhi hai
    },//yahan option end ho rha hai

});