import withSession from '../../lib/session';

const VALID_USERNAME = 'admin';
const VALID_PASSWORD = 'uploaderr';

export default withSession(async (req, res) => {
    if (req.method === "POST") {
        const { username, password } = req.body;

        if (username == VALID_USERNAME && password == VALID_PASSWORD) {
            req.session.set('user', { username });
            await req.session.save();
            return res.status(201).end();
        }

        return res.status(403).end();
    }

    return res.status(404).end();
});