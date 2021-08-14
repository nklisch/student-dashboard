import React from 'react'
import PropTypes from 'prop-types'
import {
  CButton,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
} from '@coreui/react'
import { daysBetween, formatDate } from 'src/util/dates'

const SprintsTable = (props) => {
  return (
    <CTable hover striped>
      <TableHeader />
      <TableBody sprintData={props.sprintData} openSprintModal={props.openSprintModal} />
    </CTable>
  )
}

SprintsTable.propTypes = {
  sprintData: PropTypes.arrayOf(PropTypes.object).isRequired,
  openSprintModal: PropTypes.func.isRequired,
}

const TableHeader = () => {
  const headers = ['#', 'Details', '']
  return (
    <CTableHead>
      <CTableRow>
        {headers.map((header, index) => (
          <CTableHeaderCell key={index + header} scope="col">
            {header}
          </CTableHeaderCell>
        ))}
      </CTableRow>
    </CTableHead>
  )
}

const TableBody = (props) => {
  return (
    <CTableBody>
      {props.sprintData.map((item, index) => (
        <CTableRow key={index + item.startDate}>
          <CTableHeaderCell scope="row">{item.id}</CTableHeaderCell>
          <CTableDataCell>
            <strong>Start:</strong> {formatDate(item.startDate)}
            <br />
            <strong>End:</strong> {formatDate(item.endDate)}
            <br />
            <strong>Days:</strong> {daysBetween(item.startDate, item.endDate)}
          </CTableDataCell>
          <CTableDataCell>
            <CButton
              color="primary"
              variant="outline"
              size="sm"
              onClick={() => {
                props.openSprintModal(item)
              }}
            >
              Edit
            </CButton>
          </CTableDataCell>
        </CTableRow>
      ))}
    </CTableBody>
  )
}

TableBody.propTypes = {
  sprintData: PropTypes.arrayOf(PropTypes.object).isRequired,
  openSprintModal: PropTypes.func.isRequired,
}

export default SprintsTable
