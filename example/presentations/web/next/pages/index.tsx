import Head from 'next/head'
import styles from '../styles/Home.module.css'
import React, { useEffect, useState } from 'react'
import { DefaultApi, UserVTO } from '../openapi'

const api = new DefaultApi({
  basePath: process.env.API,
})

const Home: React.FunctionComponent = function () {
  const urls = {
    next: 'https://nextjs.org',
    docs: 'https://nextjs.org/docs',
    learn: 'https://nextjs.org/learn',
    examples: 'https://github.com/vercel/next.js/tree/master/examples',
    // eslint-disable-next-line prettier/prettier,max-len
    deploy: 'https://vercel.com/import?filter=next.js&utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app',
    vercel: 'https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app',
  }

  const [users, setUsers] = useState<UserVTO[]>([])
  useEffect(() => {
    ;(async () => {
      const results = await api.listUsersUsersGet()
      setUsers(results.data.users)
    })()
  }, [])

  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href={urls.next}>Next.js!</a>
        </h1>

        <p className={styles.description}>
          Get started by editing <code className={styles.code}>pages/index.js</code>
          <br />
          <code className={styles.code}>$API = {process.env.API}</code>
        </p>

        <div className={styles.grid}>
          <a href={urls.docs} className={styles.card}>
            <h3>Documentation &rarr;</h3>
            <p>Find in-depth information about Next.js features and API.</p>
          </a>

          <a href={urls.learn} className={styles.card}>
            <h3>Learn &rarr;</h3>
            <p>Learn about Next.js in an interactive course with quizzes!</p>
          </a>

          <a href={urls.examples} className={styles.card}>
            <h3>Examples &rarr;</h3>
            <p>Discover and deploy boilerplate example Next.js projects.</p>
          </a>

          <a href={urls.deploy} className={styles.card}>
            <h3>Deploy &rarr;</h3>
            <p>Instantly deploy your Next.js site to a public URL with Vercel.</p>
          </a>
          {users.map((user) => (
            <a className={styles.card} key={user.id}>
              <h3>
                {user.name.last} {user.name.first}{user.name.other}
              </h3>
            </a>
          ))}
        </div>
      </main>

      <footer className={styles.footer}>
        <a href={urls.vercel} target="_blank" rel="noopener noreferrer">
          Powered by <img src="/vercel.svg" alt="Vercel Logo" className={styles.logo} />
        </a>
      </footer>
    </div>
  )
}

export default Home
