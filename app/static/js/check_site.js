async function checkSite() 
{
    const url = document.getElementById('urlInput').value;
    if (!url)
        {
            alert('Please enter a URL');
            return;
        }

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Checking...';
    resultDiv.style.display = 'block';
    resultDiv.className = '';

    try
    {
        const response = await fetch('/ping', 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url}),
            });

            const data = await response.json();

            if (data.status == 'online') 
                {
                    resultDiv.className = 'online';
                    resultDiv.innerHTML = `
                    <p><strong>Staus:</strong> Online</p>
                    <p><strong>Url:</strong> ${data.url}</p>
                    <p><strong>Response Time:</strong> ${data.response_time} ms</p>
                    `;
                } else
                {
                    resultDiv.className = 'offline';
                    resultDiv.innerHTML = `
                    <p><strong>Status:</strong>Offline</p>
                    <p><strong>URL:</strong>${data.url}</p>
                    `;
                }
    } catch (error)
    {
        resultDiv.className = 'offline';
        resultDiv.innerHTML = `
        <p>Error to check site: ${error.message}</p>
        `;
    }
}