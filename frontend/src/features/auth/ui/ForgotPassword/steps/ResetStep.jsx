import { Button } from "../../../../../shared/ui/Button/Button";

export const ResetStep = ({ loading, onSubmit }) => {
  const [password, setPassword] = useState("");
  const [repeat, setRepeat] = useState("");
  const [error, setError] = useState(null);

  const handleLocalSubmit = (e) => {
    e.preventDefault();
    if (!password && password.length < 6) {
      setError("Пароль должен быт минимум 6 символов");
      return;
    }
    if (password !== repeat) {
      setError("Пароли не совпадают");
    }
    setError(null);
    onSubmit(password);
  };

  return (
    <form className="auth-form" onSubmit={handleLocalSubmit}>
      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="new-password">
          Новый пароль
        </label>
        <input
          id="new-password"
          className="auth-form__input"
          type="password"
          placeholder="Введите новый пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <div className="auth-form__field">
        <label className="auth-form__label" htmlFor="new-password-repeat">
          Повторите пароль
        </label>
        <input
          id="new-password-repeat"
          className="auth-form__input"
          type="password"
          placeholder="Повторите новый пароль"
          value={repeat}
          onChange={(e) => setRepeat(e.target.value)}
        />
      </div>

      {error && <div className="forgot__error">{error}</div>}

      <Button
        className="auth-form__submit"
        type="submit"
        disabled={loading}
        variant="primary"
      >
        {loading ? "Обновляем..." : "Обновить пароль"}
      </Button>
    </form>
  );
};
