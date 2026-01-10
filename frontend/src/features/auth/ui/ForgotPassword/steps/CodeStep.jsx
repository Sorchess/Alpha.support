import { Button } from "../../../../../shared/ui/Button/Button";

export const CodeStep = ({
  email,
  code,
  setCode,
  loading,
  onSubmit,
  onBack,
}) => {
  return (
    <form className="auth-form" onSubmit={onSubmit}>
      <p className="forgot-hint">
        Мы отправили код на <strong>{email}</strong>. Введите его ниже, чтобы
        подтвердить, что это ваша почта.
      </p>

      <div className="auth-form__field">
        <label htmlFor="forgot-code" className="auth-form__label">
          Код из письма:
        </label>
        <input
          id="forgot-password"
          className="auth-form__input"
          type="text"
          placeholder="Ваш код"
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
      </div>

      <div className="auth-form__row">
        <button
          type="button"
          className="auth-form__link-button"
          onClick={onBack}
        >
          Назад
        </button>
      </div>

      <Button
        type="submit"
        variant="primary"
        size="medium"
        disabled={!code || loading}
      >
        {loading ? "Проверяем..." : "Подтвердить код"}
      </Button>
    </form>
  );
};
