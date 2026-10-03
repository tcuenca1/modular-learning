---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

[[Ingenieria de Software II]]

# A systematic literature review of open source software quality assessment models

**Autores:** [DOCENTE], [DOCENTE], [DOCENTE], [DOCENTE], [DOCENTE]  
**Institución:** Covenant University, Ota, Nigeria; Atilim University, Ankara, Turkey; Pontificia Universidad Católica de Valparaíso, Valparaiso, Chile.

---

## Abstract
Many [[Open Source Software]] (OSS) quality assessment models are proposed and available in the literature. However, there is little or no adoption of these models in practice. In order to guide the formulation of newer models so they can be acceptable by practitioners, there is need for clear discrimination of the existing models based on their specific properties. Based on this, the aim of this study is to perform a systematic literature review to investigate the properties of the existing OSS quality assessment models by classifying them with respect to their quality characteristics, the methodology they use for assessment, and their domain of application so as to guide the formulation and development of newer models. Searches in [[IEEE Xplore]], ACM, Science Direct, Springer and Google Search is performed so as to retrieve all relevant primary studies in this regard. Journal and conference papers between the year 2003 and 2015 were considered since the first known OSS quality model emerged in 2003.

**Results:** A total of 19 OSS quality assessment model papers were selected. To select these models we have developed assessment criteria to evaluate the quality of the existing studies. Quality assessment models are classified into five categories based on the quality characteristics they possess namely: single-attribute, rounded category, community-only attribute, non-community attribute as well as the non-quality in use models. Our study reflects that software selection based on hierarchical structures is found to be the most popular selection method in the existing OSS quality assessment models. Furthermore, we found that majority (47%) of the existing models do not specify any domain of application.

**Conclusions:** In conclusion, our study will be a valuable contribution to the community and helps the quality assessment model developers in formulating newer models and also to the practitioners (software evaluators) in selecting suitable OSS in the midst of alternatives.

**Keywords:** Analysis, Community, [[ISO 25010]], [[Open Source Software]], Quality assessment models

---

## Background
Prior to the emergence of open source software (OSS) quality models, the McCall, Dromey and [[ISO 9126]] models were already in existence (Miguel et al. 2014). These models however did not consider some quality attributes unique to OSS such as community—a body of users and developers formed around OSS who contribute to the software and popularize it (Haaland et al. 2010). This gap is what led to the evolution of OSS quality models. 

Majority of the OSS quality models that exist today are derived from the [[ISO 9126]] quality model (Miguel et al. 2014; Adewumi et al. 2013). It defines six internal and external quality characteristics, which are functionality, reliability, usability, efficiency, maintainability and portability. [[ISO 25010]] replaced the [[ISO 9126]] in 2010 (ISO/IEC 9126 2001), it has the following product quality attributes (ISO/IEC 25010 2001): functional suitability, reliability, performance efficiency, operability, security, compatibility, maintainability and transferability. The [[ISO 25010]] quality in use attributes includes effectiveness, efficiency, satisfaction, safety and usability.

It is important to note that [[ISO 25010]] can serve as standard for OSS only in terms of product quality and quality in use. It does not address unique characteristics of OSS such as the community. A key distinguishing feature of OSS is that it is built and maintained by a community (Haaland et al. 2010). The quality of this community also determines the quality of the OSS (Samoladas et al. 2008). From the literature, community related quality characteristics include (Soto and Ciolkowski 2009): maintenance capacity, sustainability, and process maturity. 

- **Maintenance capacity** refers to the number of contributors to an OSS project and the amount of time they are willing and able to contribute to the development effort as observed from versioning logs, mailing lists, discussion forums and bug report systems.
- **Sustainability** refers to the ability of the community to grow in terms of new contributors and to regenerate by attracting and engaging new members to take the place of those leaving the community.
- **Process maturity** refers to the adoption and use of standard practices in the development process such as submission and review of changes, peer review of changes, provision of a test suite, and planned releases.

---

## Methods
This section outlines the research questions posed in this study and also explains in detail the rationale behind each question.

### Research Questions
- **RQ1:** What are the key quality characteristics possessed by the OSS quality assessment models?
- **RQ2:** What are the methods used by these OSS quality assessment models for selection decisions?
- **RQ3:** What is the domain of application of OSS quality assessment models?

### Search Strategy and Selection
A search string was defined based on the keywords derived from the research question as follows: `"(Open Source Software OR libre OR OSS or FLOSS or FOSS) AND (model OR quality model OR measurement model OR evaluation model)"`.

---

> **Diagrama detectado:** Distribuciones de frecuencias de las características de calidad de productos [[ISO 25010]] en modelos OSS (Fig. 1), características de calidad en uso (Fig. 2), características de calidad relacionadas con la comunidad (Fig. 3), métodos de selección usados (Fig. 4) y dominios de aplicación (Fig. 5).

---

## Results and Discussion
- **Maintainability** is measured by 55% of the existing OSS quality models making it the most common product quality characteristic.
- **Usability** is measured by 50% of the existing OSS quality models making it the most commonly measured characteristic under the quality in use category.
- **Maintenance capacity** is measured in 45% of the existing OSS quality models making it the most commonly measured attribute in the community category.
- **Model approach** (hierarchical structures) is the most common selection method used in the existing literature (32%).
- **Majority (47%)** of the existing models do not specify any domain of application.

---

## Conclusion
The overall goal of this study is to analyze and classify the existing knowledge as regards OSS quality assessment models. Papers dealing with these models were identified between 2003 and 2015. 19 papers were selected. More attention should be paid to building models that incorporate only essential quality characteristics. Also, framework, tool-based and data mining selection methods should be given more attention in future model proposals.