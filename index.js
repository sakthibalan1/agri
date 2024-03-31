function fetchData() {
    const sensor = document.getElementById('sensor').value;
    const numberOfData = document.getElementById('numberOfData').value;

    axios.get(`/${sensor}?n=${numberOfData}`)
        .then(response => {
            const data = response.data;
            const sensorDataElement = document.getElementById('sensorData');
            sensorDataElement.innerHTML = '';
            data.forEach(value => {
                const p = document.createElement('p');
                p.textContent = `${sensor.charAt(0).toUpperCase() + sensor.slice(1)}: ${value}`;
                sensorDataElement.appendChild(p);
            });
        })
        .catch(error => console.error(`Error fetching ${sensor} data:`, error));
}
