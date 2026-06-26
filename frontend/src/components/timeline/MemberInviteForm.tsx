import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { MemberPermission } from '@/types/member'
import type { InviteMemberPayload } from '@/types/member'

const schema = z.object({
  member_id: z.number({ error: 'Укажите ID пользователя' }).min(1, 'Укажите ID пользователя'),
  member_permission: z.enum([
    MemberPermission.Member,
    MemberPermission.Moderator,
    MemberPermission.Admin,
  ]),
})

type MemberInviteFormData = z.infer<typeof schema>

interface MemberInviteFormProps {
  onSubmit: (data: InviteMemberPayload) => Promise<void>
}

export function MemberInviteForm({ onSubmit }: MemberInviteFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<MemberInviteFormData>({
    resolver: zodResolver(schema),
    defaultValues: { member_id: 0, member_permission: MemberPermission.Member },
  })

  return (
    <form className="form" onSubmit={handleSubmit(onSubmit)}>
      <Input
        label="ID пользователя"
        type="number"
        {...register('member_id', { valueAsNumber: true })}
        error={errors.member_id?.message}
      />
      <div className="form-field">
        <label className="form-label">Роль</label>
        <select className="form-input" {...register('member_permission')}>
          <option value={MemberPermission.Member}>Участник</option>
          <option value={MemberPermission.Moderator}>Модератор</option>
          <option value={MemberPermission.Admin}>Администратор</option>
        </select>
      </div>
      <Button type="submit" disabled={isSubmitting}>
        Пригласить
      </Button>
    </form>
  )
}
