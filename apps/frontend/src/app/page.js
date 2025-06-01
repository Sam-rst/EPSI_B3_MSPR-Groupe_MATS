"use client";

import { useState } from 'react';
import { Database, BrainCircuit, TrendingUp, Activity } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* En-tête */}
      <header className="bg-white shadow-md fixed w-full top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <a href="#" className="flex items-center">
                <Activity className="h-8 w-8 text-blue-600" aria-hidden="true" />
                <span className="ml-2 text-xl font-bold text-gray-900">AnalyzeIT</span>
              </a>
            </div>

            {/* Navigation - Desktop */}
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-gray-900 hover:text-blue-600 px-3 py-2 font-medium">
                Accueil
              </a>
              <a href="#services" className="text-gray-900 hover:text-blue-600 px-3 py-2 font-medium">
                Services
              </a>
              <a href="#about" className="text-gray-900 hover:text-blue-600 px-3 py-2 font-medium">
                À propos
              </a>
            </nav>

            {/* Menu mobile */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setMenuOpen(!menuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 focus:outline-none"
                aria-expanded={menuOpen}
                aria-label={menuOpen ? "Fermer le menu" : "Ouvrir le menu"}
              >
                {menuOpen ? (
                  <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                ) : (
                  <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Menu mobile ouvert */}
        {menuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-blue-50">
                Accueil
              </a>
              <a href="#services" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-blue-50">
                Services
              </a>
              <a href="#about" className="block px-3 py-2 rounded-md text-base font-medium text-gray-900 hover:bg-blue-50">
                À propos
              </a>
            </div>
          </div>
        )}
      </header>

      {/* Contenu principal */}
      <main className="pt-16">
        {/* Bannière */}
        <section className="bg-blue-700 text-white py-16 md:py-24">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="md:flex md:items-center md:justify-between">
              <div className="md:w-1/2">
                <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4" id="main-heading">
                  Analyses de santé mondiale avec AnalyzeIT
                </h1>
                <p className="text-lg md:text-xl mb-8 text-blue-100">
                  Solutions de pointe pour analyser les données de santé mondiale et prédire les tendances épidémiologiques
                </p>
                <div className="flex flex-wrap gap-4">
                  <a
                    href="#services"
                    className="inline-block bg-white text-blue-700 font-bold py-3 px-6 rounded-lg shadow-lg hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-blue-700 transition-colors"
                    aria-label="Découvrir nos services"
                  >
                    Découvrir nos services
                  </a>
                  <a
                    href="#about"
                    className="inline-block bg-transparent border-2 border-white text-white font-bold py-3 px-6 rounded-lg hover:bg-white hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-white transition-colors"
                    aria-label="En savoir plus"
                  >
                    En savoir plus
                  </a>
                </div>
              </div>
              <div className="mt-8 md:mt-0 md:w-1/2 flex justify-center">
                <div className="w-64 h-64 bg-blue-600 rounded-full flex items-center justify-center shadow-xl">
                  <Activity className="h-32 w-32 text-white" aria-hidden="true" />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section services - Les 3 boutons demandés */}
        <section id="services" className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-2xl md:text-3xl font-bold text-gray-900">Nos Services</h2>
              <p className="mt-4 text-lg text-gray-600">Accédez à nos outils d'analyse et de traitement des données</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* ETL */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden transform transition duration-300 hover:scale-105">
                <div className="p-8 flex flex-col items-center">
                  <div className="rounded-full bg-blue-100 p-4 mb-4">
                    <Database className="h-8 w-8 text-blue-600" aria-hidden="true" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Accès ETL</h3>
                  <p className="text-gray-600 text-center mb-6">Extraction, transformation et chargement de données de santé mondiale</p>
                  <a
                    href="#"
                    className="inline-block bg-blue-600 text-white font-medium py-2 px-6 rounded hover:bg-blue-700 transition-colors"
                    aria-label="Accéder à l'ETL"
                  >
                    Accéder
                  </a>
                </div>
              </div>

              {/* IA */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden transform transition duration-300 hover:scale-105">
                <div className="p-8 flex flex-col items-center">
                  <div className="rounded-full bg-purple-100 p-4 mb-4">
                    <BrainCircuit className="h-8 w-8 text-purple-600" aria-hidden="true" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Accès IA</h3>
                  <p className="text-gray-600 text-center mb-6">Modèles prédictifs et analyses avancées par intelligence artificielle</p>
                  <Link
                    href="/analyse"
                    className="inline-block bg-purple-600 text-white font-medium py-2 px-6 rounded hover:bg-purple-700 transition-colors"
                    aria-label="Accéder à l'IA"
                  >
                    Accéder
                  </Link>
                </div>
              </div>

              {/* Metabase */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden transform transition duration-300 hover:scale-105">
                <div className="p-8 flex flex-col items-center">
                  <div className="rounded-full bg-green-100 p-4 mb-4">
                    <TrendingUp className="h-8 w-8 text-green-600" aria-hidden="true" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Accès Metabase</h3>
                  <p className="text-gray-600 text-center mb-6">Tableaux de bord interactifs et visualisation de données en temps réel</p>
                  <a
                    href="#"
                    className="inline-block bg-green-600 text-white font-medium py-2 px-6 rounded hover:bg-green-700 transition-colors"
                    aria-label="Accéder à Metabase"
                  >
                    Accéder
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section à propos */}
        <section className="py-16 bg-gray-50" id="about">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="md:flex md:items-center md:gap-12">
              <div className="md:w-1/2 mb-8 md:mb-0">
                <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">À propos d'AnalyzeIT</h2>
                <p className="text-gray-600 mb-4">
                  AnalyzeIT est une entreprise spécialisée dans l'analyse de données de santé mondiale, collaborant étroitement avec l'Organisation Mondiale de la Santé (OMS) pour fournir des insights précieux sur les tendances épidémiologiques.
                </p>
                <p className="text-gray-600 mb-4">
                  Notre mission est de mettre la puissance des données et de l'intelligence artificielle au service de la santé publique, en permettant une prise de décision éclairée et rapide face aux défis sanitaires mondiaux.
                </p>
              </div>
              <div className="md:w-1/2 flex justify-center">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-600 h-40 rounded-lg flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div className="bg-purple-600 h-40 rounded-lg flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <div className="bg-green-600 h-40 rounded-lg flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                    </svg>
                  </div>
                  <div className="bg-yellow-500 h-40 rounded-lg flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Pied de page */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-400">© 2025 AnalyzeIT. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}