// Combined Financial Data Scraper for Khaan Bank, State Bank, and XacBank
// npm install prompt-sync axios node-fetch

const axios = require('axios');
const fetch = require('node-fetch');
const fs = require('fs');
const prompt = require('prompt-sync')();

process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';

// Fetch data from Khaan Bank
const fetchKhaanBankData = async (year, season) => {
    const types = [133, 134, 135];
    for (const type of types) {
        const url = `https://www.khanbank.com/api/back/financial-statement?type=${type}&year=${year}&season=${season}`;
        try {
            const response = await axios.get(url);
            fs.writeFileSync(
                `json/khaan_df${type}.json`,
                JSON.stringify(response.data, null, 2)
            );
            console.log(`Khaan Bank data type ${type} saved.`);
        } catch (error) {
            console.error(
                `Error fetching Khaan Bank type ${type}:`,
                error.message
            );
        }
    }
};

// State Bank Fetch
const fetchStateBankData = async (number) => {
    try {
        const apiUrl = `https://www.statebank.mn/back/api/news/${number}`;
        console.log(`Trying State Bank URL: ${apiUrl}`);

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
        fs.writeFileSync('json/state.json', JSON.stringify(data, null, 2));
        console.log('Data fetched successfully and saved to state.json');
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

// Enhanced XacBank Fetch with Complete Headers
const fetchXacBankData = async (year, season) => {
    for (let type = 1; type <= 2; type++) {
        try {
            const url =
                'https://www.xacbank.mn/finance-reports/ajax-get-report';
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    Accept: 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Content-Type':
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
                    Cookie: 'xacbank=5da0aa1741bbdc933249f277a8a12cce; site=personal; csrfToken=0b22e25b8445032cf18cf98bad0fb5b6c71fc8a4132d860256495dfb8a3420a6363892b8efc4ac9a6d01d7de956ae022336840549f667ef94a3a78ce037866a0',
                    Referer:
                        'https://www.xacbank.mn/page/statement-of-financial-position',
                    'Referrer-Policy': 'strict-origin-when-cross-origin',
                },
                body: `year=${year}&season=${season}&type=${type}`,
            });

            if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
            const data = await response.json();
            fs.writeFileSync(
                `json/xac_df${type}.json`,
                JSON.stringify(data, null, 2)
            );
            console.log(`XacBank data type ${type} saved.`);
        } catch (error) {
            console.error(
                `Error fetching XacBank type ${type}:`,
                error.message
            );
        }
    }
};

// Main function to control data fetching
const main = async () => {
    const year = prompt('Enter year: ');
    const season = prompt('Enter season: ');
    const stateNumber = prompt('Enter State Bank URL last numbers: ');

    console.log('Fetching data for Khaan Bank...');
    await fetchKhaanBankData(year, season);

    console.log('Fetching data for State Bank...');
    await fetchStateBankData(stateNumber);

    console.log('Fetching data for XacBank...');
    await fetchXacBankData(year, season);

    console.log('Data fetched and saved for all banks.');
};

main();
