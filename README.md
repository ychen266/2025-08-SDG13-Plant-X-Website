# 2025-08 SDG13 Plant'X Website (Sustainable Gardening Platform)

[![Frontend: Vue.js](https://img.shields.io/badge/Frontend-Vue.js-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![AI & Data: Python](https://img.shields.io/badge/AI%20%26%20Data-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Infrastructure: AWS](https://img.shields.io/badge/Infra-AWS-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Website Status](https://img.shields.io/website?url=https%3A%2F%2Fwww.plantx.me%2F&up_message=Online&down_message=Offline&label=Live%20Demo)](https://www.plantx.me/)

> A sustainable planting and ecological awareness platform for Australian gardening enthusiasts. The project was delivered over three iterations: onboarding & plant search, disease identification & climate-fit recommendations, endangered species & climate-trend visualizations, plus community connection features.
---

## 📎 Links

📄 **Website URL**: https://www.plantx.me/  
📄 **中文版README**: [`README.zh.md`](README.zh.md)  
📑 **Product Document**: [Product_Document.pdf](04_handover_package/Product_Document.pdf)  
📑 **Support Document**: [Support_Document.pdf](04_handover_package/Support_Document.pdf)  
📑 **Maintenance Document**: [Maintenance_Document.pdf](04_handover_package/Maintenance_Document.pdf)

---

## 📌 Project Overview

This platform provides **evidence-based and accessible** sustainable gardening guidance for Australian gardeners. It helps users make better planting decisions under climate change and understand how personal gardening practices connect to broader environmental and climate goals (SDG 13). Features, data, and system architecture are refined across three iterations.

**Core problem** (excerpt): Climate change makes rainfall and temperature more volatile, and many gardeners lack clear, practical guidance. Key strategies include **choosing climate-appropriate species**, **efficient water use**, **improving soil**, and **supporting biodiversity**. The platform offers tools and resources to reduce trial-and-error costs and boost confidence in sustainable practices.

**Target users**: Australian gardeners (from beginners to advanced users, home or community gardens) who want **localized, reliable, and easy-to-understand** guidance for environmentally friendly planting.

**Persona (example)**: Sarah Green, 46, librarian in Caulfield, Victoria. She cares about the environment but struggles with **disease identification**, **climate-matched plant selection**, and **accessing trustworthy biodiversity data**. The platform helps via **AI disease recognition**, **location- & weather-based recommendations**, and **visualizing ecological data**.

---

## 🔁 Iteration Roadmap & Feature Overview

The main Epics and key user stories/acceptance criteria by iteration are summarized below for a quick understanding of project evolution.

### Iteration 1: Onboarding & Plant Search

* **Epic 1 | Vision & Onboarding**:
  * A homepage clearly communicates the mission, core features, and sustainable gardening “knowledge cards”; mobile-friendly.
  * Key user stories:
    * US 1.1/1.2/1.3: View intro & feature cards; click “Learn more” to see simple sustainable practice examples (e.g., local natives, water-saving).

* **Epic 2 | Plant Exploration & Details**:
  * Multimodal search: **keyword**, **voice**, and **photo** matching.
  * Details page with **care icons/tips** and expandable sections to lower the learning curve for beginners.

### Iteration 2: Disease Identification, Climate-Fit Recommendations & Urban Ecology

* **Epic 3 | Plant Disease Recognition & Interpretation**:
  * Disease search (by name or **uploading an image** for likely matches).
  * Disease details include **overview/symptoms/solutions**.
  * **AI predictions** return Top-3 probabilities with links to details.

* **Epic 4 | Location & Weather-Based Plant Recommendations**:
  * Pick a coordinate on the map → call weather API to aggregate **next 16 days** of key variables (temperature, rainfall, sunshine, UV, precipitation probability, etc.).
  * Compare the weather summary against plant growth conditions to generate an **adaptation list**; click a plant card to view **description/features/care guide**.

* **Epic 5 | Nearby Plants & Trees (Urban Biodiversity)**:
  * Interactive map shows **species density/distribution** in the selected area.
  * Search by species name and **highlight occurrence regions/coordinates** to support local ecological literacy.

### Iteration 3: Threatened Species, Climate Trends & Community

* **Epic 6 | Australian Threatened Plants Distribution**:
  * **Filter by state** and display threatened plant markers on the map.
  * Right-side list is linked to the map; clicking a card opens **species info**.

* **Epic 7 | Climate Trends vs. Threatened Plants**:
  * A **time slider** drives a choropleth map to compare interannual state-level spatial patterns.
  * State-level **trend lines** jointly visualize the **species index** and **temperature/other weather variables** over time.

* **Epic 8 | Community & Plant Clubs**:
  * List club **names/contacts/meeting cadence**.
  * **Filter by region/state**.
  * A **“Today’s Meetings”** panel automatically shows clubs with activities today (or “None” if no events).

> Note: Detailed user stories and acceptance criteria for each Epic are documented in the iteration documents; this README provides a showcase-oriented summary.

---

## 🔧 Technology & Implementation Highlights (Summary)

* **Cloud & Services**: AWS (API Gateway, Lambda, S3, CloudFront, RDS/KMS/Secrets Manager)
* **AI/ML**: **Image-based disease recognition** with Top-K probability visualization
* **Visualization**: Interactive maps (distribution, choropleth with time slider), linked cards & trend charts
* **Usability**: Mobile-friendly; icons/tips and expandable sections to ease onboarding

---

## 🗂️ Data & Sources (by Iteration)

**Iteration 1** (baseline plants & environment):
* Melbourne Planting Guide (traits/growth conditions/biodiversity, CSV)
* Kaggle (gardening images, JPEG/PNG)
* ALA species list (CSV)
* Vic Future Climate Tool (API)

**Iteration 2** (disease/weather/urban forestry):
* Perenual API (disease **descriptions/solutions** & **images**) → training/retrieval
* Open-Meteo (16-day forecast, API) → climate-fit recommendations
* City of Melbourne Urban Forest (CSV) → urban species map
* The Australian Threatened Species Index (CSV) → enrich sustainable-practice content

**Iteration 3** (threatened/historical climate/boundaries/clubs):
* Perenual + City of Melbourne (general + threatened plants, API/HTML → CSV)
* Open-Meteo historical weather (API)
* ABS state boundaries (SHP)
* Garden Clubs of Australia (CSV)

> Note: Each dataset is annotated in the docs with its Epic/user-story usage. Production tables and light preprocessing outputs are standardized to CSV for frontend/backend and visualization.

---

## 🧱 Architecture & Security (evolving with iterations)

* **Architecture evolution**:
  * Iteration 1: Frontend–backend connected via API Gateway; algorithms and database on private networks; the **backend performs more computation**.
  * Iteration 2: Shift to **API-centric** and **serverless** design: API Gateway + **AWS Lambda** for algorithms; frontend static assets and objects (e.g., disease images) in **S3**, accelerated by **CloudFront**; database hardened with **Secrets Manager/KMS**; APIs connect directly with Lambda/S3 to optimize data flow.

* **Security strategy**:
  * Iteration 1: Perimeter-focused (VPC, subnets, port allowlists, etc.).
  * Iteration 2: **API-level** security: API Gateway **rate limiting/quotas**, usage plans, API keys; **AWS Shield** (Standard/Advanced) for DDoS mitigation.
  * Rationale: Once APIs are exposed externally, the primary risks shift from perimeter threats to **interface abuse and denial of service**, requiring API-side mitigations.

---

## 👥 Team & Roles

* **Team**: Spaghetti Marshmallow King (ID TA21)
* **Members (example)**: Zihan Yin, Yiyang Chen, Klarissa Jutivannadevi, Yu Xie, Yean Yee Tan, Weiqi Xie
* **Disciplines & responsibilities**:
  * **MDS**: Open data processing (rainfall/temperature/species), modeling & analysis; actionable insights (e.g., native weather-resilient plants)
  * **MIT**: Architecture & full-stack development, testing & version control, feature integration (search, water-saving tips, community, etc.)
  * **MAI**: AI models (disease recognition, climate-matched plant selection), AI ethics (bias/privacy)
  * **MBIS**: Iteration planning, persona/journey design, project governance (minutes, docs, supervisor comms)

---

## 📝 Version History (Milestones)

* **v1**: Vision & basic retrieval (Iteration 1)
* **v2**: Disease recognition / weather-fit recommendations / urban ecology (Iteration 2)
* **v3**: Threatened distribution / climate–species trends / community (Iteration 3)

---

## 🧭 Repository Structure

```plaintext
📦2025-08-SDG13-PLANT-X-WEBSITE
├─ 📂.vscode
│  ├─ extensions.json
│  └─ settings.json
│
├─ 📂01_data_wrangling                           ⟶ Raw datasets, cleaned outputs & processing scripts
│  ├─ 📂01_raw_data
│  │  ├─ 📂01_species_details                    ⟶ Species detail JSON (large, numeric filenames)
│  │  ├─ 📂02_care_guide                         ⟶ Species care guide JSON (large)
│  │  ├─ 📂03_hardiness_map                      ⟶ Species hardiness/distribution HTML (large)
│  │  ├─ 📂04_plant_diseases                     ⟶ Disease JSON (1–100+)
│  │  ├─ 📂05_thumbnail_image                    ⟶ Species thumbnails JPG (large)
│  │  └─ 📂06_tsx_table_vic                      ⟶ State/national TSX CSV raw tables
│  │  ├─ 01_threatened-plant-living-collection-plan.csv
│  │  ├─ 02_tsx-aggregated-data-dataset_for_vic_plants.csv
│  │  ├─ 03_TSX 2024 Data Dictionary.pdf
│  │  ├─ 04_urban-forest.csv
│  │  ├─ 05_STE_2021_AUST_SHP_GDA2020.zip           ⟶ Geospatial boundary data
│  │  └─ 06_tsx-aggregated-data-dataset_for_aus_plants.csv
│  ├─ 📂02_wrangled_data                         ⟶ Cleaned master tables (for FE/BE/models)
│  │  ├─ Table01_PlantMainTable.csv
│  │  ├─ Table02_GeneralPlantDescriptionTable.csv
│  │  ├─ Table03_GeneralPlantCareGuideTable.csv
│  │  ├─ Table04_GeneralPlantDistributionMapTable.csv
│  │  ├─ Table05_GeneralPlantImageTable.csv
│  │  ├─ Table06_ThreatenedPlantDescriptionTable.csv
│  │  ├─ Table07_ThreatenedPlantCareGuideTable.csv
│  │  ├─ Table09_PlantDiseaseTable.csv
│  │  ├─ Table10_PlantDiseaseImageTable.csv
│  │  ├─ Table11_PlantDiseaseLinkTable.csv
│  │  ├─ Table12_UrbanForestTable.csv
│  │  ├─ Table13_GeneralPlantListforRecommendation.csv
│  │  ├─ Table14_TSX_Table_VIC_version{1..4}.csv ⟶ TSX state-level aggregated versions
│  │  ├─ Table15_StateShapeTable.csv
│  │  ├─ Table16_TSX_SpeciesMonitoringTable.csv
│  │  └─ Table17_AustralianGardenClubTable.csv
│  ├─ .cache.sqlite                              ⟶ Cache for downloads/cleaning
│  ├─ 01_download_plant_species_details_data.ipynb    ⟶ Download species details
│  ├─ 02_download_plant_species_care_guide_data.ipynb ⟶ Download species care guides
│  ├─ 03_download_plant_species_hardiness_map.ipynb   ⟶ Download hardiness/distribution maps
│  ├─ 04_download_plant_disease_data.ipynb            ⟶ Download plant disease data
│  ├─ 05_wrangle_for_Table06_Table07.ipynb            ⟶ Clean Tables 06 & 07 (threatened species desc/care)
│  ├─ 06_wrangle_for_Table01_PlantMainTable.ipynb     ⟶ Clean Table 01 (plant main)
│  ├─ 07_wrangle_for_Table02_GeneralPlantDescriptionTable.ipynb     ⟶ Clean Table 02 (general description)
│  ├─ 08_wrangle_for_Table03_GeneralPlantCareGuideTable.ipynb       ⟶ Clean Table 03 (general care)
│  ├─ 09_wrangle_for_Table04_GeneralPlantDistributionMapTable.ipynb ⟶ Clean Table 04 (distribution map)
│  ├─ 10_wrangle_for_Table05_GeneralPlantImageTable.ipynb           ⟶ Clean Table 05 (images)
│  ├─ 11_wrangle_for_Table09_Table10.ipynb                          ⟶ Clean Tables 09 & 10 (diseases & images)
│  ├─ 12_wrangle_for_Table11_PlantDiseaseLinkTable.ipynb            ⟶ Clean Table 11 (external links)
│  ├─ 13_wrangle_for_Table12_UrbanForestTable.ipynb                 ⟶ Clean Table 12 (urban forest)
│  ├─ 14_wrangle_for_Table13_GeneralPlantListforRecommendation.ipynb⟶ Clean Table 13 (rec list)
│  ├─ 15_wrangle_for_Table14_ThreatenedSpeciesIndexTable.ipynb      ⟶ Clean Table 14 (threatened species index)
│  ├─ 16_wrangle_for_Table14_TSX_Table_VIC.ipynb               ⟶ Clean Table 14 (VIC TSX version)
│  ├─ 17_wrangle_for_Table15_StateShapeTable.ipynb             ⟶ Clean Table 15 (state shapes)
│  ├─ 18_wrangle_for_Table16_TSX_SpeciesMonitoringTable.ipynb  ⟶ Clean Table 16 (species monitoring)
│  └─ 19_wrangle_for_Table17_AustralianGardenClubTable.ipynb   ⟶ Clean Table 17 (AU garden clubs)
│
├─ 📂02_backend                                  ⟶ Shared utilities & (Lambda) backend code
│  ├─ 📂common
│  │  ├─ config.py / db_utils.py / http_utils.py / s3_utils.py ⟶ Base utilities
│  │  └─ index.py / __init__.py
│  └─ 📂lambdas
│     ├─ 📂assets
│     │  ├─ app.py                                ⟶ Lambda entry for static assets/files
│     │  └─ requirements.txt
│     └─ 📂gardening_clubs
│        └─ 📂common (same structure)             ⟶ Backend shared code for garden clubs
│
├─ 📂03_machine_learning_models
│  ├─ 📂01_plant_image_recognition               ⟶ Plant image retrieval/recognition (CLIP)
│  │  ├─ 📂clip-vit-b32                          ⟶ Tokenizer/preprocess configs
│  │  ├─ 📂index (embeddings_fp16.npz, meta.json)⟶ Prebuilt index
│  │  ├─ 📂test_images                           ⟶ Sample test images
│  │  ├─ 01_plant_image_embedding.ipynb          ⟶ Embedding
│  │  ├─ 02_plant_image_query.{ipynb,py}         ⟶ Similarity search/query
│  │  └─ requirements.txt
│  ├─ 📂02_plant_disease_recognition             ⟶ Disease classification (PyTorch)
│  │  ├─ 📂test_images                           ⟶ Sample test images
│  │  ├─ model.pth                               ⟶ Trained weights
│  │  ├─ 01_plant_disease_training.ipynb         ⟶ Training script
│  │  ├─ 02_plant_disease_query.{ipynb,py}       ⟶ Inference scripts
│  │  ├─ Dockerfile / lambda_function.py         ⟶ Deployment (container & serverless)
│  │  ├─ class_map.json / Table11_*.csv          ⟶ Class mapping & link tables
│  │  └─ requirements.txt / kaggle.json          ⟶ Dependencies & data credentials
│  ├─ 📂03_plant_recommendation_system
│  │  ├─ 01_plant_recommendation.{ipynb,py}      ⟶ Recommendations based on Table 13
│  │  └─ Table13.csv
│  ├─ 📂04_tsx_trend_prediction                  ⟶ TSX trends/visualization/backend integration
│  │  ├─ 01_tsx_trend_prediction.ipynb
│  │  ├─ 02_upload_table14_to_mysql.ipynb        ⟶ Data ingest
│  │  ├─ 03_epic7_backend_local.ipynb
│  │  ├─ 04_epic7_backend_{local,sql}.py         ⟶ Local/SQL backends
│  │  ├─ Table14_TSX_Table_VIC_version{3,4}.csv
│  │  └─ Table15_StateShapeTable.csv
│  └─ 📂05_ml_workflow_description                ⟶ ML workflow docs (EN/ZH + images)
│     ├─ 📂images (2_01.png, 4_01~4_08.png)
│     ├─ 01_plant_image_recognition_{en,zh}.{md,pdf}
│     ├─ 02_plant_disease_recognition_{en,zh}.{md,pdf}
│     └─ 03,04_*_{en,zh}.{md,pdf}
│
├─ 📂public
│  └─ weblogo.svg
│
├─ 📂src                                         ⟶ Frontend (Vue + Vite)
│  ├─ 📂api
│  │  ├─ http.ts                                 ⟶ Axios/request wrapper
│  │  ├─ plants.ts / plantrcmd.js                ⟶ Plant list & recommendation APIs
│  │  ├─ pdisease.js / DiseaseUpload.js          ⟶ Disease search/upload
│  │  ├─ climateimpact.js                        ⟶ Climate impact/TSX
│  │  ├─ tpmap.js / trees.js                     ⟶ Distribution/tree data APIs
│  │  └─ uploads.ts                              ⟶ Generic upload
│  ├─ 📂assets                                   ⟶ Static images/styles (many)
│  │  └─ styles.css / logo.svg / …               ⟶ Key assets
│  ├─ 📂components
│  │  ├─ 📂icons (Icon*.vue)                     ⟶ Reusable icon components
│  │  ├─ NavBar.vue / FooterBar.vue              ⟶ Global nav/footer
│  │  ├─ ThemeToggle.vue                         ⟶ Theme switch
│  │  ├─ PlantCard.vue / PdiseaseCard.vue        ⟶ List cards
│  │  └─ CardSkeleton.vue                        ⟶ Skeleton loader
│  ├─ 📂router/Router.js                         ⟶ Routes
│  ├─ 📂views                                    ⟶ Pages
│  │  ├─ HomePage.vue                            ⟶ Home
│  │  ├─ PlantSearch.vue / PlantDetail.vue
│  │  ├─ PlantRcmd.vue                           ⟶ Plant recommendations
│  │  ├─ DiseaseSearch.vue / DiseaseDetail.vue
│  │  ├─ UrbanMap.vue / UrbanThreaten.vue        ⟶ Urban forest/threatened views
│  │  ├─ TPmapping.vue                           ⟶ Species distribution (hardiness/map)
│  │  ├─ ClimateImpact.vue                       ⟶ TSX/trend impact
│  │  └─ CommunityPage.vue / GardenPage.vue
│  ├─ App.vue / main.js                          ⟶ App entry
│  ├─ env.d.ts                                   ⟶ TS env declarations
│  └─ vite.config.js                             ⟶ Frontend build config
│
├─ .editorconfig / .env / .gitattributes / .gitignore / .prettierrc.json
├─ dist.zip                                      ⟶ Build artifacts (snapshot)
├─ eslint.config.js / jsconfig.json / tsconfig.json
├─ index.html                                    ⟶ App template
├─ package.json / package-lock.json              ⟶ Dependencies & scripts
├─ README.md
└─ vite.config.js                                ⟶ Root build config (same name as in src)
```

## 📄 License

Distributed under the [MIT License](LICENSE).

---

*This project is part of Monash University’s **FIT5120 Industry Experience Studio Project**, **Semester 2, 2025**;     
Delivered via an agile, open process across **three iterations**.*
