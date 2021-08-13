import React, { Suspense } from 'react'
import { Redirect, Switch, Route } from 'react-router-dom'
import { CContainer, CSpinner } from '@coreui/react'

// routes config
import routes from '../routes'
import ProtectedRoute from './routing/ProtectedRoute'
import Login from 'src/views/pages/Login'
import { LOGIN_PATH } from '../globals'

const AppContent = (props) => {
  return (
    <CContainer lg>
      <Suspense fallback={<CSpinner color="primary" />}>
        <Switch>
          {routes.map((route, idx) => {
            return (
              route.component && (
                <ProtectedRoute
                  {...props}
                  key={idx}
                  path={route.path}
                  exact={route.exact}
                  name={route.name}
                  required_role={route.required_role}
                >
                  {' '}
                  <route.component {...props} />
                </ProtectedRoute>
              )
            )
          })}
          <Route
            {...props}
            path={LOGIN_PATH}
            exact
            name={'Login'}
            render={() => <Login {...props} />}
          />
          <Redirect from="/" to="/dashboard" />
        </Switch>
      </Suspense>
    </CContainer>
  )
}

export default React.memo(AppContent)
