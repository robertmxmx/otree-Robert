import { withIronSession } from 'next-iron-session';

export default function withSession(handler) {
    return withIronSession(handler, {
        cookieName: 'UPLOADER_COOKIE',
        cookieOptions: { secure: true },
        password: process.env.UPLOADER_SECRET
    });
}