import React from 'react'
import { CCol, CContainer, CRow } from '@coreui/react'
import PropTypes from 'prop-types'
import MetricCallout from 'src/components/dashboard/MetricCallout'
import SemesterSetup from 'src/components/dashboard/setup/SemesterSetup'
import StudentActivity from './StudentActivity'

const Dashboard = (props) => {
  return (
    <CContainer>
      {/* <h4>Your Progress (Sprint 1)</h4>
      <CRow>
        {labels.map((label, index) => (
          <CCol key={label} sm={3} xs={6}>
            <MetricCallout label={label} value={studentData[index]} />
          </CCol>
        ))}
      </CRow> */}

      <h4 className="mt-4">Class Perspective</h4>

      <StudentActivity user={props.user} />

      <br />
      <br />
      <br />
      <SemesterSetup />
    </CContainer>
  )
}

const toRelativeScale = (data, otherData) => {
  return data.map((value, index) => {
    const otherValue = otherData[index]
    if (value >= otherValue) {
      return 100
    } else {
      return ((value / otherValue) * 100).toFixed(2)
    }
  })
}

Dashboard.propTypes = {
  user: PropTypes.object,
}

export default Dashboard
