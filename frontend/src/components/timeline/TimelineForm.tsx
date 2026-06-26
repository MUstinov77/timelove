import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import type { TimelineCreatePayload } from '@/types/timeline'

const schema = z.object({
  title: z.string().min(1, 'Введите название'),
})

interface TimelineFormProps {
  defaultValues?: TimelineCreatePayload
  submitLabel?: string
  onSubmit: (data: TimelineCreatePayload) => Promise<void>
}

export function TimelineForm({
  defaultValues,
  submitLabel = 'Сохранить',
  onSubmit,
}: TimelineFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<TimelineCreatePayload>({
    resolver: zodResolver(schema),
    defaultValues: defaultValues ?? { title: '' },
  })

  return (
    <form className="form" onSubmit={handleSubmit(onSubmit)}>
      <Input
        label="Название"
        {...register('title')}
        error={errors.title?.message}
        placeholder="Наша история"
      />
      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Сохранение...' : submitLabel}
      </Button>
    </form>
  )
}
