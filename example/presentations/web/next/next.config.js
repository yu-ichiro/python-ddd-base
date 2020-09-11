require('dotenv').config()

function configBuilder(_phase, _ctx) {
  const defaultEnv = {
    API: 'http://localhost:5000',
    HOME: '',
  }
  const env = Object.fromEntries(
    Object.entries(defaultEnv).map(([key, val]) =>
      Object.hasOwnProperty.call(process.env, key) ? [key, process.env[key]] : [key, val]
    )
  )

  return {
    env,
    poweredByHeader: false,
  }
}

module.exports = configBuilder
