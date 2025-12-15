import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  case_id?: string;
  use_rag?: boolean;
  max_tokens?: number;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources?: Array<{
    filename: string;
    content_type: string;
    relevance?: number;
  }>;
  tokens_used?: number;
}

export interface CaseInfo {
  id: string;
  name: string;
  description: string;
  date?: string;
  location?: string;
  status: string;
  documents_count: number;
  images_count: number;
  texts_count: number;
}

export interface SearchRequest {
  query: string;
  case_id?: string;
  limit?: number;
  content_types?: string[];
}

export interface SearchResult {
  content: string;
  content_type: string;
  filename: string;
  score: number;
  metadata?: any;
}

export interface DocumentInfo {
  filename: string;
  content_type: string;
  file_type: string;
  size?: number;
  path: string;
  preview?: string;
}

// API Client
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatAPI = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/api/chat/', request);
    return response.data;
  },

  clearConversation: async (conversationId: string): Promise<void> => {
    await api.delete(`/api/chat/${conversationId}`);
  },

  getConversation: async (conversationId: string): Promise<{ messages: ChatMessage[] }> => {
    const response = await api.get(`/api/chat/${conversationId}`);
    return response.data;
  },
};

// Cases API
export const casesAPI = {
  getCases: async (): Promise<CaseInfo[]> => {
    const response = await api.get<CaseInfo[]>('/api/cases/');
    return response.data;
  },

  getCase: async (caseId: string): Promise<CaseInfo> => {
    const response = await api.get<CaseInfo>(`/api/cases/${caseId}`);
    return response.data;
  },

  search: async (request: SearchRequest): Promise<SearchResult[]> => {
    const response = await api.post<SearchResult[]>('/api/cases/search', request);
    return response.data;
  },

  getStats: async (caseId: string): Promise<any> => {
    const response = await api.get(`/api/cases/${caseId}/stats`);
    return response.data;
  },
};

// Files API
export const filesAPI = {
  listDocuments: async (contentType?: string): Promise<DocumentInfo[]> => {
    const params = contentType ? { content_type: contentType } : {};
    const response = await api.get<DocumentInfo[]>('/api/files/documents', { params });
    return response.data;
  },

  getFileContent: async (contentType: string, filename: string): Promise<{ content: string; type: string }> => {
    const response = await api.get(`/api/files/content/${contentType}/${filename}`);
    return response.data;
  },

  downloadFile: (contentType: string, filename: string): string => {
    return `${API_URL}/api/files/download/${contentType}/${filename}`;
  },
};

export default api;
