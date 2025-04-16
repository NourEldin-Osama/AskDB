// Unified Backend API utility for authentication, threads, and chatbot

const API_BASE = "http://localhost:8000/api/v1";

export const BackendAPI = {
    async login(email: string, password: string): Promise<string> {
        const body = new URLSearchParams();
        body.append("username", email);
        body.append("password", password);

        const response = await fetch(`${API_BASE}/login/access-token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || "Login failed");
        }

        const data = await response.json();
        return data.access_token;
    },

    async fetchThreads(token: string) {
        const response = await fetch(`${API_BASE}/threads/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (!response.ok) throw new Error("Failed to fetch threads");
        return response.json();
    },

    async createThread(token: string, title: string) {
        const response = await fetch(`${API_BASE}/threads/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ title }),
        });
        if (!response.ok) throw new Error("Failed to create thread");
        return response.json();
    },

    async updateThread(token: string, id: string, title: string) {
        const response = await fetch(`${API_BASE}/threads/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ title }),
        });
        if (!response.ok) throw new Error("Failed to update thread");
        return response.json();
    },

    async deleteThread(token: string, id: string) {
        const response = await fetch(`${API_BASE}/threads/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        if (!response.ok) throw new Error("Failed to delete thread");
        return response.json();
    },

    async chatbotMessage(token: string, message: string, threadId?: string) {
        const body: any = { content: message };
        if (threadId) body.thread_id = threadId;

        const response = await fetch(`${API_BASE}/chatbot/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(body),
        });
        if (!response.ok) throw new Error("Failed to get chatbot response");
        return response.json();
    },

    async fetchChatHistory(token: string, threadId: string) {
        const response = await fetch(`${API_BASE}/chatbot/chat-history`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ thread_id: threadId }),
        });
        if (!response.ok) throw new Error("Failed to fetch chat history");
        return response.json();
    },
};
