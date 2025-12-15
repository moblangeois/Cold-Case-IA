"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, FileText, Home, ArrowLeft } from "lucide-react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import { chatAPI, type ChatMessage, type ChatResponse } from "@/lib/api";

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [currentSources, setCurrentSources] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response: ChatResponse = await chatAPI.sendMessage({
        message: userMessage.content,
        conversation_id: conversationId || undefined,
        case_id: "kyron_horman",
        use_rag: true,
        max_tokens: 4096,
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.message,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setConversationId(response.conversation_id);

      if (response.sources) {
        setCurrentSources(response.sources);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: ChatMessage = {
        role: "assistant",
        content:
          "Désolé, une erreur s'est produite. Assurez-vous que le backend est démarré et que votre clé API Anthropic est configurée.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setConversationId(null);
    setCurrentSources([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="border-b border-white/10 bg-black/20 backdrop-blur-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link
                href="/"
                className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                Retour
              </Link>
              <span className="text-xl font-bold text-white">Chat Investigation</span>
            </div>
            <div className="flex gap-4">
              <button
                onClick={handleClearChat}
                className="px-4 py-2 rounded-lg bg-red-600/20 hover:bg-red-600/30 text-red-400 transition-colors"
              >
                Réinitialiser
              </button>
              <Link
                href="/cases/kyron_horman"
                className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition-colors"
              >
                Explorer le cas
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-12rem)]">
          {/* Chat Area */}
          <div className="lg:col-span-2 flex flex-col bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl overflow-hidden">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.length === 0 ? (
                <div className="text-center py-12">
                  <FileText className="w-16 h-16 text-purple-400 mx-auto mb-4" />
                  <h2 className="text-2xl font-bold text-white mb-2">
                    Démarrez une investigation
                  </h2>
                  <p className="text-gray-300">
                    Posez une question sur le cas Kyron Horman pour commencer l&apos;analyse
                  </p>
                  <div className="mt-6 space-y-2">
                    <p className="text-sm text-gray-400">Exemples de questions :</p>
                    <div className="flex flex-wrap gap-2 justify-center">
                      <SuggestionChip
                        onClick={() =>
                          setInput("Qui est Kyron Horman et que lui est-il arrivé ?")
                        }
                      >
                        Résumé du cas
                      </SuggestionChip>
                      <SuggestionChip
                        onClick={() =>
                          setInput("Quelles sont les personnes clés dans cette affaire ?")
                        }
                      >
                        Personnes impliquées
                      </SuggestionChip>
                      <SuggestionChip
                        onClick={() => setInput("Quelle est la chronologie des événements ?")}
                      >
                        Chronologie
                      </SuggestionChip>
                    </div>
                  </div>
                </div>
              ) : (
                messages.map((message, index) => (
                  <MessageBubble key={index} message={message} />
                ))
              )}

              {loading && (
                <div className="flex items-center gap-2 text-gray-300">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Claude analyse les documents...</span>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-white/10">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Posez une question sur le cas..."
                  className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-purple-500"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-xl transition-colors flex items-center gap-2"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Sources Sidebar */}
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 overflow-y-auto">
            <h3 className="text-xl font-bold text-white mb-4">Sources</h3>

            {currentSources.length > 0 ? (
              <div className="space-y-3">
                {currentSources.map((source, index) => (
                  <div
                    key={index}
                    className="p-3 bg-white/5 border border-white/10 rounded-lg"
                  >
                    <div className="text-sm font-medium text-purple-400 mb-1">
                      {source.content_type}
                    </div>
                    <div className="text-sm text-gray-300">{source.filename}</div>
                    {source.relevance !== null && source.relevance !== undefined && (
                      <div className="mt-2">
                        <div className="text-xs text-gray-400 mb-1">Pertinence</div>
                        <div className="w-full bg-white/10 rounded-full h-2">
                          <div
                            className="bg-purple-500 h-2 rounded-full"
                            style={{ width: `${(source.relevance * 100).toFixed(0)}%` }}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-400 text-sm">
                Les sources utilisées par Claude apparaîtront ici lors de vos recherches.
              </p>
            )}

            <div className="mt-6 pt-6 border-t border-white/10">
              <h4 className="text-sm font-semibold text-white mb-2">À propos du système</h4>
              <p className="text-xs text-gray-400">
                Ce chat utilise Claude Sonnet 4.5 avec un système RAG (Retrieval Augmented
                Generation) pour rechercher dans tous les documents du cas et fournir des
                réponses précises basées sur les sources disponibles.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} animate-fadeIn`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-purple-600 text-white"
            : "bg-white/5 border border-white/10 text-gray-100"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="prose prose-invert prose-sm max-w-none">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}

function SuggestionChip({
  children,
  onClick,
}: {
  children: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 rounded-full text-purple-300 text-sm transition-colors"
    >
      {children}
    </button>
  );
}
