import Head from 'next/head';
import { useState } from 'react';
import axios from 'axios';
import Router from 'next/router';

import styles from '../styles/Home.module.css';
import UserDataTable from '../components/UserDataTable';

export default function Home() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = e => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = () => {
    if (!file) {
      setError('Please select a file');
      return;
    }
    
    const data = new FormData();
    data.append('file', file);
    axios.post('http://localhost:3000/api/upload', data)
      .then(res => {
        Router.reload(window.location.pathname);
      })
      .catch(err => {
        setError(err.response.data);
      });
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>User data uploader</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Uploader
        </h1>

        <div className={styles.form}>
          <form action="#">
            <input type="file" onChange={handleFileChange} />
          </form>
          { error && <p>{error}</p> }
          <button onClick={handleSubmit} disabled={file === null || file === undefined}>
            Upload
          </button>
        </div>

        <UserDataTable />
      </main>
    </div>
  )
}
