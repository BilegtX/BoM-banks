const axios = require('axios');
const fs = require('fs');
const prompt = require('prompt-sync')();

process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';

const fetchData = async (type, year, season) => {
    const url = `https://www.khanbank.com/api/back/financial-statement?type=${type}&year=${year}&season=${season}`;
    const response = await axios.get(url);
    return response.data;
};

const getData = async () => {
    const types = [133, 134, 135];
    const year = prompt('Enter year: ');
    const season = prompt('Enter season: ');
    for (const type of types) {
        const data = await fetchData(type, year, season);
        fs.writeFileSync(`khaan_df${type}.json`, JSON.stringify(data, null, 2));
    }
    console.log('Data saved to files.');
};

getData();
