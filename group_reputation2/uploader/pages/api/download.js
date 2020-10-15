import fs from 'fs';

import withSession from '../../lib/session';

export const config = {
    api: {
        externalResolver: true,
    },
};

export default withSession(async (req, res) => {   
    const user = req.session.get('user');
    const api_key = req.headers.authorization;

    if (!(user || api_key === 'Basic ' + process.env.API_KEY)) {
        return res.status(401).end();
    }

    fs.readFile('userdata.json', function(err, data) {
        if (err) return res.status(500).send(err.message);
        res.json(JSON.parse(data));
    })
});