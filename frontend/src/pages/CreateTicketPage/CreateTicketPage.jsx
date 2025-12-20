import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../app/providers/AuthProvider";
import { useToast } from "../../shared/ui/toast/ToastProvider";
import { Button } from "../../shared/ui/Button/Button";
import { BottomNav } from "../../widgets/BottomNav/BottomNav";
import "./CreateTicketPage.scss";

export const CreateTicketPage = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const { isLoading: authLoading, isAuthenticated } = useAuth();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const [errors, setErrors] = useState({ title: null, description: null });
  const [formError, setFormError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateTitle = (value) => {
    const trimmed = value.trim();
    if (!trimmed) return "Заголовок обязателен";
    if (trimmed.length < 4) return "Минимум 4 символа";
    return null;
  };

  const validateDescription = (value) => {
    const trimmed = value.trim();
    if (!trimmed) return "Описание обязательно";
    if (trimmed.length < 10) return "Минимум 10 символов";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(null);

    const titleError = validateTitle(title);
    const descriptionError = validateDescription(description);

    const newErrors = { title: titleError, description: descriptionError };
    setErrors(newErrors);

    if (titleError || descriptionError) return;

    setIsSubmitting(true);

    try {
      // Создание обращения через topics
      const res = await fetch("/api/topics/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
        }),
      });

      const json = await res.json().catch(() => null);

      if (!res.ok) {
        const msg =
          json?.detail || json?.message || "Не удалось создать обращение";
        setFormError(msg);
        toast.error(msg);
        return;
      }

      toast.success("Обращение создано");
      navigate("/tickets");
    } catch (error) {
      const msg = "Ошибка сети. Попробуйте ещё раз.";
      setFormError(msg);
      toast.error(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormInValid =
    !!errors.title ||
    !!errors.description ||
    !title.trim() ||
    !description.trim() ||
    isSubmitting;

  if (authLoading) {
    return (
      <div className="create-ticket-page create-ticket-page--loading">
        <p className="create-ticket-page__hint">Загрузка...</p>
      </div>
    );
  }

  return (
    <div className="create-ticket-page">
      <header className="create-ticket-page__header">
        <h1 className="create-ticket-page__title">Создать обращение</h1>
        <p className="create-ticket-page__subtitle">
          Опиши проблему — оператор увидит обращение в списке.
        </p>
      </header>

      <main className="create-ticket-page__content">
        <form
          className="create-ticket-page__form"
          onSubmit={handleSubmit}
          noValidate
        >
          <div className="create-ticket-page__field">
            <label className="create-ticket-page__label" htmlFor="topic-title">
              Заголовок
            </label>
            <input
              id="topic-title"
              className={
                errors.title
                  ? "create-ticket-page__input create-ticket-page__input--error"
                  : "create-ticket-page__input"
              }
              type="text"
              value={title}
              onChange={(e) => {
                const v = e.target.value;
                setTitle(v);
                setErrors((prev) => ({ ...prev, title: validateTitle(v) }));
                setFormError(null);
              }}
              placeholder="Например: Не открывается личный кабинет"
            />
            {errors.title && (
              <span className="create-ticket-page__error">{errors.title}</span>
            )}
          </div>

          <div className="create-ticket-page__field">
            <label
              className="create-ticket-page__label"
              htmlFor="topic-description"
            >
              Описание
            </label>
            <textarea
              id="topic-description"
              className={
                errors.description
                  ? "create-ticket-page__textarea create-ticket-page__textarea--error"
                  : "create-ticket-page__textarea"
              }
              value={description}
              onChange={(e) => {
                const v = e.target.value;
                setDescription(v);
                setErrors((prev) => ({
                  ...prev,
                  description: validateDescription(v),
                }));
                setFormError(null);
              }}
              placeholder="Что именно происходит, когда началось, шаги воспроизведения..."
              rows={6}
            />
            {errors.description && (
              <span className="create-ticket-page__error">
                {errors.description}
              </span>
            )}
          </div>

          {formError && (
            <div className="create-ticket-page__form-error">{formError}</div>
          )}

          <div className="create-ticket-page__actions">
            <Button
              type="button"
              variant="secondary"
              size="medium"
              onClick={() => navigate("/tickets")}
              disabled={isSubmitting}
            >
              Отмена
            </Button>

            <Button
              type="submit"
              variant="primary"
              size="medium"
              disabled={isFormInvalid}
            >
              {isSubmitting ? "Создаём..." : "Создать"}
            </Button>
          </div>
        </form>
      </main>

      <footer>
        <BottomNav />
      </footer>
    </div>
  );
};
