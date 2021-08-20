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
      setSprint({ start_date: dateStringToday(), end_date: dateStringToday() })
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
              value={sprint.start_date}
              type="date"
              onChange={(e) => {
                setSprint({ ...sprint, start_date: e.target.value })
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
              value={sprint.end_date}
              type="date"
              onChange={(e) => {
                setSprint({ ...sprint, end_date: e.target.value })
              }}
              invalid={endError.length !== 0}
              required
            />
            <CFormFeedback invalid>{endError}</CFormFeedback>
          </div>
          <h6 className="mt-4 mb-2">
            Days: {getDaysLabel(daysDifference(sprint.end_date, sprint.start_date))}
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
            !validDate(sprint.start_date) ||
            !validDate(sprint.end_date)
          }
          onClick={() => {
            const { start_date, end_date } = sprint
            editMode()
              ? props.sprintActions.edit(editIndex, start_date, end_date)
              : props.sprintActions.add(start_date, end_date)
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
  const [sprint, setSprint] = useState({ start_date: '', end_date: '' })
  const [startError, setStartError] = useState('')
  const [endError, setEndError] = useState('')

  useEffect(() => {
    const anyOtherSprint = (predicate) => {
      return allSprints.some((other, index) => index !== editIndex && predicate(other))
    }

    const dateOverlapsSprint = (date) => {
      return anyOtherSprint((other) => dateInInterval(date, other.start_date, other.end_date))
    }

    const intervalOverlapsSprint = (date1, date2) => {
      return anyOtherSprint((other) =>
        overlappingIntervals(date1, date2, other.start_date, other.end_date),
      )
    }

    let startErrorMsg = ''
    if (dateOverlapsSprint(sprint.start_date)) {
      startErrorMsg = 'Start date overlaps an existing sprint.'
    } else if (intervalOverlapsSprint(sprint.start_date, sprint.end_date)) {
      startErrorMsg = 'This sprint overlaps an existing sprint.'
    }

    let endErrorMsg = ''
    if (dateOverlapsSprint(sprint.end_date)) {
      endErrorMsg = 'End date overlaps an existing sprint.'
    } else if (daysDifference(sprint.end_date, sprint.start_date) < 0) {
      endErrorMsg = 'End date is before start date.'
    }

    setStartError(startErrorMsg)
    setEndError(endErrorMsg)
  }, [sprint.start_date, sprint.end_date, editIndex, allSprints])

  return [sprint, setSprint, startError, endError]
}

export default SprintModal
