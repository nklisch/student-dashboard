import React, { Component } from 'react'
import { HashRouter, Route, Switch } from 'react-router-dom'
import './scss/style.scss'
import { useAuthentication } from './util/reusable/hooks'
const loading = (
  <div className="pt-3 text-center">
    <div className="sk-spinner sk-spinner-pulse"></div>
  </div>
)

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/Login'))
const Page404 = React.lazy(() => import('./views/pages/Page404'))
const Page500 = React.lazy(() => import('./views/pages/Page500'))

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
