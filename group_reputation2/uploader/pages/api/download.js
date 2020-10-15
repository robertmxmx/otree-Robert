import fs from 'fs';
import * as csv from 'fast-csv';

import withSession from '../../lib/session';

export const config = {
    api: {
        externalResolver: true,
    },
};

export default withSession(async (req, res) => {
    const user = req.session.get('user');

    if (!user) return res.status(401).end();

    const readStream = fs.createReadStream('userdata.csv');

    readStream.on('error', function(err) {
        res.status(500).send('Error opening file. File may not exist');
    });

    readStream.on('open', function() {
        var userdata = [];
        readStream.pipe(csv.parse({ headers: true }))
            .on('error', err => res.status(500).send(err.message + '. This is could be due to invalid file contents'))
            .on('data', data => userdata.push(data))
            .on('end', () => {
                res.json({
                    headers: userdata[0] ? Object.keys(userdata[0]) : [],
                    rows: userdata
                });
            });
    });
});