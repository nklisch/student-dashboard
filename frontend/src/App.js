import React from 'react'
import { HashRouter, Route } from 'react-router-dom'
import './scss/style.scss'
import { useAuthentication } from './util/hooks'
const loading = (
  <div className="pt-3 text-center">
    <div className="sk-spinner sk-spinner-pulse"></div>
  </div>
)

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

function App() {
  const [isAuthenticated, user, login, logout] = useAuthentication()
  return (
    <HashRouter>
      <React.Suspense fallback={loading}>
        <Route
          path="/"
          name="Home"
          render={() => (
            <DefaultLayout
              isAuthenticated={isAuthenticated}
              user={user}
              login={login}
              logout={logout}
            />
          )}
        />
      </React.Suspense>
    </HashRouter>
  )
}

export default App
