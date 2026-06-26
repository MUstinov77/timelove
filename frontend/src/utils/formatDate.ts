import { format, parseISO } from 'date-fns'
import { ru } from 'date-fns/locale'

export function formatEventDate(dateStr: string): string {
  return format(parseISO(dateStr), 'd MMMM yyyy', { locale: ru })
}

export function formatEventDateShort(dateStr: string): string {
  return format(parseISO(dateStr), 'dd.MM.yyyy')
}
