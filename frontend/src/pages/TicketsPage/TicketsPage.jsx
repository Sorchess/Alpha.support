import { useNavigate } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";

import { useAuth } from "../../app/providers/AuthProvider";
import { TicketCard } from "../../entities/topic/ui/TicketCard/TicketCard";
import { BottomNav } from "../../widgets/BottomNav/BottomNav";
import { topicStatusStorage } from "../../entities/topic/model/topicStatusStorage";
import { ticketStatus } from "../../entities/topic/model/type";
import { loadTopics } from "../../features/topic/loadTopics";

import "./TicketsPage.scss";

const FILTER_TABS = [
  { key: "all", label: "Все" },
  { key: ticketStatus.new, label: "Новые" },
  { key: ticketStatus.in_progress, label: "В работе" },
  { key: ticketStatus.resolved, label: "Решено" },
];

export const TicketsPage = () => {
  const navigate = useNavigate();
  const { isLoading: authLoading, isAuthenticated } = useAuth();

  const [activeFilter, setActiveFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  const [topics, setTopics] = useState([]);
  const [isTopicsLoading, setIsTopicsLoading] = useState(false);
  const [topicError, setTopicError] = useState(null);

  // Редирект неавторизованных
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate("/auth");
    }
  }, [authLoading, isAuthenticated, navigate]);

  // Загрузка topics
  useEffect(() => {
    if (authLoading || !isAuthenticated) return;

    const load = async () => {
      setIsTopicsLoading(true);
      setTopicError(null);

      try {
        const res = await loadTopics();
        if (!res.ok) {
          setTopicError(res.error || "Не удалось загрузить обращения.");
          setTopics([]);
          return;
        }

        setTopics(res.data);
      } catch (e) {
        setTopicError("Ошибка сети. Попробуйте ещё раз.");
        setTopics([]);
      } finally {
        setIsTopicsLoading(false);
      }
    };

    load();
  }, [authLoading, isAuthenticated]);

  const filteredTopics = useMemo(() => {
    const query = searchQuery.toLowerCase().trim();

    return topics.filter((topic) => {
      const title = (topic?.title || "").toLowerCase();
      const oid = String(topic?.oid || "");
      const status = topicStatusStorage.get(topic?.oid);

      const matchStatus = activeFilter === "all" || status === activeFilter;
      const matchSearch =
        !query || title.includes(query) || oid.includes(query);

      return matchStatus && matchSearch;
    });
  }, [topics, activeFilter, searchQuery]);

  const handleTopicClick = (topic) => {
    navigate(`/tickets/${topic.oid}`);
  };

  if (authLoading) {
    return (
      <div className="tickets-page tickets-page--loading">
        <p className="tickets-page__hint">Загрузка...</p>
      </div>
    );
  }

  return (
    <div className="tickets-page">
      <header className="tickets-page__header">
        <h1 className="tickets-page__title">Обращения</h1>
      </header>

      <main className="tickets-page__content">
        <div className="tickets-page__search">
          <input
            className="tickets-page__search-input"
            placeholder="Поиск по теме или ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="tickets-page__filters">
          {FILTER_TABS.map((tab) => (
            <button
              key={tab.key}
              type="button"
              className={
                activeFilter === tab.key
                  ? "tickets-page__filter-btn tickets-page__filter-btn--active"
                  : "tickets-page__filter-btn"
              }
              onClick={() => setActiveFilter(tab.key)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {topicError ? (
          <p className="tickets-page__hint">{topicError}</p>
        ) : isTopicsLoading ? (
          <p className="tickets-page__hint">Загрузка обращений...</p>
        ) : filteredTopics.length === 0 ? (
          <p className="tickets-page__hint">Обращений не найдено</p>
        ) : (
          <div className="tickets-page__list">
            {filteredTopics.map((topic) => (
              <TicketCard
                key={topic.oid}
                topic={topic}
                status={topicStatusStorage.get(topic.oid)}
                onClick={() => handleTopicClick(topic)}
              />
            ))}
          </div>
        )}
      </main>

      <footer>
        <BottomNav />
      </footer>
    </div>
  );
};
