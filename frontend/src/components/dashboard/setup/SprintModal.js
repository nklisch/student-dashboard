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
    const initialData = props.modalData
    if (!initialData) return

    const editing = initialData.editIndex !== -1
    if (editing) {
      setEditIndex(initialData.editIndex)

      const sprintData = initialData.sprintData
      setSprint({ start: sprintData.startDate, end: sprintData.endDate })
    } else {
      setEditIndex(-1)
      setSprint({ start: dateStringToday(), end: dateStringToday() })
    }
  }, [props.modalData, setSprint])

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
              value={sprint.start}
              type="date"
              onChange={(e) => {
                setSprint({ ...sprint, start: e.target.value })
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
              value={sprint.end}
              type="date"
              onChange={(e) => {
                setSprint({ ...sprint, end: e.target.value })
              }}
              invalid={endError.length !== 0}
              required
            />
            <CFormFeedback invalid>{endError}</CFormFeedback>
          </div>
          <h6 className="mt-4 mb-2">
            Days: {getDaysLabel(daysDifference(sprint.end, sprint.start))}
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
            !validDate(sprint.start) ||
            !validDate(sprint.end)
          }
          onClick={() => {
            editMode()
              ? props.sprintActions.edit(editIndex, sprint.start, sprint.end)
              : props.sprintActions.add(sprint.start, sprint.end)
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
  modalData: PropTypes.object,
  semesterCode: PropTypes.string.isRequired,
  sprints: PropTypes.arrayOf(PropTypes.object).isRequired,
  sprintActions: PropTypes.object.isRequired,
}

const useSprintValidation = (editIndex, allSprints) => {
  const [sprint, setSprint] = useState({ start: '', end: '' })
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
    if (dateOverlapsSprint(sprint.start)) {
      startErrorMsg = 'Start date overlaps an existing sprint.'
    } else if (intervalOverlapsSprint(sprint.start, sprint.end)) {
      startErrorMsg = 'This sprint overlaps an existing sprint.'
    }

    let endErrorMsg = ''
    if (dateOverlapsSprint(sprint.end)) {
      endErrorMsg = 'End date overlaps an existing sprint.'
    } else if (daysDifference(sprint.end, sprint.start) < 0) {
      endErrorMsg = 'End date is before start date.'
    }

    setStartError(startErrorMsg)
    setEndError(endErrorMsg)
  }, [sprint.start, sprint.end, editIndex, allSprints])

  return [sprint, setSprint, startError, endError]
}

export default SprintModal
