import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import {
  CButton,
  CForm,
  CFormControl,
  CFormFeedback,
  CFormLabel,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
} from '@coreui/react'
import {
  dateInInterval,
  dateStringToday,
  daysDifference,
  overlappingIntervals,
  validDate,
} from 'src/util/dates'

const SprintModal = (props) => {
  const [editIndex, setEditIndex] = useState(-1)
  const [sprint, setSprint, startError, endError] = useSprintValidation(editIndex, props.sprints)

  useEffect(() => {
    const newEditIndex = props.editIndex
    const editing = newEditIndex !== -1
    if (editing) {
      setEditIndex(newEditIndex)
      setSprint(props.sprints[newEditIndex])
    } else {
      setEditIndex(-1)
      setSprint({ startDate: dateStringToday(), endDate: dateStringToday() })
    }
  }, [props.editIndex, props.sprints, setSprint])

  const editMode = () => editIndex !== -1

  const getDaysLabel = (days) => {
    return !Number.isNaN(days) ? days : '-'
  }

  return (
    <CModal visible={props.modalOpen} onDismiss={() => props.setModalOpen(false)}>
      <CModalHeader onDismiss={() => props.setModalOpen(false)}>
        <CModalTitle>{editMode() ? 'Edit' : 'Add'} Sprint</CModalTitle>
      </CModalHeader>

      <CModalBody>
        <CForm>
          <div className="mb-3">
            <CFormLabel htmlFor="startInput">Start Date</CFormLabel>
            <CFormControl
              id="startInput"
              value={sprint.startDate}
              type="date"
              onChange={(e) => {
                setSprint({ ...sprint, startDate: e.target.value })
              }}
              invalid={startError.length !== 0}
              required
            />
            <CFormFeedback invalid>{startError}</CFormFeedback>
          </div>
          <div className="mb-3">
            <CFormLabel htmlFor="endInput">End Date</CFormLabel>
            <CFormControl
              id="endInput"
              value={sprint.endDate}
              type="date"
              onChange={(e) => {
                setSprint({ ...sprint, endDate: e.target.value })
              }}
              invalid={endError.length !== 0}
              required
            />
            <CFormFeedback invalid>{endError}</CFormFeedback>
          </div>
          <h6 className="mt-4 mb-2">
            Days: {getDaysLabel(daysDifference(sprint.endDate, sprint.startDate))}
          </h6>
          <h6 className="mb-4">Semester: {props.semesterCode}</h6>
          {editMode() && (
            <CButton
              color="danger"
              variant="outline"
              onClick={() => {
                if (window.confirm('Delete Sprint ' + (editIndex + 1) + '?')) {
                  props.sprintActions.remove(editIndex)
                  props.setModalOpen(false)
                }
              }}
            >
              Delete
            </CButton>
          )}
        </CForm>
      </CModalBody>

      <CModalFooter>
        <CButton color="secondary" onClick={() => props.setModalOpen(false)}>
          Close
        </CButton>
        <CButton
          color="primary"
          disabled={
            startError.length !== 0 ||
            endError.length !== 0 ||
            !validDate(sprint.startDate) ||
            !validDate(sprint.endDate)
          }
          onClick={() => {
            const { startDate, endDate } = sprint
            editMode()
              ? props.sprintActions.edit(editIndex, startDate, endDate)
              : props.sprintActions.add(startDate, endDate)
            props.setModalOpen(false)
          }}
        >
          Save
        </CButton>
      </CModalFooter>
    </CModal>
  )
}

SprintModal.propTypes = {
  modalOpen: PropTypes.bool.isRequired,
  setModalOpen: PropTypes.func.isRequired,
  editIndex: PropTypes.number.isRequired,
  semesterCode: PropTypes.string.isRequired,
  sprints: PropTypes.arrayOf(PropTypes.object).isRequired,
  sprintActions: PropTypes.object.isRequired,
}

const useSprintValidation = (editIndex, allSprints) => {
  const [sprint, setSprint] = useState({ startDate: '', endDate: '' })
  const [startError, setStartError] = useState('')
  const [endError, setEndError] = useState('')

  useEffect(() => {
    const anyOtherSprint = (predicate) => {
      return allSprints.some((other, index) => index !== editIndex && predicate(other))
    }

    const dateOverlapsSprint = (date) => {
      return anyOtherSprint((other) => dateInInterval(date, other.startDate, other.endDate))
    }

    const intervalOverlapsSprint = (date1, date2) => {
      return anyOtherSprint((other) =>
        overlappingIntervals(date1, date2, other.startDate, other.endDate),
      )
    }

    let startErrorMsg = ''
    if (dateOverlapsSprint(sprint.startDate)) {
      startErrorMsg = 'Start date overlaps an existing sprint.'
    } else if (intervalOverlapsSprint(sprint.startDate, sprint.endDate)) {
      startErrorMsg = 'This sprint overlaps an existing sprint.'
    }

    let endErrorMsg = ''
    if (dateOverlapsSprint(sprint.endDate)) {
      endErrorMsg = 'End date overlaps an existing sprint.'
    } else if (daysDifference(sprint.endDate, sprint.startDate) < 0) {
      endErrorMsg = 'End date is before start date.'
    }

    setStartError(startErrorMsg)
    setEndError(endErrorMsg)
  }, [sprint.startDate, sprint.endDate, editIndex, allSprints])

  return [sprint, setSprint, startError, endError]
}

export default SprintModal
