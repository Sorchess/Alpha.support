import { useState } from "react";
import { useAuth } from "../../../../app/providers/AuthProvider";
import { useToast } from "../../../../shared/ui/toast/ToastProvider";
import { Button } from "../../../../shared/ui/Button/Button";
import "./RegisterForm.scss";

export const RegisterForm = ({ onSubmit }) => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordRepeat, setPasswordRepeat] = useState("");
  const [agree, setAgree] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { register } = useAuth();
  const toast = useToast();

  const [errors, setErrors] = useState({
    fullName: null,
    email: null,
    password: null,
    passwordRepeat: null,
    agree: null,
  });

  const [formError, setFormError] = useState(null); // Ошибка от Backend
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateFullName = (value) => {
    const trimmed = value.trim();
    if (!trimmed) return "Имя обязательно";
    if (trimmed.length < 2) return "Слишком короткое имя";
    return null;
  };

  const validateEmail = (value) => {
    const trimmed = value.trim();
    if (!trimmed) return "Email обязателен";
    const emailregex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailregex.test(trimmed)) return "Некорректный email";
    return null;
  };

  const validatePassword = (value) => {
    if (!value) return "Пароль обязателен";
    if (value.length < 6) return "Минимум 6 символов";
    return null;
  };

  const validatePasswordRepeat = (value, original) => {
    if (!value) return "Повторите пароль";
    if (value !== original) return "Пароли не совпадают";
    return null;
  };

  const validateAgree = (value) => {
    if (!value) return "Необходимо согласие";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const fullNameError = validateFullName(fullName);
    const emailError = validateEmail(email);
    const passwordError = validatePassword(password);
    const passwordRepeatError = validatePasswordRepeat(
      passwordRepeat,
      password
    );
    const agreeError = validateAgree(agree);

    const newErrors = {
      fullName: fullNameError,
      email: emailError,
      password: passwordError,
      passwordRepeat: passwordRepeatError,
      agree: agreeError,
    };
    setErrors(newErrors);

    if (
      fullNameError ||
      emailError ||
      passwordError ||
      passwordRepeatError ||
      agreeError
    ) {
      return;
    }

    setIsSubmitting(true);

    try {
      const payLoad = {
        fullName: fullName.trim(),
        email: email.trim(),
        password,
        agree,
      };

      if (onSubmit) {
        // Старый режим ручного перехода
        await onSubmit(payLoad);
      } else {
        // Новый режим: регистрация через AuthProvider + backend
        const result = await register({
          email: payLoad.email,
          password,
        });

        if (!result.ok) {
          const msg = result.error || "Не удалось зарегистрироваться";
          setFormError(msg);
          toast.error(msg);
          return;
          // После успешной регистрации register сам залогинит пользователя через AuthPage и сделает navigate("/profile")
        }
        toast.success("Аккаунт создан. Вы вошли!")
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormInvalid =
    !fullName ||
    !email ||
    !password ||
    !passwordRepeat ||
    !agree ||
    !!errors.fullName ||
    !!errors.email ||
    !!errors.password ||
    !!errors.passwordRepeat ||
    !!errors.agree;

  return (
    <form className="auth-form" onSubmit={handleSubmit} noValidate>
      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="fullName">
          Имя
        </label>
        <input
          id="fullName"
          className={`auth-form__input ${
            errors.fullName ? "auth-form__input--error" : ""
          }`}
          type="text"
          placeholder="Как к вам обращаться?"
          value={fullName}
          onChange={(e) => {
            const value = e.target.value;
            setFullName(value);
            setErrors((prev) => ({
              ...prev,
              fullName: validateFullName(value),
            }));
          }}
        />
        {errors.fullName && (
          <span className="auth-form__error">{errors.fullName}</span>
        )}
      </div>

      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="reg-email">
          Email
        </label>
        <input
          id="reg-email"
          className={`auth-form__input ${
            errors.email ? "auth-form__input--error" : ""
          }`}
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => {
            const value = e.target.value;
            setEmail(value);
            setErrors((prev) => ({
              ...prev,
              email: validateEmail(value),
            }));
          }}
          autoComplete="email"
        />
        {errors.email && (
          <span className="auth-form__error">{errors.email}</span>
        )}
      </div>

      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="reg-password">
          Пароль
        </label>
        <div className="auth-form__password-wrapper">
          <input
            id="reg-password"
            className={`auth-form__input ${
              errors.password ? "auth-form__input--error" : ""
            }`}
            type={showPassword ? "text" : "password"}
            placeholder="Придумайте пароль"
            value={password}
            onChange={(e) => {
              const value = e.target.value;
              setPassword(value);
              setErrors((prev) => ({
                ...prev,
                password: validatePassword(value),
                passwordRepeat: validatePasswordRepeat(passwordRepeat, value),
              }));
            }}
            autoComplete="new-password"
          />

          <button
            type="button"
            className="auth-form__password-eye"
            onClick={() => setShowPassword((prev) => !prev)}
            aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
          >
            {showPassword ? (
              // перечёркнутый глаз
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
        {errors.password && (
          <span className="auth-form__error">{errors.password}</span>
        )}
      </div>

      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="reg-password-repeat">
          Повторите пароль
        </label>
        <input
          id="reg-password-repeat"
          className={`auth-form__input ${
            errors.passwordRepeat ? "auth-form__input--error" : ""
          }`}
          type="password"
          placeholder="Повторите пароль"
          value={passwordRepeat}
          onChange={(e) => {
            const value = e.target.value;
            setPasswordRepeat(value);
            setErrors((prev) => ({
              ...prev,
              passwordRepeat: validatePasswordRepeat(value, password),
            }));
          }}
          autoComplete="new-password"
        />
        {errors.passwordRepeat && (
          <span className="auth-form__error">{errors.passwordRepeat}</span>
        )}
      </div>

      <div className="auth-form__row auth-form__row_agree">
        <label className="auth-form__checkbox-label">
          <input
            className="auth-form__checkbox-input"
            type="checkbox"
            checked={agree}
            onChange={(e) => {
              const value = e.target.checked;
              setAgree(value);
              setErrors((prev) => ({
                ...prev,
                agree: validateAgree(value),
              }));
            }}
          />
          <span className="auth-form__checkbox-box" aria-hidden="true"></span>
          <span className="auth-form__checkbox-text">
            Согласен с обработкой персональных данных
          </span>
        </label>
        {errors.agree && (
          <span className="auth-form__error">{errors.agree}</span>
        )}
      </div>

      <Button
        className="auth-form__submit"
        type="submit"
        variant="primary"
        size="medium"
        disabled={isFormInvalid || isSubmitting}
      >
        {isSubmitting ? "Регистрируем..." : "Зарегистрироваться"}
      </Button>
    </form>
  );
};
