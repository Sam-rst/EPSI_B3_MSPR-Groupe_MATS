"use client";

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

// Données importées
const countriesData = [
  { "name": "China", "iso2": "CN", "iso3": "CHN", "population": 1439323776, "continent_id": 4 },
  { "name": "India", "iso2": "IN", "iso3": "IND", "population": 1380004385, "continent_id": 4 },
  { "name": "United States", "iso2": "US", "iso3": "USA", "population": 331002651, "continent_id": 5 },
  { "name": "Indonesia", "iso2": "ID", "iso3": "IDN", "population": 273523615, "continent_id": 4 },
  { "name": "Pakistan", "iso2": "PK", "iso3": "PAK", "population": 220892340, "continent_id": 4 },
  { "name": "Brazil", "iso2": "BR", "iso3": "BRA", "population": 212559417, "continent_id": 6 },
  { "name": "Nigeria", "iso2": "NG", "iso3": "NGA", "population": 206139589, "continent_id": 2 },
  { "name": "Bangladesh", "iso2": "BD", "iso3": "BGD", "population": 164689383, "continent_id": 4 },
  { "name": "Russia", "iso2": "RU", "iso3": "RUS", "population": 145912025, "continent_id": 3 },
  { "name": "Japan", "iso2": "JP", "iso3": "JPN", "population": 126476461, "continent_id": 4 }
];

const epidemicsData = [
  { "name": "COVID-19", "start_date": "2019-12-01", "end_date": "2023-05-05", "type": "virus", "pathogen_name": "SARS-CoV-2", "reproduction_rate": 2.5 },
  { "name": "Ebola Outbreak West Africa", "start_date": "2013-12-01", "end_date": "2016-06-09", "type": "virus", "pathogen_name": "Ebola virus", "reproduction_rate": 1.8 },
  { "name": "H1N1 Influenza Pandemic", "start_date": "2009-04-01", "end_date": "2010-08-10", "type": "virus", "pathogen_name": "H1N1 Influenza Virus", "reproduction_rate": 1.5 },
  { "name": "Cholera Outbreak Haiti", "start_date": "2010-10-01", "end_date": "2019-01-01", "type": "bacteria", "pathogen_name": "Vibrio cholerae", "reproduction_rate": 1.4 },
  { "name": "Plague of Madagascar", "start_date": "2017-08-01", "end_date": "2018-03-01", "type": "bacteria", "pathogen_name": "Yersinia pestis", "reproduction_rate": 1.3 },
  { "name": "Sleeping Sickness Epidemic", "start_date": "1970-01-01", "end_date": "1990-01-01", "type": "parasite", "pathogen_name": "Trypanosoma brucei", "reproduction_rate": 1.2 },
  { "name": "Malaria Epidemic Ethiopia", "start_date": "2003-01-01", "end_date": "2004-12-31", "type": "parasite", "pathogen_name": "Plasmodium falciparum", "reproduction_rate": 1.4 },
  { "name": "Kuru Epidemic Papua New Guinea", "start_date": "1957-01-01", "end_date": "1980-01-01", "type": "prion", "pathogen_name": "Prion protein", "reproduction_rate": 1.1 },
  { "name": "Candidiasis Outbreak Hospitals", "start_date": "2015-01-01", "end_date": "2020-01-01", "type": "fungus", "pathogen_name": "Candida auris", "reproduction_rate": 1.2 }
];

const vaccinesData = [
  { "name": "Pfizer/BioNTech", "laboratory": "Pfizer/BioNTech", "technology": "mRNA", "dose": "2 doses, 3 weeks apart", "efficacy": 95.0, "storage_temperature": "-70°C (long terme), 2–8°C (5 jours)" },
  { "name": "Moderna", "laboratory": "Moderna", "technology": "mRNA", "dose": "2 doses, 4 weeks apart", "efficacy": 94.1, "storage_temperature": "-20°C (long terme), 2–8°C (30 jours)" },
  { "name": "Sputnik V", "laboratory": "Gamaleya Research Institute", "technology": "Viral vector (adenovirus 26 and 5)", "dose": "2 doses, 3 weeks apart", "efficacy": 91.6, "storage_temperature": "2–8°C" },
  { "name": "Novavax", "laboratory": "Novavax", "technology": "Protein subunit", "dose": "2 doses, 3 weeks apart", "efficacy": 89.7, "storage_temperature": "2–8°C" },
  { "name": "Covaxin", "laboratory": "Bharat Biotech", "technology": "Inactivated virus", "dose": "2 doses, 4 weeks apart", "efficacy": 77.8, "storage_temperature": "2–8°C" },
  { "name": "Sinopharm/Beijing", "laboratory": "Sinopharm", "technology": "Inactivated virus", "dose": "2 doses, 3–4 weeks apart", "efficacy": 79.0, "storage_temperature": "2–8°C" },
  { "name": "Oxford/AstraZeneca", "laboratory": "AstraZeneca", "technology": "Viral vector (adenovirus from chimpanzee)", "dose": "2 doses, 4-12 weeks apart", "efficacy": 76.0, "storage_temperature": "2–8°C" },
  { "name": "Johnson&Johnson", "laboratory": "Johnson & Johnson", "technology": "Viral vector (adenovirus type 26)", "dose": "1 dose", "efficacy": 66.9, "storage_temperature": "2–8°C" },
  { "name": "CanSino", "laboratory": "CanSino Biologics", "technology": "Viral vector (adenovirus type 5)", "dose": "1 dose", "efficacy": 65.28, "storage_temperature": "2–8°C" },
  { "name": "Sinovac", "laboratory": "Sinovac Biotech", "technology": "Inactivated virus", "dose": "2 doses, 2–4 weeks apart", "efficacy": 51.0, "storage_temperature": "2–8°C" }
];

const continentsData = [
  { "name": "Not defined", "code": "N/A", "population": 0, "id": 1 },
  { "name": "Africa", "code": "AF", "population": 1400000000, "id": 2 },
  { "name": "Europe", "code": "EU", "population": 750000000, "id": 3 },
  { "name": "Asia", "code": "AS", "population": 4600000000, "id": 4 },
  { "name": "North America", "code": "NA", "population": 600000000, "id": 5 },
  { "name": "South America", "code": "SA", "population": 430000000, "id": 6 },
  { "name": "Oceania", "code": "OC", "population": 43000000, "id": 7 },
  { "name": "Antarctica", "code": "AN", "population": 1100, "id": 8 }
];

// Préparer les données avec les noms de continents
const countriesWithContinents = countriesData.map(country => {
  const continent = continentsData.find(cont => cont.id === country.continent_id);
  return {
    ...country,
    continent: continent ? continent.name : "Unknown"
  };
});

export default function AnalysePage() {
  const [activeTab, setActiveTab] = useState('countries');
  const [filterValue, setFilterValue] = useState('');

  // Références pour les graphiques Plotly
  const populationChartRef = useRef(null);
  const continentPieChartRef = useRef(null);
  const epidemicChartRef = useRef(null);
  const epidemicTypeChartRef = useRef(null);
  const vaccineChartRef = useRef(null);
  const vaccineTechChartRef = useRef(null);

  // Fonction pour filtrer les données selon l'onglet actif
  const getFilteredData = () => {
    const filter = filterValue.toLowerCase();

    switch (activeTab) {
      case 'countries':
        return countriesWithContinents.filter(country =>
          country.name.toLowerCase().includes(filter) ||
          country.continent.toLowerCase().includes(filter)
        );
      case 'epidemics':
        return epidemicsData.filter(epidemic =>
          epidemic.name.toLowerCase().includes(filter) ||
          epidemic.type.toLowerCase().includes(filter) ||
          epidemic.pathogen_name.toLowerCase().includes(filter)
        );
      case 'vaccines':
        return vaccinesData.filter(vaccine =>
          vaccine.name.toLowerCase().includes(filter) ||
          vaccine.laboratory.toLowerCase().includes(filter) ||
          vaccine.technology.toLowerCase().includes(filter)
        );
      default:
        return [];
    }
  };

  // Effet pour charger Plotly et créer les graphiques
  useEffect(() => {
    const loadPlotly = async () => {
      if (typeof window !== 'undefined') {
        if (!window.Plotly) {
          const script = document.createElement('script');
          script.src = 'https://cdn.plot.ly/plotly-2.24.1.min.js';
          script.async = true;

          script.onload = () => {
            createCharts();
          };

          document.head.appendChild(script);
        } else {
          createCharts();
        }
      }
    };

    loadPlotly();

    return () => {
      if (typeof window !== 'undefined') {
        const script = document.querySelector('script[src="https://cdn.plot.ly/plotly-2.24.1.min.js"]');
        if (script) {
          document.head.removeChild(script);
        }
      }
    };
  }, [activeTab, filterValue]);

  // Fonction pour créer les graphiques
  const createCharts = () => {
    if (typeof window === 'undefined' || !window.Plotly) return;

    const filteredData = getFilteredData();

    if (activeTab === 'countries') {
      if (populationChartRef.current && continentPieChartRef.current) {
        createCountryCharts(filteredData);
      }
    } else if (activeTab === 'epidemics') {
      if (epidemicChartRef.current && epidemicTypeChartRef.current) {
        createEpidemicCharts(filteredData);
      }
    } else if (activeTab === 'vaccines') {
      if (vaccineChartRef.current && vaccineTechChartRef.current) {
        createVaccineCharts(filteredData);
      }
    }
  };

  // Fonction pour créer les graphiques des pays
  const createCountryCharts = (data) => {
    // Graphique à barres des populations
    const sortedData = [...data].sort((a, b) => b.population - a.population);
    const top10 = sortedData.slice(0, 10);

    const populationBarChart = {
      x: top10.map(country => country.name),
      y: top10.map(country => country.population),
      type: 'bar',
      marker: {
        color: 'rgb(59, 130, 246)'
      }
    };

    window.Plotly.newPlot(populationChartRef.current, [populationBarChart], {
      title: 'Top 10 des pays par population',
      xaxis: { title: 'Pays' },
      yaxis: { title: 'Population' },
      margin: { t: 50, r: 50, b: 100, l: 80 }
    }, { responsive: true });

    // Graphique circulaire par continent
    const populationByContinent = {};
    data.forEach(country => {
      if (!populationByContinent[country.continent]) {
        populationByContinent[country.continent] = 0;
      }
      populationByContinent[country.continent] += country.population;
    });

    const continentPieChart = {
      labels: Object.keys(populationByContinent),
      values: Object.values(populationByContinent),
      type: 'pie',
      marker: {
        colors: ['rgb(59, 130, 246)', 'rgb(139, 92, 246)', 'rgb(236, 72, 153)', 'rgb(245, 158, 11)', 'rgb(16, 185, 129)', 'rgb(99, 102, 241)', 'rgb(239, 68, 68)']
      }
    };

    window.Plotly.newPlot(continentPieChartRef.current, [continentPieChart], {
      title: 'Population par continent',
      margin: { t: 50, r: 50, b: 50, l: 50 }
    }, { responsive: true });
  };

  // Fonction pour créer les graphiques des épidémies
  const createEpidemicCharts = (data) => {
    // Graphique à barres des taux de reproduction
    const epidemicBarChart = {
      x: data.map(epidemic => epidemic.name),
      y: data.map(epidemic => epidemic.reproduction_rate),
      type: 'bar',
      marker: {
        color: 'rgb(139, 92, 246)'
      }
    };

    window.Plotly.newPlot(epidemicChartRef.current, [epidemicBarChart], {
      title: 'Taux de reproduction (R0) des épidémies',
      xaxis: { title: 'Épidémie' },
      yaxis: { title: 'Taux R0' },
      margin: { t: 50, r: 50, b: 100, l: 80 }
    }, { responsive: true });

    // Graphique circulaire par type
    const epidemicsByType = {};
    data.forEach(epidemic => {
      if (!epidemicsByType[epidemic.type]) {
        epidemicsByType[epidemic.type] = 0;
      }
      epidemicsByType[epidemic.type]++;
    });

    const epidemicPieChart = {
      labels: Object.keys(epidemicsByType),
      values: Object.values(epidemicsByType),
      type: 'pie',
      marker: {
        colors: ['rgb(139, 92, 246)', 'rgb(236, 72, 153)', 'rgb(245, 158, 11)', 'rgb(16, 185, 129)']
      }
    };

    window.Plotly.newPlot(epidemicTypeChartRef.current, [epidemicPieChart], {
      title: 'Épidémies par type',
      margin: { t: 50, r: 50, b: 50, l: 50 }
    }, { responsive: true });
  };

  // Fonction pour créer les graphiques des vaccins
  const createVaccineCharts = (data) => {
    // Graphique à barres de l'efficacité
    const sortedByEfficacy = [...data].sort((a, b) => b.efficacy - a.efficacy);

    const vaccineBarChart = {
      x: sortedByEfficacy.map(vaccine => vaccine.name),
      y: sortedByEfficacy.map(vaccine => vaccine.efficacy),
      type: 'bar',
      marker: {
        color: 'rgb(16, 185, 129)'
      }
    };

    window.Plotly.newPlot(vaccineChartRef.current, [vaccineBarChart], {
      title: 'Efficacité des vaccins COVID-19 (%)',
      xaxis: { title: 'Vaccin' },
      yaxis: { title: 'Efficacité (%)' },
      margin: { t: 50, r: 50, b: 100, l: 80 }
    }, { responsive: true });

    // Graphique circulaire par technologie
    const vaccinesByTech = {};
    data.forEach(vaccine => {
      let tech = vaccine.technology;
      if (!tech) tech = "Non spécifié";
      if (!vaccinesByTech[tech]) {
        vaccinesByTech[tech] = 0;
      }
      vaccinesByTech[tech]++;
    });

    const vaccinePieChart = {
      labels: Object.keys(vaccinesByTech),
      values: Object.values(vaccinesByTech),
      type: 'pie',
      marker: {
        colors: ['rgb(16, 185, 129)', 'rgb(59, 130, 246)', 'rgb(245, 158, 11)', 'rgb(239, 68, 68)']
      }
    };

    window.Plotly.newPlot(vaccineTechChartRef.current, [vaccinePieChart], {
      title: 'Vaccins par technologie',
      margin: { t: 50, r: 50, b: 50, l: 50 }
    }, { responsive: true });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* En-tête */}
      <header className="bg-white shadow-md fixed w-full top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <Link
                href="/"
                className="mr-2 p-2 rounded-md text-gray-700 hover:text-blue-600 focus:outline-none"
                aria-label="Retour à l'accueil"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </Link>
              <span className="text-xl font-bold text-gray-900">Tableau de bord OMS</span>
            </div>
          </div>
        </div>
      </header>

      {/* Contenu principal */}
      <main className="pt-20 pb-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Analyses des données de santé mondiale</h1>
            <p className="mt-2 text-lg text-gray-600">
              Explorez les statistiques sur les pays, les épidémies et les vaccins
            </p>
          </div>

          {/* Onglets */}
          <div className="mb-6">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                <button
                  onClick={() => setActiveTab('countries')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'countries'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  aria-label="Voir les données des pays"
                >
                  Pays
                </button>
                <button
                  onClick={() => setActiveTab('epidemics')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'epidemics'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  aria-label="Voir les données des épidémies"
                >
                  Épidémies
                </button>
                <button
                  onClick={() => setActiveTab('vaccines')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'vaccines'
                    ? 'border-green-500 text-green-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  aria-label="Voir les données des vaccins"
                >
                  Vaccins
                </button>
              </nav>
            </div>
          </div>

          {/* Barre de recherche */}
          <div className="mb-6">
            <label htmlFor="data-search" className="sr-only">Filtrer les données</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                </svg>
              </div>
              <input
                type="text"
                name="data-search"
                id="data-search"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-600 focus:border-blue-600 sm:text-sm"
                placeholder={`Rechercher des ${activeTab === 'countries' ? 'pays' : activeTab === 'epidemics' ? 'épidémies' : 'vaccins'}...`}
                value={filterValue}
                onChange={(e) => setFilterValue(e.target.value)}
                aria-label={`Rechercher des ${activeTab === 'countries' ? 'pays' : activeTab === 'epidemics' ? 'épidémies' : 'vaccins'}`}
              />
            </div>
          </div>

          {/* Contenu des onglets */}
          {activeTab === 'countries' && (
            <div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="bg-white p-4 rounded-lg shadow">
                  <h2 className="text-lg font-semibold mb-4 text-gray-900">Top 10 des pays par population</h2>
                  <div ref={populationChartRef} className="h-80"></div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow">
                  <h2 className="text-lg font-semibold mb-4 text-gray-900">Population par continent</h2>
                  <div ref={continentPieChartRef} className="h-80"></div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4 text-gray-900">Liste des pays</h2>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pays</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Continent</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Population</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code ISO</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {getFilteredData().map((country, idx) => (
                        <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{country.name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{country.continent}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{country.population.toLocaleString()}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{country.iso3}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'epidemics' && (
            <div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="bg-white p-4 rounded-lg shadow">
                  <h2 className="text-lg font-semibold mb-4 text-gray-900">Taux de reproduction des épidémies</h2>
                  <div ref={epidemicChartRef} className="h-80"></div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow">
                  <h2 className="text-lg font-semibold mb-4 text-gray-900">Épidémies par type</h2>
                  <div ref={epidemicTypeChartRef} className="h-80"></div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4 text-gray-900">Liste des épidémies</h2>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nom</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Période</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pathogène</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Taux R0</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {getFilteredData().map((epidemic, idx) => (
                        <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{epidemic.name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{epidemic.type}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{epidemic.start_date} à {epidemic.end_date}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{epidemic.pathogen_name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{epidemic.reproduction_rate}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'vaccines' && (
            <div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="bg-white p-4 rounded-lg shadow">
                  <h2 className="text-lg font-semibold mb-4 text-gray-900">Efficacité des vaccins COVID-19</h2>
                  <div ref={vaccineChartRef} className="h-80"></div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow">
                  <h2 className="text-lg font-semibold mb-4 text-gray-900">Vaccins par technologie</h2>
                  <div ref={vaccineTechChartRef} className="h-80"></div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4 text-gray-900">Liste des vaccins</h2>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nom</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Laboratoire</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Technologie</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Posologie</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Efficacité (%)</th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Conservation</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {getFilteredData().map((vaccine, idx) => (
                        <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{vaccine.name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vaccine.laboratory}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vaccine.technology}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vaccine.dose}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vaccine.efficacy}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vaccine.storage_temperature}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Pied de page */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-400">© 2025 AnalyzeIT - Organisation Mondiale de la Santé. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}