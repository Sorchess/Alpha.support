import { Button } from "../../../../../shared/ui/Button/Button";

export const EmailStep = ({ email, setEmail, loading, onSubmit }) => {
  return (
    <form className="auth-form" onSubmit={onSubmit}>
      <div className="auth-form__field">
        <label htmlFor="forgot-email" className="auth-form-label">
          Email
        </label>
        <input
          id="forgot-email"
          className="auth-form__input"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
        />
      </div>

      <p className="forgot__hint">
        Введите почту, на которую зарегистрирован аккаунт. Мы отправим на неё
        код для восстановления.
      </p>

      <Button
        className="auth-form__submit"
        type="submit"
        disabled={!email || loading}
        variant="primary"
      >
        {loading ? "Отправляем..." : "Отправить код"}
      </Button>
    </form>
  );
};
