import { useRef, useState} from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

import styles from '../styles/Home.module.css';

export default function LoginForm() {
    const router = useRouter();

    const usernameInput = useRef();
    const passwordInput = useRef();

    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const username = usernameInput.current.value;
        const password = passwordInput.current.value;

        axios.post('/api/sessions', { username, password })
            .then(() => router.push('/'))
            .catch(err => setError(err.message));
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>
                    Username: <input type="text" ref={usernameInput} />
                </label>
            </div>
            <div>
                <label>
                    Password: <input type="password" ref={passwordInput} />
                </label>
            </div>
            <div>
                <button type="submit">Log in</button>
            </div>
            { error && 
                <p className={styles.error}>{error}</p> 
            }
        </form>
    )
}