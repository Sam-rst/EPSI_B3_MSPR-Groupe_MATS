# Audit Securite - AnalyzeIT (Groupe MATS)

**Module :** Security By Design - EISI I1 SECE843
**Date :** 27 mars 2026

## Structure du dossier

```
docs/audit/
├── README.md                          # Ce fichier (index)
├── analyse/                           # Phase d'audit (matin)
│   ├── ROADMAP_AUDIT_SECURITE.md      # Plan d'audit initial
│   ├── PHASE1_ANALYSE_STATIQUE.md     # Analyse statique du code (6 constats)
│   ├── PHASE2_SUPPLY_CHAIN.md         # SonarQube, deps, Docker, CI/CD
│   ├── PHASE3_TESTS_DYNAMIQUES.md     # Tests curl, BDD, enumeration
│   └── PHASE4_SYNTHESE.md             # 8 constats, matrice risques, top 3, plan
├── remediation/                       # Phase de remediation (apres-midi)
│   └── REMEDIATION.md                 # 3 corrections, verifications, plan final
└── soutenance/                        # Supports de presentation
    ├── SOUTENANCE_AUDIT.md            # Support audit initial (6 slides)
    ├── SOUTENANCE_AUDIT_GAMMA.md      # Version Gamma de l'audit
    └── SOUTENANCE_REMEDIATION.md      # Support final 7 slides (evaluation)
```

## Resume

- **8 constats** identifies (2 critiques, 5 eleves, 1 moyen)
- **3 risques majeurs** priorises
- **3 corrections** implementees couvrant 3 natures differentes
- **8/8 actions immediates** completees
- **Verification post-correction** : 3/3 conformes
