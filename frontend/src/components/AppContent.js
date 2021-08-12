import React, { Suspense } from 'react'
import { Redirect, Switch, Route } from 'react-router-dom'
import { CContainer, CSpinner } from '@coreui/react'

// routes config
import routes from '../routes'
import PrivateRoute from './PrivateRoute'
import Login from 'src/views/pages/login/Login'
import { LOGIN_PATH } from 'src/assets/globals'

const AppContent = (props) => {
  return (
    <CContainer lg>
      <Suspense fallback={<CSpinner color="primary" />}>
        <Switch>
          {routes.map((route, idx) => {
            return (
              route.component && (
                <PrivateRoute
                  {...props}
                  key={idx}
                  path={route.path}
                  exact={route.exact}
                  name={route.name}
                  render={() => <route.component {...props} />}
                />
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
