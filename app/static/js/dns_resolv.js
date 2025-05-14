async function dns_resolv() 
{
	const url = document.getElementById('urlInput').value;
	if (!url)
		{
			alert("Please enter a URL.");
			return;
		}
	
	const resultDiv = document.getElementById('result');
	resultDiv.innerHTML = 'Resolving DNS... this may take a minutes...';
	resultDiv.style.display = 'block';
	resultDiv.className = 'scanning';

	try{
		const response = await fetch('/dns_resolv',{
				method: 'POST',
				headers:
				{
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ url:url}),
			}
		);

		const data = await response.json();
		resultDiv.className = 'online';
		let html = `
			<p><strong>Host:</strong> ${data.host}</p>
			<p><strong>IP Address:</strong> ${data.ip_address}</p>
			<p><strong>DNS Server:</strong> ${data.dns_server}</p>
			<p><strong>DNS Resolution Time:</strong> ${data.resolution_time} seconds</p>
		`;
		
		if (data.dns_records && data.dns_records.length > 0) {
			html += `
				<table>
					<tr>
						<th>Record Type</th>
						<th>Record Value</th>
					</tr>
			`;
			
			data.dns_records.forEach(record => {
				html += `
					<tr>
						<td>${record.type}</td>
						<td>${record.value}</td>
					</tr>
				`;
			});
			
			html += '</table>';
		} else {
			html += '<p>No DNS records found</p>';
		}
		resultDiv.innerHTML = html;

	}catch{
		resultDiv.className = 'offline';
		resultDiv.innerHTML = '<p>Error resolving DNS</p>';
		console.error('Error:', error);
		alert("Error resolving DNS");
		resultDiv.innerHTML = '<p>Error resolving DNS</p>';
	}
}