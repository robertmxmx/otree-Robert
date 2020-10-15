import { useState } from 'react';
import axios from 'axios';
import Router from 'next/router';

import styles from '../styles/Home.module.css';

export default function FileUploader() {
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
      axios.post('/api/upload', data)
        .then(res => {
          Router.reload(window.location.pathname);
        })
        .catch(err => {
          setError(err.response.data);
        });
    };
  
    return (
        <div className={styles.form}>
            <form action="#">
                <input type="file" onChange={handleFileChange} />
            </form>
            { error && <p className={styles.error}>{error}</p> }
            <button 
                onClick={handleSubmit} 
                disabled={file === null || file === undefined}
            >
                Upload
            </button>
        </div>
    )
}