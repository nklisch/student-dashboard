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
import { daysDifference, formatDate } from 'src/util/dates'

const SprintsTable = (props) => {
  return (
    <CTable hover striped>
      <TableHeader deleteSprints={props.deleteSprints} />
      <TableBody sprints={props.sprints} openSprintModal={props.openSprintModal} />
    </CTable>
  )
}

SprintsTable.propTypes = {
  sprints: PropTypes.arrayOf(PropTypes.object).isRequired,
  deleteSprints: PropTypes.func.isRequired,
  openSprintModal: PropTypes.func.isRequired,
}

const TableHeader = (props) => {
  return (
    <CTableHead>
      <CTableRow>
        <CTableHeaderCell scope="col">#</CTableHeaderCell>
        <CTableHeaderCell scope="col">Details</CTableHeaderCell>
        <CTableHeaderCell scope="col">
          <CButton color="danger" variant="outline" size="sm" onClick={props.deleteSprints}>
            Clear
          </CButton>
        </CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  )
}

TableHeader.propTypes = {
  deleteSprints: PropTypes.func.isRequired,
}

const TableBody = (props) => {
  return (
    <CTableBody>
      {props.sprints.map((item, index) => (
        <CTableRow key={index + item.startDate}>
          <CTableHeaderCell scope="row">{item.id}</CTableHeaderCell>
          <CTableDataCell>
            <strong>Start:</strong> {formatDate(item.startDate)}
            <br />
            <strong>End:</strong> {formatDate(item.endDate)}
            <br />
            <strong>Days:</strong> {daysDifference(item.endDate, item.startDate)}
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
  sprints: PropTypes.arrayOf(PropTypes.object).isRequired,
  openSprintModal: PropTypes.func.isRequired,
}

export default SprintsTable
