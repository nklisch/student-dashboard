import Moment from 'moment'
import { extendMoment } from 'moment-range'

const moment = extendMoment(Moment)

export const daysBetween = (dateStr, dateStr2) => {
  const fmt = 'YYYY-MM-DD'
  const start = moment(dateStr, fmt)
  const end = moment(dateStr2, fmt)

  return end.diff(start, 'days')
}

export const formatDate = (dateStr) => {
  const date = moment(dateStr)
  return date.format('ddd, MMM Do, YYYY')
}

export const dateDifference = (date, date2) => {
  const m1 = moment(date)
  const m2 = moment(date2)
  return m1.diff(m2)
}

export const dateLessThan = (date, date2) => {
  return dateDifference(date, date2) < 0
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
