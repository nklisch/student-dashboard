import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { CTable, CTableHead, CTableHeaderCell } from '@coreui/react'
import { get } from 'src/util/requests'
const ClassHistory = () => {
  const [semesters, setSemesters] = useState([])

  useEffect(() => {
    get({ api: 'Semesters' }).then((result) => {
      setSemesters(result)
    })
  }, [])

  return (
    <CTable>
      <CTableHead>
        {semesters &&
          semesters.length > 0 &&
          Object.keys(semesters[0]).map((key, idx) => (
            <CTableHeaderCell key={idx}>{key}</CTableHeaderCell>
          ))}
      </CTableHead>
    </CTable>
  )
}

export default ClassHistory
