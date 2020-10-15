import Head from 'next/head';

import withSession from '../lib/session';
import styles from '../styles/Home.module.css';
import UserDataTable from '../components/UserDataTable';
import FileUploader from '../components/FileUploader';
import LoginForm from '../components/LoginForm';

export const getServerSideProps = withSession(async ({ req, res }) => {
  const user = req.session.get('user');

  if (!user) return { props: {} };

  return { props: { user }};
});

export default function Home({ user }) {
  if (!user) {
    return (
      <div className={styles.container}>
        <main className={styles.main}>
          <LoginForm />
        </main>
      </div>
    )
  }

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
        <FileUploader />
        <UserDataTable />
      </main>
    </div>
  )
}
