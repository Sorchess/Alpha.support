import { useEffect, useState, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../../app/providers/AuthProvider";
import { BottomNav } from "../../widgets/BottomNav/BottomNav";
import { topicApi } from "../../entities/topic";
import { topicStatusStorage } from "../../entities/topic/model/topicStatusStorage";
import {
  ticketStatus,
  ticketStatusLabels,
  ticketStatusColors,
} from "../../entities/topic/model/type";
import { Button } from "../../shared/ui/Button/Button";

import "./TicketDetailPage.scss";

const formatDateTime = (iso) => {
  if (!iso) return "";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

export const TicketDetailPage = () => {
  const navigate = useNavigate();
  const { topicOid } = useParams();
  const { isLoading: authLoading, isAuthenticated, user } = useAuth();

  const [topic, setTopic] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const [newMessage, setNewMessage] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [sendError, setSendError] = useState(null);

  const messagesEndRef = useRef(null);

  // Редирект неавторизованных
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate("/auth");
    }
  }, [authLoading, isAuthenticated, navigate]);

  // Загрузка данных обращения и сообщений
  useEffect(() => {
    if (authLoading || !isAuthenticated || !topicOid) return;

    const loadData = async () => {
      setIsLoading(true);
      setError(null);

      try {
        // Загружаем все topics и находим нужный
        const topicsRes = await topicApi.getTopics();
        if (!topicsRes.ok) {
          setError("Не удалось загрузить обращение");
          return;
        }

        const foundTopic = topicsRes.data.find((t) => t.oid === topicOid);
        if (!foundTopic) {
          setError("Обращение не найдено");
          return;
        }
        setTopic(foundTopic);

        // Загружаем сообщения
        const messagesRes = await topicApi.getMessages(topicOid);
        if (messagesRes.ok) {
          setMessages(messagesRes.data || []);
        }
      } catch (e) {
        setError("Ошибка сети. Попробуйте ещё раз.");
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [authLoading, isAuthenticated, topicOid]);

  // Прокрутка к последнему сообщению
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || isSending) return;

    setIsSending(true);
    setSendError(null);

    try {
      const res = await topicApi.sendMessage(topicOid, {
        content: newMessage.trim(),
      });

      if (!res.ok) {
        setSendError(res.error || "Не удалось отправить сообщение");
        return;
      }

      setMessages((prev) => [...prev, res.data]);
      setNewMessage("");

      // Обновляем статус на "В работе" если был "Новое"
      const currentStatus = topicStatusStorage.get(topicOid);
      if (currentStatus === ticketStatus.new) {
        topicStatusStorage.set(topicOid, ticketStatus.in_progress);
      }
    } catch (e) {
      setSendError("Ошибка сети. Попробуйте ещё раз.");
    } finally {
      setIsSending(false);
    }
  };

  const handleStatusChange = (newStatus) => {
    topicStatusStorage.set(topicOid, newStatus);
    // Форсим перерендер
    setTopic((prev) => ({ ...prev }));
  };

  const currentStatus = topicStatusStorage.get(topicOid) || ticketStatus.new;

  if (authLoading || isLoading) {
    return (
      <div className="ticket-detail-page ticket-detail-page--loading">
        <p className="ticket-detail-page__hint">Загрузка...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="ticket-detail-page ticket-detail-page--error">
        <p className="ticket-detail-page__hint">{error}</p>
        <Button variant="secondary" onClick={() => navigate("/tickets")}>
          Вернуться к списку
        </Button>
      </div>
    );
  }

  return (
    <div className="ticket-detail-page">
      <header className="ticket-detail-page__header">
        <button
          type="button"
          className="ticket-detail-page__back-btn"
          onClick={() => navigate("/tickets")}
          aria-label="Назад"
        >
          ←
        </button>
        <div className="ticket-detail-page__header-info">
          <h1 className="ticket-detail-page__title">
            {topic?.title || "Без темы"}
          </h1>
          <span className="ticket-detail-page__id">
            #{topicOid?.slice(0, 8)}
          </span>
        </div>
      </header>

      <main className="ticket-detail-page__content">
        {/* Информация об обращении */}
        <section className="ticket-detail-page__info">
          <div className="ticket-detail-page__info-row">
            <span className="ticket-detail-page__info-label">Статус:</span>
            <span
              className={`ticket-detail-page__status ticket-detail-page__status--${ticketStatusColors[currentStatus]}`}
            >
              {ticketStatusLabels[currentStatus]}
            </span>
          </div>
          <div className="ticket-detail-page__info-row">
            <span className="ticket-detail-page__info-label">Создано:</span>
            <span>{formatDateTime(topic?.created_at)}</span>
          </div>
          {topic?.description && (
            <div className="ticket-detail-page__description">
              <span className="ticket-detail-page__info-label">Описание:</span>
              <p>{topic.description}</p>
            </div>
          )}
        </section>

        {/* Кнопки смены статуса */}
        <section className="ticket-detail-page__actions">
          <span className="ticket-detail-page__actions-label">
            Изменить статус:
          </span>
          <div className="ticket-detail-page__status-buttons">
            {Object.entries(ticketStatus).map(([key, value]) => (
              <button
                key={key}
                type="button"
                className={`ticket-detail-page__status-btn ticket-detail-page__status-btn--${
                  ticketStatusColors[value]
                } ${
                  currentStatus === value
                    ? "ticket-detail-page__status-btn--active"
                    : ""
                }`}
                onClick={() => handleStatusChange(value)}
              >
                {ticketStatusLabels[value]}
              </button>
            ))}
          </div>
        </section>

        {/* Сообщения */}
        <section className="ticket-detail-page__messages">
          <h2 className="ticket-detail-page__messages-title">Переписка</h2>

          {messages.length === 0 ? (
            <p className="ticket-detail-page__no-messages">
              Сообщений пока нет. Напишите первый ответ!
            </p>
          ) : (
            <div className="ticket-detail-page__messages-list">
              {messages.map((msg) => (
                <div
                  key={msg.oid}
                  className={`ticket-detail-page__message ${
                    msg.author_oid === user?.oid
                      ? "ticket-detail-page__message--own"
                      : "ticket-detail-page__message--other"
                  }`}
                >
                  <div className="ticket-detail-page__message-content">
                    {msg.content}
                  </div>
                  <div className="ticket-detail-page__message-meta">
                    <span className="ticket-detail-page__message-author">
                      {msg.author_oid?.slice(0, 6)}
                    </span>
                    <span className="ticket-detail-page__message-time">
                      {formatDateTime(msg.sended_at)}
                    </span>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </section>

        {/* Форма отправки сообщения */}
        <form
          className="ticket-detail-page__reply-form"
          onSubmit={handleSendMessage}
        >
          {sendError && (
            <p className="ticket-detail-page__send-error">{sendError}</p>
          )}
          <div className="ticket-detail-page__reply-input-wrapper">
            <textarea
              className="ticket-detail-page__reply-input"
              placeholder="Напишите ответ..."
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              rows={3}
              disabled={isSending}
            />
            <Button
              type="submit"
              variant="primary"
              size="medium"
              disabled={!newMessage.trim() || isSending}
            >
              {isSending ? "Отправка..." : "Отправить"}
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
