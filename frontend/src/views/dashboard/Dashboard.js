import React from 'react'
import { CContainer } from '@coreui/react'
import PropTypes from 'prop-types'
import SemesterSetup from 'src/components/dashboard/setup/SemesterSetup'
import StudentActivity from './StudentActivity'

const Dashboard = (props) => {
  return (
    <CContainer>
      <h4 className="mt-4">Class Perspective</h4>
      <StudentActivity user={props.user} />

      <br />
      <br />
      <br />
      <SemesterSetup />
    </CContainer>
  )
}

Dashboard.propTypes = {
  user: PropTypes.object,
}

export default Dashboard
