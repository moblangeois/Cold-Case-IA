"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  FileText,
  Image as ImageIcon,
  FolderOpen,
  Search,
  Download,
  BarChart3,
} from "lucide-react";
import { casesAPI, filesAPI, type CaseInfo, type DocumentInfo } from "@/lib/api";

export default function CasePage() {
  const params = useParams();
  const caseId = params.id as string;

  const [caseInfo, setCaseInfo] = useState<CaseInfo | null>(null);
  const [documents, setDocuments] = useState<DocumentInfo[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedContentType, setSelectedContentType] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    loadData();
  }, [caseId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [caseData, docsData, statsData] = await Promise.all([
        casesAPI.getCase(caseId),
        filesAPI.listDocuments(),
        casesAPI.getStats(caseId),
      ]);

      setCaseInfo(caseData);
      setDocuments(docsData);
      setStats(statsData);
    } catch (error) {
      console.error("Error loading case data:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredDocuments = documents.filter((doc) => {
    const matchesContentType = !selectedContentType || doc.content_type === selectedContentType;
    const matchesSearch =
      !searchQuery ||
      doc.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (doc.preview && doc.preview.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesContentType && matchesSearch;
  });

  const contentTypes = Array.from(new Set(documents.map((d) => d.content_type)));

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Chargement...</div>
      </div>
    );
  }

  if (!caseInfo) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Cas non trouvé</div>
      </div>
    );
  }

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
              <span className="text-xl font-bold text-white">{caseInfo.name}</span>
            </div>
            <Link
              href="/chat"
              className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition-colors"
            >
              Discuter avec Claude
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        {/* Case Info Header */}
        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-8 mb-6">
          <h1 className="text-4xl font-bold text-white mb-4">{caseInfo.name}</h1>
          <p className="text-gray-300 mb-4">{caseInfo.description}</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <StatCard label="Documents" value={caseInfo.documents_count} />
            <StatCard label="Images" value={caseInfo.images_count} />
            <StatCard label="Textes" value={caseInfo.texts_count} />
            <StatCard label="Statut" value={caseInfo.status.toUpperCase()} />
          </div>
        </div>

        {/* Stats */}
        {stats && (
          <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 mb-6">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-6 h-6" />
              Statistiques
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard label="Total Documents" value={stats.total_documents} />
              {stats.content_types &&
                Object.entries(stats.content_types).map(([type, count]: [string, any]) => (
                  <StatCard key={type} label={type} value={count} />
                ))}
            </div>
          </div>
        )}

        {/* Search and Filters */}
        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Rechercher dans les documents..."
                className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:border-purple-500"
              />
            </div>
            <select
              value={selectedContentType || ""}
              onChange={(e) => setSelectedContentType(e.target.value || null)}
              className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-purple-500"
            >
              <option value="">Tous les types</option>
              {contentTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Documents Grid */}
        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-6">
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
            <FolderOpen className="w-6 h-6" />
            Documents ({filteredDocuments.length})
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredDocuments.map((doc, index) => (
              <DocumentCard key={index} document={doc} />
            ))}
          </div>

          {filteredDocuments.length === 0 && (
            <div className="text-center py-12 text-gray-400">
              Aucun document trouvé
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4">
      <div className="text-sm text-gray-400 mb-1">{label}</div>
      <div className="text-2xl font-bold text-white">{value}</div>
    </div>
  );
}

function DocumentCard({ document }: { document: DocumentInfo }) {
  const getIcon = () => {
    switch (document.file_type) {
      case "image":
        return <ImageIcon className="w-6 h-6 text-purple-400" />;
      case "pdf":
        return <FileText className="w-6 h-6 text-red-400" />;
      case "text":
        return <FileText className="w-6 h-6 text-blue-400" />;
      default:
        return <FileText className="w-6 h-6 text-gray-400" />;
    }
  };

  const formatSize = (bytes?: number) => {
    if (!bytes) return "N/A";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-colors">
      <div className="flex items-start gap-3 mb-3">
        {getIcon()}
        <div className="flex-1 min-w-0">
          <h3 className="text-white font-medium text-sm truncate">{document.filename}</h3>
          <p className="text-xs text-gray-400">{document.content_type}</p>
        </div>
      </div>

      {document.preview && (
        <p className="text-xs text-gray-300 mb-3 line-clamp-2">{document.preview}</p>
      )}

      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-400">{formatSize(document.size)}</span>
        <a
          href={filesAPI.downloadFile(document.content_type, document.filename)}
          download
          className="text-purple-400 hover:text-purple-300 transition-colors"
        >
          <Download className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
}
