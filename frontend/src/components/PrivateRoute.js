import { Route } from 'react-router'
import { Redirect } from 'react-router-dom'
import { LOGIN_PATH } from 'src/assets/globals'
import { authorization } from 'src/assets/util/requests'
export default function PrivateRoute({ children, ...props }) {
  return (
    <Route
      {...props}
      render={({ location }) =>
        authorization.isAuthenticated() ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: LOGIN_PATH,
              state: { from: location ? location : '/' },
            }}
          />
        )
      }
    />
  )
}
