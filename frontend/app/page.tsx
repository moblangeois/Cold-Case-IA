"use client";

import Link from "next/link";
import { FileText, Search, MessageSquare, Database, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="border-b border-white/10 bg-black/20 backdrop-blur-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Search className="w-8 h-8 text-purple-400" />
              <span className="text-2xl font-bold text-white">Cold Case IA</span>
            </div>
            <div className="flex gap-4">
              <Link
                href="/chat"
                className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition-colors"
              >
                Démarrer
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Investigation Assistée
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
              par Intelligence Artificielle
            </span>
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            Explorez les cold cases avec Claude Sonnet 4.5, un assistant IA de pointe
            pour l&apos;analyse approfondie et la découverte de connexions cachées.
          </p>
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 px-8 py-4 bg-purple-600 hover:bg-purple-700 text-white text-lg font-semibold rounded-xl transition-all transform hover:scale-105"
          >
            Commencer l&apos;investigation
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-20">
          <FeatureCard
            icon={<MessageSquare className="w-8 h-8" />}
            title="Chat Intelligent"
            description="Conversez avec Claude Sonnet 4.5 pour explorer les détails du cas"
          />
          <FeatureCard
            icon={<Database className="w-8 h-8" />}
            title="RAG System"
            description="Système de recherche sémantique dans tous les documents"
          />
          <FeatureCard
            icon={<FileText className="w-8 h-8" />}
            title="Documents Multiples"
            description="Textes, PDFs, transcriptions et images analysés"
          />
          <FeatureCard
            icon={<Search className="w-8 h-8" />}
            title="Analyse Approfondie"
            description="Découvrez des connexions et patterns cachés"
          />
        </div>

        {/* Case Preview */}
        <div className="mt-20 bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-8">
          <h2 className="text-3xl font-bold text-white mb-4">Cas Kyron Horman</h2>
          <p className="text-gray-300 mb-6">
            Le 4 juin 2010, Kyron Horman, 7 ans, disparaît de son école élémentaire
            à Portland, Oregon. Malgré une enquête massive, le cas reste non résolu.
            Cette plateforme centralise toutes les informations disponibles pour faciliter
            l&apos;analyse et la découverte de nouvelles pistes.
          </p>
          <Link
            href="/cases/kyron_horman"
            className="inline-flex items-center gap-2 text-purple-400 hover:text-purple-300 font-semibold"
          >
            Explorer ce cas
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Technology Stack */}
        <div className="mt-20 text-center">
          <h3 className="text-2xl font-bold text-white mb-8">Technologies Utilisées</h3>
          <div className="flex flex-wrap justify-center gap-4">
            <TechBadge>Claude Sonnet 4.5</TechBadge>
            <TechBadge>Next.js 15</TechBadge>
            <TechBadge>FastAPI</TechBadge>
            <TechBadge>ChromaDB</TechBadge>
            <TechBadge>Sentence Transformers</TechBadge>
            <TechBadge>TailwindCSS</TechBadge>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-20 py-8">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>Cold Case IA - Démonstration technique d&apos;analyse assistée par IA</p>
          <p className="text-sm mt-2">
            Cet outil est à usage éducatif et démonstratif uniquement.
          </p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-colors">
      <div className="text-purple-400 mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-300 text-sm">{description}</p>
    </div>
  );
}

function TechBadge({ children }: { children: React.ReactNode }) {
  return (
    <span className="px-4 py-2 bg-purple-600/20 border border-purple-500/30 rounded-full text-purple-300 text-sm font-medium">
      {children}
    </span>
  );
}
