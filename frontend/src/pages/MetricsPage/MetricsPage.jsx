import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../app/providers/AuthProvider";
import { BottomNav } from "../../widgets/BottomNav/BottomNav";
import { ticketStatus, ticketStatusLabels } from "../../entities/topic";
import { topicStatusStorage } from "../../entities/topic/model/topicStatusStorage";
import { loadTopics } from "../../features/topic/loadTopics";

import "./MetricsPage.scss";

const isSameDay = (a, b) =>
  a.getFullYear() === b.getFullYear() &&
  a.getMonth() === b.getMonth() &&
  a.getDate() === b.getDate();

export const MetricsPage = () => {
  const navigate = useNavigate();
  const { isLoading: authLoading, isAuthenticated } = useAuth();

  const [topics, setTopics] = useState([]);
  const [isTopicLoading, setIsTopicLoading] = useState(false);
  const [topicsError, setTopicsError] = useState(null);

  // Редирект неавторизованыых
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate("/auth");
    }
  }, [authLoading, isAuthenticated, navigate]);

  // Загружаем topics
  useEffect(() => {
    if (authLoading || !isAuthenticated) return;

    const load = async () => {
      setIsTopicLoading(true);
      setTopicsError(null);

      try {
        const res = await loadTopicss();
        if (!res.ok) {
          setTopicsError(res.error || "Не удалось загрузить метрики");
          setTopics([]);
          return;
        }

        setTopics(res.data);
      } catch (e) {
        setTopicsError("Ошибка сети. Попробуйте ещё раз.");
        setTopics([]);
      } finally {
        setIsTopicLoading(false);
      }
    };

    load();
  }, [authLoading, isAuthenticated]);

  const Metrics = useMemo(() => {
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    const parsed = topics
      .map((t) => ({
        ...t,
        createdAtDate: t?.created_at ? new Date(t.created_at) : null,
      }))
      .filter(
        (t) => t.createdAtDate && !Number.isNaN(t.createdAtDate.getTime())
      );

    const total = topics.length;

    const todayCount = parsed.filter((t) =>
      isSameDay(t.createdAtDate, now)
    ).length;
    const last7DaysCount = parsed.filter(
      (t) => t.createdAtDate >= weekAgo
    ).length;

    const latest = [...parsed]
      .sort((a, b) => b.createdAtDate.getTime() - a.createdAtDate.getTime())
      .slice(0, 5);

    const statusMap = topicStatusStorage.getAll();

    const newCount = topics.filter(
      (t) => (statusMap[t?.oid] || ticketStatus.new) === ticketStatus.new
    ).length;

    const inProgressCount = topics.filter(
      (t) =>
        (statusMap[t?.oid] || ticketStatus.new) === ticketStatus.in_progress
    ).length;

    const resolvedCount = topics.filter(
      (t) => (statusMap[t?.oid] || ticketStatus.new) === ticketStatus.resolved
    ).length;

    return {
      total,
      todayCount,
      last7DaysCount,
      latest,
      newCount,
      inProgressCount,
      resolvedCount,
    };
  }, [topics]);

  if (authLoading) {
    return (
      <div className="metrics-page metrics-page--loading">
        <p className="metrics-page__hint">Загрузка...</p>
      </div>
    );
  }

  return (
    <div className="metrics-page">
      <header className="metrics-page__header">
        <h1 className="metrics-page__title">Метрики</h1>
        <p className="metrics-page__subtitle">
          Считаются на клиенте по обращениям (topics).
        </p>
      </header>

      <main className="metrics-page__content">
        {topicsError ? (
          <div className="metrics-page__error">{topicsError}</div>
        ) : (
          <>
            <section className="metrics-page__grid">
              <div className="metric-card">
                <div className="metric-card__label">Всего обращений</div>
                <div className="metric-card__value">{Metrics.total}</div>
              </div>

              <div className="metric-card">
                <div className="metric-card__label">
                  {ticketStatusLabels[ticketStatus.new]}
                </div>
                <div className="metric-card__value">{Metrics.newCount}</div>
              </div>

              <div className="metric-card">
                <div className="metric-card__label">
                  {ticketStatusLabels[ticketStatus.in_progress]}
                </div>
                <div className="metric-card__value">
                  {Metrics.inProgressCount}
                </div>
              </div>

              <div className="metric-card">
                <div className="metric-card__label">
                  {ticketStatusLabels[ticketStatus.resolved]}
                </div>
                <div className="metric-card__value">
                  {Metrics.resolvedCount}
                </div>
              </div>

              <div className="metric-card">
                <div className="metric-card__label">Создано сегодня</div>
                <div className="metric-card__value">{Metrics.todayCount}</div>
              </div>

              <div className="metric-card">
                <div className="metric-card__label">За 7 дней</div>
                <div className="metric-card__value">
                  {Metrics.last7DaysCount}
                </div>
              </div>

              <div
                className="metric-card metric-card--action"
                onClick={() => navigate("/tickets")}
              >
                <div className="metric-card__label">Перейти к списку</div>
                <div className="metric-card__value">→</div>
              </div>
            </section>

            <section className="metrics-page__section">
              <h2 className="metrics-page__section-title">
                Последние обращения
              </h2>

              {isTopicLoading ? (
                <p className="metrics-page__hint">Загрузка обращений...</p>
              ) : Metrics.latest.length === 0 ? (
                <p className="metrics-page__hint">Пока нет обращений.</p>
              ) : (
                <ul className="metrics-page__latest">
                  {Metrics.latest.map((t) => (
                    <li key={t.oid} className="metrics-page__latest-item">
                      <div className="metrics-page__latest-title">
                        {t.title}
                      </div>
                      <div className="metrics-page__latest-meta">
                        <span>#{String(t.oid).slice(0, 6)}</span>
                        <span>•</span>
                        <span>
                          {t.createdAtDate.toLocaleString(undefined, {
                            day: "2-digit",
                            month: "2-digit",
                            year: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </>
        )}
      </main>

      <footer>
        <BottomNav />
      </footer>
    </div>
  );
};
