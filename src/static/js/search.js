
function loadWait(){

    const locationElement = document.getElementById('location')
    const qElement = document.getElementById('q')
    const location = locationElement.value
    const q = qElement.value

    fetch(
        '/loading',
        {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            location: location,
            q: q
        }
    }).then(function(data){
        Plotly.newPlot('netGraph', data);
    });

}