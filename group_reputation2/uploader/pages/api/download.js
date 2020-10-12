import fs from 'fs';
import * as csv from 'fast-csv';

export const config = {
    api: {
        externalResolver: true,
    },
};

export default async (req, res) => {
    const readStream = fs.createReadStream('userdata.csv');

    readStream.on('error', function(err) {
        res.status(500).send(err.message);
    });

    readStream.on('open', function() {
        var userdata = [];
        readStream.pipe(csv.parse({ headers: true }))
            .on('error', err => res.status(500).send(err.message))
            .on('data', data => userdata.push(data))
            .on('end', () => {
                res.json({
                    headers: userdata[0] ? Object.keys(userdata[0]) : [],
                    rows: userdata
                });
            });
    });
}
  