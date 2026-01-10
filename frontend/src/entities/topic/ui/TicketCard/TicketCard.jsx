import {
  ticketStatus,
  ticketStatusColors,
  ticketStatusLabels,
} from "../../model/type";
import "./TicketCard.scss";

const getInitialsFromOid = (oid) => {
  if (!oid) return "??";
  return oid.slice(0, 2).toUpperCase();
};

const formatRelativeTime = (iso) => {
  if (!iso) return "";
  const date = new Date(iso);
  const diffMs = Date.now() - date.getTime();
  if (Number.isNaN(diffMs)) return "";

  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "Только что";
  if (diffMin < 60) return `${diffMin} минут назад`;

  const diffH = Math.floor(diffMin / 60);
  if (diffH < 24) return `${diffH} часов назад`;

  const diffD = Math.floor(diffH / 24);
  if (diffD < 7) return `${diffD} дней назад`;

  return date.toLocaleDateString();
};

export const TicketCard = ({ topic, onClick, status }) => {
  const id = topic?.oid || "";
  const title = topic?.title || "Без темы";
  const createdAt = formatRelativeTime(topic?.created_at);
  const authorInitials = getInitialsFromOid(topic?.author_oid);

  // У topic'ов статусов нет, поэтому по умолчанию считаем  "new"
  const finalStatus = status || ticketStatus.new;
  const statusLabel = ticketStatusLabels[finalStatus] || "Новое";
  const statusColor = ticketStatusColors[finalStatus] || "Blue";

  const handleKeyDown = (e) => {
    if (e.key === "Enter" || e.key === " ") onClick?.();
  };

  return (
    <article
      className="ticket-card"
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      aria-label={`Открыть обращение ${id}`}
    >
      <div className="ticket-card__header">
        <span className="ticket-card__id">#{id.slice(0, 6)}</span>
        <span className="ticket-card__time">{createdAt}</span>
      </div>

      <h3 className="ticket-card__title">{title}</h3>

      <div className="ticket-card__footer">
        <span
          className={`ticket-card__status ticket-card__status--${statusColor}`}
        >
          {statusLabel}
        </span>
        <span className="ticket-card__author">{authorInitials}</span>
      </div>
    </article>
  );
};
