import { request } from "../../../shared/api/request";

export const topicApi = {
  async getTopics() {
    return request("/api/topics/", { method: "GET" });
  },

  async createTopic(payload) {
    return request("/api/topics/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
