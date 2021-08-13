import React from 'react'
import { Route } from 'react-router'
import { Redirect } from 'react-router-dom'
import { LOGIN_PATH, ACCESS_DENIED, verify_role } from '../../globals'
import PropTypes from 'prop-types'
export default function ProtectedRoute({
  children,
  render,
  required_role,
  user,
  isAuthenticated,
  ...props
}) {
  return (
    <Route
      {...props}
      render={() => {
        if (!isAuthenticated) {
          return <Redirect to={LOGIN_PATH} />
        }
        if (verify_role(required_role, user.role)) {
          return children
        }

        return <Redirect to={ACCESS_DENIED} />
      }}
    />
  )
}

ProtectedRoute.propTypes = {
  children: PropTypes.any,
  isAuthenticated: PropTypes.bool.isRequired,
  render: PropTypes.func,
  user: PropTypes.object,
  required_role: PropTypes.string,
}
