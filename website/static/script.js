
function getCharts(charts, uid) {
    // Analytics page
    // Generate the charts on demand
    const generateChart = "chart-gen";
    const webAppURL = window.location.href + "/generate-charts";
    const baseImgSrc = "static/images/analytics/";
    const baseExt = ".png";
    data = {
        "charts": charts,
        "userID": uid
    }
    fetch(webAppURL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
        })
        .then( (c) => {
            for(let i = 0; i < charts.length; i++){
                document.getElementById("chart" + charts[i]).src = baseImgSrc + charts[i] + baseExt;
            }
            })
        .catch( (e) =>{
            console.error(e);
        }
    )
}