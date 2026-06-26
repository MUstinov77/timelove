import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/Button'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Input } from '@/components/ui/Input'

const schema = z.object({
  email: z.email('Некорректный email'),
  password: z.string().min(6, 'Минимум 6 символов'),
  first_name: z.string().optional(),
  last_name: z.string().optional(),
})

type SignupFormData = z.infer<typeof schema>

export function SignupForm() {
  const { signup, login } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignupFormData>({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: SignupFormData) => {
    setError(null)
    try {
      await signup(data)
      await login({ email: data.email, password: data.password })
      navigate('/')
    } catch {
      setError('Не удалось создать аккаунт')
    }
  }

  return (
    <div className="auth-card">
      <h1>Регистрация</h1>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <Input label="Email" type="email" {...register('email')} error={errors.email?.message} />
        <Input
          label="Пароль"
          type="password"
          {...register('password')}
          error={errors.password?.message}
        />
        <Input label="Имя" {...register('first_name')} />
        <Input label="Фамилия" {...register('last_name')} />
        {error && <ErrorMessage message={error} />}
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Регистрация...' : 'Зарегистрироваться'}
        </Button>
      </form>
      <p className="auth-link">
        Уже есть аккаунт? <Link to="/login">Войти</Link>
      </p>
    </div>
  )
}
