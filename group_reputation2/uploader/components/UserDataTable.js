import axios from 'axios';
import { useEffect, useState } from 'react';

import styles from '../styles/Home.module.css';

export default function UserDataTable() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setData(null);
        setLoading(true);
        setError(null);

        axios.get('/api/download')
            .then(res => {
                setData(res.data);
                setLoading(false);
                setError(null);
            })
            .catch(err => {
                setData(null);
                setLoading(false);
                setError(err.response.data);
            });
    }, []);

    if (error) {
        return (
            <p className={styles.error}>{error}</p> 
        );
    }

    if (loading || !data) {
        return (
            <p>Loading...</p>
        );
    }

    return (
        <table className={styles.table}>
            <tr>
                { data.headers.map((elem, index) => (
                    <th key={index}>{elem}</th>
                )) }
            </tr>
            { data.rows.map((row, index) => (
                <tr key={index}>
                    { Object.keys(row).map((key, index2) => (
                        <td key={index2}>{row[key]}</td>
                    ))}
                </tr>
            )) }
        </table>
    );
}