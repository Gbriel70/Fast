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
		const response = await fetch('/dns',{
				method: 'POST',
				headers:
				{
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ url:url}),
			}
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const data = await response.json();
		resultDiv.className = data.success ? 'online' : 'offline';
		let html = `
			<p><strong>Domain:</strong> ${data.domain}</p>
			<p><strong>Record Type:</strong> ${data.record_types ? data.record_types.join(', ') : 'None'}</p>
			<p><strong>Resolution Time:</strong>${data.resolution_time} seconds</p>
		`;

		if (data.ip_addresses && data.ip_addresses.length > 0) {
			html += `
				<p><strong>IP Addresses:</strong></p>
				<ul>
			`;
			
			data.ip_addresses.forEach(ip => {
				html += `
					<li>${ip}</li>
				`;
			});
			html += '</ul>';
		} else {
			html += '<p>No Ip addresses found</p>';
		}

		if (data.cname_records && data.cname_records.length > 0){
			html += `
				<p><strong>CNAME Records:</strong></p>
				<ul>
			`;
			
			data.cname_records.forEach(cname => {
				html += `
					<li>${cname}</li>
				`;
			});
			html += '</ul>';
		}else{
			html += '<p><strong>CNAME Records:</strong> None (Apex domains like this typically cannot have CNAME records)</p>';
		}

		resultDiv.innerHTML = html;

	}catch (error){
		resultDiv.className = 'offline';
		resultDiv.innerHTML = '<p>Error resolving DNS</p>';
		console.error('Error:', error);
		alert("Error resolving DNS");
		resultDiv.innerHTML = '<p>Error resolving DNS</p>';
	}
}