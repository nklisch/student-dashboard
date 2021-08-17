import React from 'react'
import PropTypes from 'prop-types'
import SemesterSetup from 'src/components/dashboard/setup/SemesterSetup'

const InstructorDashboard = ({ user }) => {
  return <SemesterSetup />
}

InstructorDashboard.propTypes = {
  user: PropTypes.object,
}

export default InstructorDashboard
