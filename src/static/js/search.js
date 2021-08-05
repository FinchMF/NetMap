
function loadWait(){

    const loader = document.getElementsByClassName('loader')[0]
    const locationElement = document.getElementById('location')
    const qElement = document.getElementById('q')
    const location = locationElement.value
    const q = qElement.value

    loader.style.display = 'block'

    fetch(
        '/loading',
        {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify( {
            location: location,
            q: q
        })
    }).then( async function(data){
        const G = await data.json()
        loader.style.display = 'none'
        Plotly.newPlot('netGraph', G);
    })
}