async function scanPorts() 
{
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert("Please enter a URL.");
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Scanning ports... this may take a minutes...';
    resultDiv.style.display = 'block';
    resultDiv.className = 'scanning';

    try
    {
        const response = await fetch('/nmap',
            {
                method: 'POST',
                headers: 
                {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url:url}),
            });

            const data = await response.json();

            resultDiv.className = 'online';
            let html = `
                <p><strong>Host:</strong> ${data.host}</p>
                <p><strong>Ports Scanned:</strong> ${data.ports_scanned}</p>
                <p><strong>Scan Time:</strong> ${data.scan_time} seconds</p>
            `;

            if (data.open_ports && data.open_ports.length > 0) {
                html += `
                    <table>
                        <tr>
                            <th>Port</th>
                            <th>Service</th>
                        </tr>
                `;
                
                data.open_ports.forEach(port => {
                    html += `
                        <tr>
                            <td>${port.port}</td>
                            <td>${port.service}</td>
                        </tr>
                    `;
                });
                
                html += '</table>';
            } else {
                html += '<p>No open ports found</p>';
            }

            resultDiv.innerHTML = html;
    }catch (error)
    {
        console.error("Error:", error);
        resultDiv.className = 'offline';
        resultDiv.innerHTML = `
            <p>Error scanning ports: ${error.message}</p>
        `
    }
}