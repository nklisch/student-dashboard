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
      <TableHeader sprintActions={props.sprintActions} />
      <TableBody sprints={props.sprints} openSprintModal={props.openSprintModal} />
    </CTable>
  )
}

SprintsTable.propTypes = {
  sprints: PropTypes.arrayOf(PropTypes.object).isRequired,
  sprintActions: PropTypes.object.isRequired,
  openSprintModal: PropTypes.func.isRequired,
}

const TableHeader = (props) => {
  return (
    <CTableHead>
      <CTableRow>
        <CTableHeaderCell scope="col">#</CTableHeaderCell>
        <CTableHeaderCell scope="col">Details</CTableHeaderCell>
        <CTableHeaderCell scope="col">
          <CButton
            color="danger"
            variant="outline"
            size="sm"
            onClick={props.sprintActions.deleteAll}
          >
            Clear
          </CButton>
        </CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  )
}

TableHeader.propTypes = {
  sprintActions: PropTypes.object.isRequired,
}

const TableBody = (props) => {
  return (
    <CTableBody>
      {props.sprints.map((sprint, index) => (
        <CTableRow key={index + sprint.startDate}>
          <CTableHeaderCell scope="row">{sprint.id}</CTableHeaderCell>
          <CTableDataCell>
            <strong>Start:</strong> {formatDate(sprint.startDate)}
            <br />
            <strong>End:</strong> {formatDate(sprint.endDate)}
            <br />
            <strong>Days:</strong> {daysDifference(sprint.endDate, sprint.startDate)}
          </CTableDataCell>
          <CTableDataCell>
            <CButton
              color="primary"
              variant="outline"
              size="sm"
              onClick={() => {
                props.openSprintModal(sprint)
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
