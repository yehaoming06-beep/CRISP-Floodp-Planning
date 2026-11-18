# V3 literature verification and integration brief

Verification date: 6 November 2026, Asia/Shanghai. This is a bounded, targeted update to the existing contribution matrix, not a systematic review. Only bibliographic titles and generic topic terms were submitted externally; manuscript text was not uploaded. No experiments were run.

## Materials and scope

Read `Methodological_Contribution_Matrix.md`, `literature/Source_Verification_Ledger.md`, `literature/Search_and_Access_Ledger.md` in `peer_review_validation_20261105_v2`, v2 Introduction/Related Work/References, and the previous `Citation_Audit.md`. The older citation audit predates the CI-01 integration: its CI-01 OPEN label and 20-reference/29-mention counts must not be presented as the current v2/v3 status or counts. Its actual reading limits remain relevant. CI-01 remains PARTIALLY RESOLVED and CI-06 remains OPEN under the later integration.

The contribution matrix correctly separates identity verification, source availability and passages actually inspected. Its P/E/H/A/U qualifiers should be retained. An inaccessible complete article is not proof of absence of a method. Obtaining HTML does not establish full-document semantic review, and no author-read declaration is inferred from this assistant's retrieval.

## Four references recommended for the main manuscript

These four references supply the requested direct flood-logistics, mobile-pump and temporary-equipment comparators. The proposed new numbers [27]–[30] leave the existing v2 [1]–[26] identities unchanged.

[27] Chang, M.-S., Tseng, Y.-L., and Chen, J.-W. (2007). A scenario planning approach for the flood emergency logistics preparation problem under uncertainty. *Transportation Research Part E: Logistics and Transportation Review*, 43(6), 737–754. [DOI](https://doi.org/10.1016/j.tre.2006.10.013).

[28] Garrido, R. A., Lamas, P., and Pino, F. J. (2015). A stochastic programming approach for floods emergency logistics. *Transportation Research Part E: Logistics and Transportation Review*, 75, 18–31. [DOI](https://doi.org/10.1016/j.tre.2014.12.002).

[29] Yosua, H., Kusuma, M. S. B., Nugroho, J., Nugroho, E. O., and Septiadi, D. (2025). Optimizing the Mobile Pump and Its Equipment to Reduce the Risk of Pluvial Flooding. *Fluids*, 10(5), 119. [DOI](https://doi.org/10.3390/fluids10050119).

[30] Lopane, F. D., and Dawson, R. J. (2026). Optimisation of Temporary and Demountable Flood Protection for Infrastructure Resilience. *Journal of Flood Risk Management*, 19(1), e70182. [DOI](https://doi.org/10.1111/jfr3.70182).

### Primary-source identity and reading check

| Matrix ID | V3 recheck and actual read scope | Supported comparison and boundary |
| --- | --- | --- |
| L01 / [27] | [Publisher article](https://www.sciencedirect.com/science/article/pii/S1366554507000178) returned 403 on direct opening. Indexed publisher preview supplied title, authors, issue/pages/DOI, abstract, introduction and section snippets. A search URL resembling a PDF supplied article-preview content, not an acquired PDF. | Flood emergency preparation with stochastic rescue demands, organization/storehouse/resource choices, capacity restrictions, GIS demand estimation and SAA is direct prior art. Exact variable domains, all equations and detailed stage assignment remain unverified. |
| L02 / [28] | [Author-institution record](https://pure.uai.cl/es/publications/a-stochastic-programming-approach-for-floods-emergency-logistics/) opened successfully: abstract, metadata and citation record. Publisher-indexed formulation/solution snippets also found. | The abstract supports supply inventories, vehicle availability, probabilistic demand satisfaction, a spatio-temporal flood process and SAA. Complete equations and exact stage-variable domains remain unverified. |
| L05 / [29] | [Publisher](https://www.mdpi.com/2311-5521/10/5/119) returned 429 directly. Publisher-indexed extended excerpts supplied author list, date/DOI, abstract, §2.1 and §3.4. This remains excerpt access. | Deployment site/access, channel deficit, pump capacity/head loss, inlet/outlet conditions and HEC-RAS configuration assessment are supported. No formal two-stage MILP was verified; figures were not independently visually inspected and numerical effectiveness is not transferred to Tai O. |
| L08 / [30] | [Published HTML](https://onlinelibrary.wiley.com/doi/full/10.1111/jfr3.70182) opened successfully: identity, abstract, §2.1–2.5 and §3.2.1–3.2.5 passages inspected. First publication: 28 January 2026. [UCL publication record](https://discovery.ucl.ac.uk/id/eprint/10225573/) corroborates identity and published-version availability. | Shared storage and deployment of temporary/demountable protection, warehouse placement and cost/time trade-offs are direct precedent. The inspected case assumes sufficient equipment and requires no new equipment purchase; do not describe it as CRISP's finite stochastic procurement model. GA convergence is not a proof of global optimality. |

## Checks on the four other matrix sources

| Matrix ID | Finding |
| --- | --- |
| L03 / existing [3] Rawls and Turnquist (2010), DOI 10.1016/j.trb.2009.08.003 | Publisher direct access again returned 403. Publisher-indexed preview/abstract remains the evidence level, consistent with the previous ledger. No upgrade to full equations or complete variable-domain verification. |
| L04 / existing [4] Mete and Zabinsky (2010), DOI 10.1016/j.ijpe.2009.10.004 | Publisher-indexed abstract/introduction retrieved. It explicitly distinguishes the preparedness two-stage SP's aggregated deliveries from the separate vehicle-loading/routing MIP. The matrix preserves this distinction correctly. |
| L06 Shehadeh and Tucker (2022), DOI 10.1016/j.trc.2022.103871 | Publisher-indexed metadata/abstract matches the [author HTML v3](https://arxiv.org/html/2012.05387v3), which opened successfully. Section headings and §8.1.2 were retrieved for the existing first-stage-fixing/out-of-sample comparison. Author-v3 access is not final-publisher-text equivalence, nor independent replication. |
| L07 Liang et al. (2025), DOI 10.5194/nhess-25-3545-2025 | [Published HTML](https://nhess.copernicus.org/articles/25/3545/2025/) opened; identity and §2.2 assumption passages checked. The matrix's richer §2.1–2.4/§3.3 audit is prior recorded reading, not repeated complete-formulation checking in this v3 pass. Do not upgrade its status on the basis of availability alone. |

The eight identities and their differentiated read scopes are supported; this pass found no reason to reject the matrix's bounded comparisons. The four selected additions are sufficient for the requested focused revision. L06/L07 need not be added merely to increase the reference count. The older `Citation_Audit.md` also retains CI-05 PARTIAL for the final-publisher comparison of Gabrel et al.; a v3 reference count closure does not close it.

## Suggested main-text integration

### Introduction contribution paragraph

CRISP is an auditable conditional case study rather than a new stochastic-programming theory or allocation algorithm. Its contribution is the explicit accounting of simultaneous pump assignments against a finite pre-event inventory, the traceable separation of event-source and tide-station sensitivities, and parallel evaluation of expected-value conventions and their optimal policy sets. Controlled component comparisons identify where these representations change the illustrative optimum and where the tested settings yield equivalent values. General two-stage planning, integer equipment procurement and shared inventory are established modelling ideas; their use here does not establish priority over previous work.

### Related Work physical resources paragraph

Mobile-pump deployment has already been examined using site accessibility, channel capacity, pump head and hydraulic simulation. Yosua et al. [29] study such factors for South Jakarta. For temporary and demountable protection, Lopane and Dawson [30] consider shared storage locations and deployment cost–time trade-offs. CRISP addresses a smaller conditional readiness-and-stock instance with abstract response scores; its results do not replace hydraulic evaluation or spatial deployment logistics.

### Related Work stochastic flood logistics paragraph

Direct flood-logistics precedents include Chang et al. [27], who formulate stochastic preparation models for rescue organization, storehouses and resource allocation, and Garrido et al. [28], who consider emergency inventories and vehicle availability under a spatio-temporal flood process. Their accessible abstracts and publisher previews establish the domain overlap, while the complete equations were not verified in this review. Together with established pre-positioning models [3,4], these studies locate CRISP's contribution in case auditability, explicit assumptions and benchmark sensitivity rather than the invention of preparedness–recourse planning.

### Discussion interpretation paragraph

The relevant advance within this case is the ability to audit how stock limits, source construction, geographic proxies and expected-value conventions affect conditional model comparisons. A zero tested difference between shared and duplicated inventory, or structural equivalence after relaxing procurement integrality, limits the observed contribution of those components in this instance. It does not show that shared-stock accounting is unnecessary generally, and none of the RP changes estimates real avoided damage.

## Editorial actions and limits

- Preserve the v2 references' identities and append the four additions; verify all in-text numbers and reference closure after editing.
- Do not use “first”, “only”, “no prior work”, new generic SP theory, or new shared/integer inventory as contribution claims. This targeted search does not establish global novelty for EV-tie ranges either.
- Keep source/read-depth details in the supplement or audit rather than expanding the literature section into access-history narration.
- The proposed paragraphs summarize verified content in new wording. No quotations, calibrated Tai O coefficients, claims about author reading, or cross-study numerical ranking are introduced.
