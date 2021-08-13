import React from 'react'
import PropTypes from 'prop-types'
import { CCallout } from '@coreui/react'

const MetricCallout = ({ label, value }) => {
  return (
    <CCallout color="dark" className="bg-white">
      <small>{label}</small>
      <br />
      <strong className="h5">{value || '-'}</strong>
    </CCallout>
  )
}

MetricCallout.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.number,
}

export default MetricCallout
