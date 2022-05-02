
function getCharts(charts) {
    // Analytics page
    // Generate the charts on demand
    const generateChart = "chart-gen";
    const webAppURL = window.location.href + "/generate-charts";
    const baseImgSrc = "static/images/";
    const baseExt = ".png";

    fetch(webAppURL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(charts)
        })
        .then( (c) => {
            for(let i = 0; i < charts.length; i++){
                document.getElementById("chart" + i).src = baseImgSrc + charts[i] + baseExt;
            }
            })
        .catch( (e) =>{
            console.error(e);
        }
    )
}