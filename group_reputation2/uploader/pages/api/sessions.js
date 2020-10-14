import { withIronSession } from "next-iron-session";

const VALID_USERNAME = 'admin';
const VALID_PASSWORD = 'uploaderr';

export default withIronSession(
    async (req, res) => {
        if (req.method === "POST") {
            const { username, password } = req.body;

            if (username == VALID_USERNAME && password == VALID_PASSWORD) {
                req.session.set('user', { username });
                await req.session.save();
                return res.status(201).send('');
            }

            return res.status(403).send('');
        }

        return res.status(404).send('');
    },
    {
        cookieName: 'UPLOADER_COOKIE',
        cookieOptions: { secure: true },
        password: process.env.UPLOADER_SECRET
    }
);