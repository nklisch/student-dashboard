import React from 'react'
import { Route } from 'react-router'
import { Redirect } from 'react-router-dom'
import { LOGIN_PATH } from 'src/assets/globals'
import PropTypes from 'prop-types'
export default function PrivateRoute({ children, render, ...props }) {
  return (
    <Route
      {...props}
      render={() => {
        if (props.isAuthenticated) {
          return render()
        }
        return <Redirect to={LOGIN_PATH} />
      }}
    />
  )
}

PrivateRoute.propTypes = {
  children: PropTypes.any,
  isAuthenticated: PropTypes.bool,
  render: PropTypes.func,
}
