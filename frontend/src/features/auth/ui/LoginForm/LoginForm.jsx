import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../../../shared/ui/Button/Button";
import "./LoginForm.scss";
import { useAuth } from "../../../../app/providers/AuthProvider";
import { useToast } from "../../../../shared/ui/toast/ToastProvider";

export const LoginForm = ({ onSubmit, onSwitchToRegister }) => {
  const navigate = useNavigate();
  const { login, isLoading: authLoading } = useAuth();
  const toast = useToast();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [errors, setErrors] = useState({ email: null, password: null });
  const [formError, setFormError] = useState(null); // ошибка от Backend
  const [isSubmitting, setIsSubmitting] = useState(false);

  // При первом рендере - подргружаем сохраннёный email, если он был "Запомнить меня"
  useEffect(() => {
    const savedEmail = localStorage.getItem("remembered-email");
    if (savedEmail) {
      setEmail(savedEmail);
      setRemember(true);
    }
  }, []);

  // Валидация email
  const validateEmail = (value) => {
    const trimmed = value.trim();
    if (!trimmed) return "Email обязателен";
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(trimmed)) return "Некорректный email";
    return null;
  };

  // Валидация пароля
  const validatePassword = (value) => {
    if (!value) return "Пароль обязателен";
    if (value.length < 6) return "Пароль должен быть минимум 6 символов";
    return null;
  };

  // Обработка изменения полей: email и пароля
  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    // Проверяем в реальном времени
    const error = validateEmail(value);
    setErrors((prev) => ({ ...prev, email: error }));
    setFormError(null);
  };

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);
    const error = validatePassword(value);
    setErrors((prev) => ({ ...prev, password: error }));
    setFormError(null);
  };

  // Обработка отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(null);

    // Валидация всех полей перед отправкой
    const emailError = validateEmail(email);
    const passwordError = validatePassword(password);
    const newErrors = {
      email: emailError,
      password: passwordError,
    };
    setErrors(newErrors);

    // Если ошибок есть - не отправляем форму
    if (emailError || passwordError) {
      return;
    }

    // Работа флажка - запомнить меня
    if (remember) {
      localStorage.setItem("remembered-email", email.trim());
    } else {
      localStorage.removeItem("remembered-email");
    }

    setIsSubmitting(true);

    // Вызов внешнего обработчика (из AuthPage)
    try {
      const payload = {
        email: email.trim(),
        password,
        remember,
      };
      if (onSubmit) {
        // Даём родителю самому решать, что делать
        await onSubmit(payload);
      } else {
        // авторизуем через AuthProvider + backend
        const result = await login({
          email: payload.email,
          password: payload.password,
        });

        if (!result.ok) {
          const msg = result.error || "Не удалось войти. Попробуйте ещё раз.";
          setFormError(msg);
          toast.error(msg);
          return;
        }
        toast.success("С возвращением!");
        // Переходим в профиль
        navigate("/profile");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormInValid =
    !!errors.email || !!errors.password || !email || !password;

  return (
    <form className="auth-form" onSubmit={handleSubmit} noValidate>
      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="email">
          Email
        </label>
        <input
          id="email"
          className={`auth-form__input ${
            errors.email ? "auth-form__input--error" : ""
          }`}
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={handleEmailChange}
          autoComplete="email"
        />
        {errors.email && (
          <span className="auth-form__error">{errors.email}</span>
        )}
      </div>

      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="password">
          Пароль
        </label>
        <div className="auth-form__password-wrapper">
          <input
            id="password"
            className={`auth-form__input ${
              errors.password ? "auth-form__input--error" : ""
            }`}
            type={showPassword ? "text" : "password"}
            placeholder="Введите пароль"
            value={password}
            onChange={handlePasswordChange}
            autoComplete="current-password"
          />

          <button
            type="button"
            className="auth-form__password-eye"
            onClick={() => setShowPassword((prev) => !prev)}
            aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
          >
            {showPassword ? (
              // Перечёркнутый глаз
              <svg
                className="auth-form__password-eye-icon"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M3 3l18 18"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
                <path
                  d="M10.58 10.58A3 3 0 0 0 13.42 13.4"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                  strokeLinecap="round"
                />
                <path
                  d="M9.88 5.1A9.77 9.77 0 0 1 12 5c5 0 8.5 3.5 9.5 7-0.32 1.2-0.92 2.3-1.74 3.3"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                  strokeLinecap="round"
                />
                <path
                  d="M4.24 4.24C2.86 5.53 1.9 7.16 1.5 9c1 3.5 4.5 7 9.5 7 1.1 0 2.1-0.16 3.02-0.46"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                  strokeLinecap="round"
                />
              </svg>
            ) : (
              // обычный глаз
              <svg
                className="auth-form__password-eye-icon"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  d="M2 12C3 8.5 7 5 12 5s9 3.5 10 7c-1 3.5-5 7-10 7S3 15.5 2 12z"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                />
                <circle
                  cx="12"
                  cy="12"
                  r="3"
                  stroke="currentColor"
                  strokeWidth="2"
                  fill="none"
                />
              </svg>
            )}
          </button>
        </div>

        {errors.email && (
          <span className="auth-form__error">{errors.password}</span>
        )}
      </div>
      <div className="auth-form__row auth-form__row_remember">
        <label className="auth-form__checkbox-label">
          <input
            className="auth-form__checkbox-input"
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
          />
          <span className="auth-form__checkbox-box" aria-hidden="true"></span>
          <span className="auth-form__checkbox-text">Запомнить меня</span>
        </label>
        <button
          type="button"
          className="auth-form__link-button"
          onClick={() => navigate("/auth/forgot")}
        >
          Забыли пароль?
        </button>
      </div>

      {formError && (
        <p className="login-form__error login-for__error--global">
          {formError}
        </p>
      )}
      <Button
        className="auth-form__submit"
        type="submit"
        variant="primary"
        size="medium"
        disabled={isFormInValid || isSubmitting || authLoading}
      >
        {isSubmitting || authLoading ? "Вход..." : "Войти"}
      </Button>
      <div className="auth-form__footer">
        <span>Нет аккаунта?</span>
        <button
          type="button"
          className="auth-form__link-button"
          onClick={onSwitchToRegister}
        >
          Зарегистрироваться
        </button>
      </div>
    </form>
  );
};
