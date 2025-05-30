// npm install prompt-sync
const axios = require('axios');
const fetch = require('node-fetch');
const cheerio = require('cheerio'); // Add this line
const fs = require('fs');
const prompt = require('prompt-sync')();

process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';

const fetchData = async (year, season, type) => {
    try {
        const res = await fetch(
            'https://www.xacbank.mn/finance-reports/ajax-get-report',
            {
                headers: {
                    accept: 'application/json, text/javascript, */*; q=0.01',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type':
                        'application/x-www-form-urlencoded; charset=UTF-8',
                    'sec-ch-ua':
                        '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-csrf-token':
                        '0b22e25b8445032cf18cf98bad0fb5b6c71fc8a4132d860256495dfb8a3420a6363892b8efc4ac9a6d01d7de956ae022336840549f667ef94a3a78ce037866a0',
                    'x-requested-with': 'XMLHttpRequest',
                    cookie: 'xacbank=5da0aa1741bbdc933249f277a8a12cce; site=personal; csrfToken=0b22e25b8445032cf18cf98bad0fb5b6c71fc8a4132d860256495dfb8a3420a6363892b8efc4ac9a6d01d7de956ae022336840549f667ef94a3a78ce037866a0; TS01e598a2=01d3b635cf7c0f93512e2150617a70bd8fae1abcb5279b441c879bf974dc8a4ca5edf52e7aa82b5036fe903f0eefaf50745cc2ffcb7c6fdf0bd9efef9352907d605de339b5aa7213cab1688105acdc55801837fa422787b07655cba9035bd975348c154b21; _gid=GA1.2.2075194848.1719385718; _ga_5CBGM7BDL4=GS1.1.1719385717.1.1.1719385727.0.0.0; _ga=GA1.1.2021602461.1719385718',
                    Referer:
                        'https://www.xacbank.mn/page/statement-of-financial-position',
                    'Referrer-Policy': 'strict-origin-when-cross-origin',
                },
                body: `year=${year}&season=${season}&type=${type}`,
                method: 'POST',
            }
        );
        const data = await res.json();
        return data; // Return the JSON data
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error; // Throw the error for handling elsewhere if needed
    }
};
const saveDataToJsonFile = async () => {
    try {
        const year = prompt('Enter year: ');
        const season = prompt('Enter season: ');

        const bodyData1 = new URLSearchParams({
            year: year,
            season: season,
        }).toString();

        const rawData_df1 = await fetchData(year, season, 1); // Fetch data
        const rawData_df2 = await fetchData(year, season, 2); // Fetch data

        const df1 = JSON.stringify(rawData_df1, null, 2); // Convert data to JSON format with pretty printing
        const df2 = JSON.stringify(rawData_df2, null, 2); // Convert data to JSON format with pretty printing

        const fs = require('fs');
        fs.writeFileSync('xac_df1.json', df1); // Write JSON data to named file
        fs.writeFileSync('xac_df2.json', df2);
        console.log('Data saved');
    } catch (error) {
        console.error('Error saving data to file:', error);
    }
};

// Call saveDataToJsonFile to initiate fetching and saving process
saveDataToJsonFile();
