const ctx1 = document.getElementById('CashFlowChart').getContext("2d");

const myChart1 = new Chart(ctx1, {
    type: "bar", //ye chart ki type hai
    data: { //ye overall data object hota jo ham pass karty han
        labels: ["January", "February", "March", "April", "May", "June", "July","August","September","October","November","December"], //label jo nichy atya han 
        datasets: [ //ye dataset hai jis ma array or array k under objects bna sakty
            {
                label: "Monthly Report", //ye jo uper lable nazar ata
                data: [1, 2, -3, 8, -5, 6, 7,9,-6,-4,10,7], //ye wo data jo nazat ata chat k uper line ya dots pay
                borderColor: "Black", //border color
                backgroundColor: ["#66FF00", "#66FF00", "#91A3B0", "#66FF00", "#91A3B0", "#66FF00", "#66FF00","#66FF00","#91A3B0","#91A3B0","#66FF00","#66FF00"], //ye colors han
                //ham rgb ma be value day sakty han
                borderWidth: 0, //border ki width hai 
                order: 1,
            },
            {
                label: "Daily Report", //ye jo uper lable nazar ata
                data: [1, 2, -3, 6, -5, 6, 7,9,-4,-6,10,7], //ye wo data jo nazar ata chat k uper line ya dots pay
                // backgroundColor: ["Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "Brown"], //ye colors han
                backgroundColor: "Blue",
                //ham rgb ma be value day sakty han
                borderColor: "Black", //border color
                borderWidth: 1, //border ki width hai 
                type: 'line',
                order: 0,
            }
        ]
    },
    //configuration for graph
    options: {
        responsive: true, // by default ye true hota jis say responsive rahta hai height or width ma farak nahi parta 
        layout: { //1 property layout ma ham different properties day sakty han like padding,margin
            padding: { //
                // left: 30,
                // right: 5,
                // top: 20,
                //  bottom: 60,
            },
        },
        tooltips: { //2-property 
            enabled: true, //bydefault ye true hota hai jis say tooltips show hota hai
            //enabled:false, //false say tooltips show nhi hota
            backgroundColor: "Red", // tooltips ka color is say rakhty hai
        },
        plugins: { //3 property
            title: {//3-A-part property
                display: true,
                // text: "Cash Flow Chart",
                fontSize: 40,
                position: 'bottom',
                fontStyle: "italic",
                padding: 20,
            },
            legend: { //3-B-part property jo uper chota color ban k ata
                display: true,
                position: 'top',
                align: 'center',
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
//second charts
const ctx2 = document.getElementById('CashFlowChart2').getContext("2d");

const myChart2 = new Chart(ctx2, {
    type: "bar", //ye chart ki type hai
    data: { //ye overall data object hota jo ham pass karty han
        labels: ["January", "February", "March", "April", "May", "June", "July","August","September","October","November","December"], //label jo nichy atya han 
        datasets: [ //ye dataset hai jis ma array or array k under objects bna sakty
            {
                label: "Monthly Report", //ye jo uper lable nazar ata
                data: [1, 2, -3, 8, -5, 6, 7,9,-6,-4,10,7], //ye wo data jo nazat ata chat k uper line ya dots pay
                borderColor: "Black", //border color
                backgroundColor: ["#66FF00", "#66FF00", "#91A3B0", "#66FF00", "#91A3B0", "#66FF00", "#66FF00","#66FF00","#91A3B0","#91A3B0","#66FF00","#66FF00"], //ye colors han
                //ham rgb ma be value day sakty han
                borderWidth: 0, //border ki width hai 
                order: 1,
            },
            {
                label: "Daily Report", //ye jo uper lable nazar ata
                data: [1, 2, -3, 6, -5, 6, 7,9,-4,-6,10,7], //ye wo data jo nazar ata chat k uper line ya dots pay
                // backgroundColor: ["Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "Brown"], //ye colors han
                backgroundColor: "Blue",
                //ham rgb ma be value day sakty han
                borderColor: "Black", //border color
                borderWidth: 1, //border ki width hai 
                type: 'line',
                order: 0,
            }
        ]
    },
    //configuration for graph
    options: {
        responsive: true, // by default ye true hota jis say responsive rahta hai height or width ma farak nahi parta 
        layout: { //1 property layout ma ham different properties day sakty han like padding,margin
            padding: { //
                // left: 30,
                // right: 5,
                // top: 20,
                // bottom: 60,
            },
        },
        tooltips: { //2-property 
            enabled: true, //bydefault ye true hota hai jis say tooltips show hota hai
            //enabled:false, //false say tooltips show nhi hota
            backgroundColor: "Red", // tooltips ka color is say rakhty hai
        },
        plugins: { //3 property
            title: {//3-A-part property
                display: true,
                // text: "Cash Flow Chart",
                fontSize: 40,
                position: 'bottom',
                fontStyle: "italic",
                padding: 20,
            },
            legend: { //3-B-part property jo uper chota color ban k ata
                display: true,
                position: 'top',
                align: 'center',
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