import { ticketStatus } from "./type";

const STORAGE_KEY = "topic-status-by-oid";

const safeParse = (value) => {
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
};

export const topicStatusStorage = {
  getAll() {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = safeParse(raw);
    return parsed && typeof parsed === "object" ? parsed : {};
  },

  get(topicOid) {
    if (!topicOid) return ticketStatus.new;
    const map = this.getAll();
    return map[topicOid] || ticketStatus.new;
  },

  set(topicOid, status) {
    if (!topicOid) return;
    const map = this.getAll();
    map[topicOid] = status;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
  },

  ensure(topicOid) {
    // Для того чтобы старые "topics" без статуса получили new
    if (!topicOid) return;
    const map = this.getAll();
    if (!map[topicOid]) {
      map[topicOid] = ticketStatus.new;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
    }
  },
};
