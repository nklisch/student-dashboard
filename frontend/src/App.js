import React, { Component } from 'react'
import { HashRouter, Route, Switch } from 'react-router-dom'
import './scss/style.scss'
import { useAuthentication } from './reusable/hooks'
const loading = (
  <div className="pt-3 text-center">
    <div className="sk-spinner sk-spinner-pulse"></div>
  </div>
)

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'))
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))

function App() {
  const [isAuthenticated, user, updateAuthentication] = useAuthentication()
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
              updateAuthentication={updateAuthentication}
            />
          )}
        />
      </React.Suspense>
    </HashRouter>
  )
}

export default App
