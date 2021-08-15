import Moment from 'moment'
import { extendMoment } from 'moment-range'

const moment = extendMoment(Moment)

export const daysDifference = (dateStr, dateStr2) => {
  const fmt = 'YYYY-MM-DD'
  const start = moment(dateStr, fmt)
  const end = moment(dateStr2, fmt)

  return start.diff(end, 'days')
}

export const formatDate = (dateStr) => {
  const date = moment(dateStr)
  return date.format('ddd, MMM D, YYYY')
}

export const dateInInterval = (date, intervalDate1, intervalDate2) => {
  const interval = moment.range(intervalDate1, intervalDate2)
  const m = moment(date)
  return m.within(interval)
}

export const overlappingIntervals = (start, end, start1, end1) => {
  const inter1 = moment.range(start, end)
  const inter2 = moment.range(start1, end1)
  return inter1.overlaps(inter2, { adjacent: true })
}

export const validDate = (dateStr) => {
  return moment(dateStr).isValid()
}

export const dateStringToday = () => {
  return moment().format('YYYY-MM-DD')
}
