// npm install prompt-sync node-fetch
const fetch = require('node-fetch');
const fs = require('fs');
const prompt = require('prompt-sync')();

const number = prompt('Last numbers of the URL: ');

// Construct the full API URL
const apiUrl = `https://www.statebank.mn/back/api/news/${number}`;

async function fetchData() {
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                Accept: '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'mn',
                Connection: 'keep-alive',
                'Content-Type': 'application/json',
                Cookie: 'XSRF-TOKEN=your_xsrf_token; statebank_session=your_statebank_session;',
                Host: 'www.statebank.mn',
                Referer: `https://www.statebank.mn/personal/news/${number}`,
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent':
                    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36',
                'sec-ch-ua':
                    '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();
        console.log('Data fetched successfully:', data);

        fs.writeFileSync('json/state.json', JSON.stringify(data, null, 2));
        console.log('Data saved to state.json');
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Run the function
fetchData();
