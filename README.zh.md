# 2025-08 SDG13 Plant'X Website (可持续园艺平台)

[![Frontend: Vue.js](https://img.shields.io/badge/Frontend-Vue.js-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![AI & Data: Python](https://img.shields.io/badge/AI%20%26%20Data-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Infrastructure: AWS](https://img.shields.io/badge/Infra-AWS-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Website Status](https://img.shields.io/website?url=https%3A%2F%2Fwww.plantx.me%2F&up_message=Online&down_message=Offline&label=Live%20Demo)](https://www.plantx.me/)

> 面向澳大利亚园艺爱好者的可持续种植与生态认知平台。项目通过三次迭代逐步实现：入门引导与植物检索、病害识别与气候适配推荐、濒危物种与气候趋势可视化，以及社区联结功能。

---

## 📎 相关链接

📄 **网站链接**: https://www.plantx.me/  
📄 **英文版README**: [`README.md`](README.md)  
📑 **项目产品文档**：[Product_Document.pdf](04_handover_package/Product_Document.pdf)  
📑 **项目支持文档**：[Support_Document.pdf](04_handover_package/Support_Document.pdf)  
📑 **项目维护文档**：[Maintenance_Document.pdf](04_handover_package/Maintenance_Document.pdf) 

---

## 📌 项目简介

这个平台旨在为澳大利亚园艺爱好者提供**基于证据、可获取**的可持续种植指导，帮助用户在气候变化背景下做出更合适的种植决策，并理解个人园艺行为与更广泛环境/气候目标（SDG 13）的关联。平台在三次迭代中持续完善功能、数据与系统架构。

**核心问题**（摘）：气候变化导致降雨与温度更不稳定，很多园艺者缺乏清晰实用的指导；关键方法包括**选择适宜气候的植物**、**合理用水**、**改善土壤**、**促进生物多样性**等。平台提供工具与资源，降低试错成本，提升信心与可持续实践。

**目标人群**：有意愿采取环保种植实践的澳大利亚园艺者（从新手到资深者、家庭/社区花园），希望获取**本地化、可靠、易理解**的指导。

**Persona（示例）**：Sarah Green，46岁，维州 Caulfield 图书管理员，关注环保但在**病害识别**、**气候匹配选苗**与**获取可靠生物多样性数据**上感到困惑。平台通过**AI 病害识别**、**基于位置与天气的推荐**、**可视化生态数据**等功能，帮助她做出更明智的决策。

---

## 🔁 迭代路线与功能总览

以下按迭代列出主要 Epic 与关键用户故事/验收标准，便于快速理解项目演进。

### 迭代 1：入门引导与植物检索

* **Epic 1｜平台愿景与入门引导**：

  * 首页清晰呈现平台使命、核心功能与可持续园艺知识卡片；移动端友好。
  * 关键用户故事：

    * US 1.1/1.2/1.3：看到简介与功能卡片；点击「了解更多」可查看简单可持续实践示例（如本地原生种、水资源节约等）。
* **Epic 2｜植物探索与详情页**：

  * 多模态检索：**关键词**、**语音**、**照片**三种方式匹配植物；
  * 详情页提供**养护图标/提示**、可展开信息等，降低新手理解门槛。

### 迭代 2：病害识别、气候适配推荐与城市生态探索

* **Epic 3｜植物病害识别与解读**：

  * 病害搜索（按名称或**上传图片**获得可能匹配）；
  * 病害详情页包含**概述/症状/解决方案**；
  * **AI 预测结果**返回 Top-3 概率并支持跳转到详情。
* **Epic 4｜基于位置天气的植物推荐**：

  * 在地图上点选坐标 → 调用天气 API 聚合**未来 16 天**关键要素（温度、降雨、日照、UV、降水概率等）；
  * 将气象摘要与植物生长条件比对，生成**适配清单**；点击植物卡片进入**描述/特征/养护指南**。
* **Epic 5｜附近植物与树木（城市生物多样性）**：

  * 交互地图展示所选区域**物种密度/分布**；
  * 按名称搜索物种并**高亮出现区域/坐标**，支持科普与本地生态认知。

### 迭代 3：濒危植物分布、气候趋势影响与社区联结

* **Epic 6｜澳大利亚濒危植物分布视图**：

  * **按州筛选**并在地图上显示濒危植物标记；
  * 右侧列表与地图联动；点击卡片弹出**物种信息**。
* **Epic 7｜气候趋势与濒危植物的关系**：

  * **时间滑块**驱动的分级着色地图，比较历年跨州空间格局；
  * 州级**趋势折线图**联合展示**植物指数**与**温度/其他天气变量**的历史变化。
* **Epic 8｜社区与社群（Plant Clubs）**：

  * 列出社团**名称/联系方式/例会节奏**；
  * **按地区/州筛选**；
  * 「**今日例会**」面板自动展示当日有活动的社团（无则显示暂无）。

> 注：各 Epic 的用户故事与验收标准在迭代文档中均有详细阐述，README 仅作面向展示的提炼。

---

## 🔧 技术与实现要点（摘要）

* **云与服务**：AWS（API Gateway、Lambda、S3、CloudFront、RDS/KMS/Secrets Manager）
* **AI/ML**：基于病害图片的**图像识别**与 Top-K 预测概率可视化；
* **可视化**：交互地图（分布、分级着色与时间滑块）、联动卡片/趋势图；
* **可用性**：移动端友好、图标/提示与可展开区块，降低新手理解门槛。

---

## 🗂️ 数据与来源（按迭代汇总）

**迭代 1**（基础植物与环境）：

* Melbourne Planting Guide（特征/生长条件/生物多样性，CSV）
* Kaggle（园艺图像，JPEG/PNG）
* ALA 物种清单（CSV）
* Vic Future Climate Tool（API）

**迭代 2**（病害/天气/城市林业）：

* Perenual API（病害**描述/解决方案** & **病害图片**）→ 训练/检索
* Open-Meteo（未来 16 天天气汇总，API）→ 气候适配推荐
* City of Melbourne Urban Forest（CSV）→ 城市物种地图
* The Australian Threatened Species Index（CSV）→ 可持续实践内容增强

**迭代 3**（濒危/历史气候/边界/社团）：

* Perenual + City of Melbourne（通用+濒危植物，API/HTML → CSV）
* Open-Meteo 历史天气（API）
* ABS 州界（SHP）
* Garden Clubs of Australia（CSV）

> 注：各数据集在文档中标注对应 Epic/用户故事用途；生产库与轻量预处理格式统一为 CSV 以便前后端与可视化使用。

---

## 🧱 系统架构与安全（随迭代演进）

* **架构演进**：

  * 迭代 1：前后端通过 API Gateway 连接，算法与数据库私有连通，**后端承担较多计算**。
  * 迭代 2：转向**API 中心**与 **Serverless** 设计：API Gateway + **AWS Lambda** 承载算法，前端静态资源与对象（如病害图片）存储于 **S3**，并用 **CloudFront** 加速；数据库配合 **Secrets Manager/KMS** 加固，API 与 Lambda/S3 直连以优化数据流。
* **安全策略**：

  * 迭代 1：以网络边界为主（VPC、子网、端口白名单等）。
  * 迭代 2：转向 **API 级**安全：API Gateway **限流/配额**、Usage Plan、API Key；引入 **AWS Shield**（标准/高级）以防 DDoS；
  * 设计动因：外部直接暴露 API 后，主要风险从边界威胁转为 **接口滥用与拒绝服务**，需 API 侧针对性缓解。

---

## 👥 团队与分工

* **团队**：Spaghetti Marshmallow King（编号 TA21）
* **成员（示例）**：Zihan Yin, Yiyang Chen, Klarissa Jutivannadevi, Yu Xie, Yean Yee Tan, Weiqi Xie
* **学科与职责**：

  * **MDS**：开放数据处理（降雨/温度/物种）、建模分析，输出可操作建议（如原生耐候植物）。
  * **MIT**：架构设计与全栈开发、测试与版本控制、功能集成（检索、节水提示、社区等）。
  * **MAI**：AI 模型（病害识别、气候匹配选苗）、AI 伦理（偏见/隐私）。
  * **MBIS**：迭代规划、Persona/旅程设计、项目治理（纪要、文件、导师沟通）。

---

## 📝 版本记录（里程碑）

* **v1**：平台愿景与基础检索（迭代 1）
* **v2**：病害识别 / 天气-适配推荐 / 城市生态（迭代 2）
* **v3**：濒危分布 / 气候-物种趋势 / 社区（迭代 3）

---

## 🧭 仓库结构

```plaintext
📦2025-08-SDG13-PLANT-X-WEBSITE
├─ 📂.vscode
│  ├─ extensions.json
│  └─ settings.json
│
├─ 📂01_data_wrangling                           ⟶ 数据原始集、清洗结果与处理脚本
│  ├─ 📂01_raw_data
│  │  ├─ 📂01_species_details                    ⟶ 物种详情 JSON（大量、按编号命名）
│  │  ├─ 📂02_care_guide                         ⟶ 物种养护指南 JSON（大量）
│  │  ├─ 📂03_hardiness_map                      ⟶ 物种耐寒/分布 HTML（大量）
│  │  ├─ 📂04_plant_diseases                     ⟶ 病害 JSON（1–100+）
│  │  ├─ 📂05_thumbnail_image                    ⟶ 物种缩略图 JPG（大量）
│  │  └─ 📂06_tsx_table_vic                      ⟶ 各州/国家 TSX CSV 原始表
│  │  ├─ 01_threatened-plant-living-collection-plan.csv
│  │  ├─ 02_tsx-aggregated-data-dataset_for_vic_plants.csv
│  │  ├─ 03_TSX 2024 Data Dictionary.pdf
│  │  ├─ 04_urban-forest.csv
│  │  ├─ 05_STE_2021_AUST_SHP_GDA2020.zip           ⟶ 地理边界数据
│  │  └─ 06_tsx-aggregated-data-dataset_for_aus_plants.csv
│  ├─ 📂02_wrangled_data                         ⟶ 清洗后的主表（用于前后端/模型）
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
│  │  ├─ Table14_TSX_Table_VIC_version{1..4}.csv ⟶ TSX 省级聚合版本
│  │  ├─ Table15_StateShapeTable.csv
│  │  ├─ Table16_TSX_SpeciesMonitoringTable.csv
│  │  └─ Table17_AustralianGardenClubTable.csv
│  ├─ .cache.sqlite                              ⟶ 数据下载/清洗缓存
│  ├─ 01_download_plant_species_details_data.ipynb    ⟶ 下载物种详情数据
│  ├─ 02_download_plant_species_care_guide_data.ipynb ⟶ 下载物种养护指南
│  ├─ 03_download_plant_species_hardiness_map.ipynb   ⟶ 下载耐寒/分布地图
│  ├─ 04_download_plant_disease_data.ipynb            ⟶ 下载植物病害数据
│  ├─ 05_wrangle_for_Table06_Table07.ipynb            ⟶ 清洗表06 & 表07（受威胁物种描述/养护）
│  ├─ 06_wrangle_for_Table01_PlantMainTable.ipynb     ⟶ 清洗表01（植物主表）
│  ├─ 07_wrangle_for_Table02_GeneralPlantDescriptionTable.ipynb     ⟶ 清洗表02（通用描述）
│  ├─ 08_wrangle_for_Table03_GeneralPlantCareGuideTable.ipynb       ⟶ 清洗表03（通用养护）
│  ├─ 09_wrangle_for_Table04_GeneralPlantDistributionMapTable.ipynb ⟶ 清洗表04（分布地图）
│  ├─ 10_wrangle_for_Table05_GeneralPlantImageTable.ipynb           ⟶ 清洗表05（图像）
│  ├─ 11_wrangle_for_Table09_Table10.ipynb                          ⟶ 清洗表09 & 表10（病害及图片）
│  ├─ 12_wrangle_for_Table11_PlantDiseaseLinkTable.ipynb            ⟶ 清洗表11（病害外链）
│  ├─ 13_wrangle_for_Table12_UrbanForestTable.ipynb                 ⟶ 清洗表12（城市森林）
│  ├─ 14_wrangle_for_Table13_GeneralPlantListforRecommendation.ipynb⟶ 清洗表13（推荐用植物清单）
│  ├─ 15_wrangle_for_Table14_ThreatenedSpeciesIndexTable.ipynb      ⟶ 清洗表14（受威胁物种指数）
│  ├─ 16_wrangle_for_Table14_TSX_Table_VIC.ipynb               ⟶ 清洗表14（VIC TSX 版本）
│  ├─ 17_wrangle_for_Table15_StateShapeTable.ipynb             ⟶ 清洗表15（州界形状）
│  ├─ 18_wrangle_for_Table16_TSX_SpeciesMonitoringTable.ipynb  ⟶ 清洗表16（物种监测）
│  └─ 19_wrangle_for_Table17_AustralianGardenClubTable.ipynb   ⟶ 清洗表17（澳洲园艺俱乐部）
│
├─ 📂02_backend                                  ⟶ 复用工具与（Lambda）服务端代码
│  ├─ 📂common
│  │  ├─ config.py / db_utils.py / http_utils.py / s3_utils.py ⟶ 基础工具
│  │  └─ index.py / __init__.py
│  └─ 📂lambdas
│     ├─ 📂assets
│     │  ├─ app.py                                ⟶ 静态资源/文件处理 Lambda 入口
│     │  └─ requirements.txt
│     └─ 📂gardening_clubs
│        └─ 📂common (同上结构)                   ⟶ 园艺俱乐部相关后端共享代码
│
├─ 📂03_machine_learning_models
│  ├─ 📂01_plant_image_recognition               ⟶ 植物图像检索/识别（CLIP）
│  │  ├─ 📂clip-vit-b32                          ⟶ 分词器/预处理配置
│  │  ├─ 📂index (embeddings_fp16.npz, meta.json)⟶ 预建索引
│  │  ├─ 📂test_images                           ⟶ 测试图像样例（无需列名）
│  │  ├─ 01_plant_image_embedding.ipynb          ⟶ 向量化
│  │  ├─ 02_plant_image_query.{ipynb,py}         ⟶ 相似检索/查询
│  │  └─ requirements.txt
│  ├─ 📂02_plant_disease_recognition             ⟶ 病害分类（PyTorch）
│  │  ├─ 📂test_images                           ⟶ 测试图像样例
│  │  ├─ model.pth                               ⟶ 训练好的权重
│  │  ├─ 01_plant_disease_training.ipynb         ⟶ 训练脚本
│  │  ├─ 02_plant_disease_query.{ipynb,py}       ⟶ 推理脚本
│  │  ├─ Dockerfile / lambda_function.py         ⟶ 部署（容器 & 无服）
│  │  ├─ class_map.json / Table11_*.csv          ⟶ 类别映射与链接表
│  │  └─ requirements.txt / kaggle.json          ⟶ 依赖与数据凭据
│  ├─ 📂03_plant_recommendation_system
│  │  ├─ 01_plant_recommendation.{ipynb,py}      ⟶ 基于表13的推荐
│  │  └─ Table13.csv
│  ├─ 📂04_tsx_trend_prediction                  ⟶ TSX 趋势/可视化/后端联调
│  │  ├─ 01_tsx_trend_prediction.ipynb
│  │  ├─ 02_upload_table14_to_mysql.ipynb        ⟶ 数据入库
│  │  ├─ 03_epic7_backend_local.ipynb
│  │  ├─ 04_epic7_backend_{local,sql}.py         ⟶ 本地/SQL 版后端
│  │  ├─ Table14_TSX_Table_VIC_version{3,4}.csv
│  │  └─ Table15_StateShapeTable.csv
│  └─ 📂05_ml_workflow_description                ⟶ 模型工作流文档（中/英 + 图片）
│     ├─ 📂images (2_01.png, 4_01~4_08.png)
│     ├─ 01_plant_image_recognition_{en,zh}.{md,pdf}
│     ├─ 02_plant_disease_recognition_{en,zh}.{md,pdf}
│     └─ 03,04_*_{en,zh}.{md,pdf}
│
├─ 📂public
│  └─ weblogo.svg
│
├─ 📂src                                         ⟶ 前端（Vue + Vite）
│  ├─ 📂api
│  │  ├─ http.ts                                 ⟶ Axios/请求封装
│  │  ├─ plants.ts / plantrcmd.js                ⟶ 植物列表 & 推荐接口
│  │  ├─ pdisease.js / DiseaseUpload.js          ⟶ 病害查询/上传
│  │  ├─ climateimpact.js                        ⟶ 气候影响/TSX 接口
│  │  ├─ tpmap.js / trees.js                     ⟶ 分布/树木数据接口
│  │  └─ uploads.ts                              ⟶ 通用上传
│  ├─ 📂assets                                   ⟶ 静态图片/样式（大量）
│  │  └─ styles.css / logo.svg / …               ⟶ 关键资源
│  ├─ 📂components
│  │  ├─ 📂icons (Icon*.vue)                     ⟶ 通用图标组件
│  │  ├─ NavBar.vue / FooterBar.vue              ⟶ 全局导航/页脚
│  │  ├─ ThemeToggle.vue                         ⟶ 主题切换
│  │  ├─ PlantCard.vue / PdiseaseCard.vue        ⟶ 列表卡片
│  │  └─ CardSkeleton.vue                        ⟶ 骨架屏
│  ├─ 📂router/Router.js                         ⟶ 路由定义
│  ├─ 📂views                                    ⟶ 页面视图
│  │  ├─ HomePage.vue                            ⟶ 首页
│  │  ├─ PlantSearch.vue / PlantDetail.vue
│  │  ├─ PlantRcmd.vue                           ⟶ 植物推荐
│  │  ├─ DiseaseSearch.vue / DiseaseDetail.vue
│  │  ├─ UrbanMap.vue / UrbanThreaten.vue        ⟶ 城市森林/受威胁展示
│  │  ├─ TPmapping.vue                           ⟶ 物种分布（耐寒/地图）
│  │  ├─ ClimateImpact.vue                       ⟶ TSX/趋势影响
│  │  └─ CommunityPage.vue / GardenPage.vue
│  ├─ App.vue / main.js                          ⟶ 应用入口
│  ├─ env.d.ts                                   ⟶ TS 环境声明
│  └─ vite.config.js                             ⟶ 构建配置（前端）
│
├─ .editorconfig / .env / .gitattributes / .gitignore / .prettierrc.json
├─ dist.zip                                      ⟶ 打包产物（快照）
├─ eslint.config.js / jsconfig.json / tsconfig.json
├─ index.html                                    ⟶ 应用模板页
├─ package.json / package-lock.json              ⟶ 依赖与脚本
├─ README.md
└─ vite.config.js                                ⟶ 构建配置（根级，同名于 src 内）
```

---

## 📄 协议

本项目以 [MIT License](LICENSE) 协议分发。

---

*本项目为莫纳什大学 **FIT5120 Industry Experience Studio Project** 课程 **2025 年 S2** 实习项目；   
遵循敏捷性开放流程，共进行了 **3 次迭代**。*
