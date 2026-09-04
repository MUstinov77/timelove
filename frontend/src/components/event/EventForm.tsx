import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Textarea } from '@/components/ui/Textarea'
import type { EventCreatePayload } from '@/types/event'

const schema = z.object({
  title: z.string().min(1, 'Введите название'),
  event_date: z.string().min(1, 'Укажите дату'),
  description: z.string()
})

interface EventFormProps {
  defaultValues?: EventCreatePayload
  submitLabel?: string
  onSubmit: (data: EventCreatePayload) => Promise<void>
}

export function EventForm({
  defaultValues,
  submitLabel = 'Сохранить',
  onSubmit,
}: EventFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<EventCreatePayload>({
    resolver: zodResolver(schema),
    defaultValues: defaultValues ?? { title: '', event_date: '', description: '' },
  })

  return (
    <form className="form" onSubmit={handleSubmit(onSubmit)}>
      <Input
        label="Название"
        {...register('title')}
        error={errors.title?.message}
        placeholder="Первое свидание"
      />
      <Input
        label="Дата"
        type="date"
        {...register('event_date')}
        error={errors.event_date?.message}
      />
      <Textarea
        label="Описание"
        rows={5}
        {...register('description')}
        placeholder="Расскажите о событии..."
      />
      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Сохранение...' : submitLabel}
      </Button>
    </form>
  )
}
