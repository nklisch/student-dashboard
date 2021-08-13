import React from 'react'
import { AppContent, AppSidebar, AppFooter, AppHeader } from '../components/index'

const DefaultLayout = (props) => {
  return (
    <div>
      <AppSidebar {...props} />
      <div className="wrapper d-flex flex-column min-vh-100 bg-light">
        <AppHeader {...props} />
        <div className="body flex-grow-1 px-3">
          <AppContent {...props} />
        </div>
        <AppFooter {...props} />
      </div>
    </div>
  )
}

export default DefaultLayout
