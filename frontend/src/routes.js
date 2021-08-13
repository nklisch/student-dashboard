import React from 'react'

const AccessDenied = React.lazy(() => {
  './views/pages/AccessDenied'
})

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

const routes = [
  { path: '/', exact: true, name: 'Home' },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    exact: true,
    required_role: 'Student',
  },
  { path: '/login', name: 'Login' },
  { path: '/access_denied', name: 'Access Denied', component: AccessDenied },
]

export default routes
