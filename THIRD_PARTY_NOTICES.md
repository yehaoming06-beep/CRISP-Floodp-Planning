# Third-party notices and rights boundaries

Checked on 18 November 2026. This repository does not grant a blanket open-source or open-data license. Rights in author-created code/text/results remain with their respective owners; no new license was selected on their behalf. Third-party rights and the following source conditions continue to apply.

## Hong Kong Observatory

The Government of the Hong Kong Special Administrative Region owns the applicable intellectual property rights in the HKO observations. The numerical inputs reproduce or transform data on the websites and in the publications published by the Hong Kong Observatory (HKO), including https://www.hko.gov.hk and https://www.weather.gov.hk. The official source URLs, dates, checksums and transformations are recorded in [the source access manifest](data/provenance/source_access.csv), the 23-event metadata and the final-60 inclusion/exclusion ledger.

The retained HKO material is supplied for **free-of-charge, non-commercial research under HKO's conditions**. It is not licensed for unrestricted or commercial reuse. Exact, unmodified official rights notices and conditions accompany this package:

- [Intellectual Property Rights Notice and Disclaimer](data/third_party_notices/hko/readme.htm) ([official](https://www.hko.gov.hk/en/readme/readme.htm)).
- [Website non-commercial conditions](data/third_party_notices/hko/applink.htm) ([official](https://www.hko.gov.hk/en/appweb/applink.htm)).
- [Publication non-commercial conditions](data/third_party_notices/hko/non-commercialuse.htm) ([official](https://www.hko.gov.hk/en/publica/non-commercialuse.htm)).

These are complete legal-notice pages, not weather-source archives. [Retrieval records](data/third_party_notices/hko/retrieval.json) retain their exact SHA-256. Continued redistribution must carry the applicable notices/conditions and disclaimer, preserve source attribution and accuracy, and comply with HKO's other requirements. Check the official terms for later changes; request authorization for use outside them. The permission covers government-owned material, not third-party works merely hosted by a government website.

### Official website-material disclaimer

> Disclaimer This website / publication / product / service contains information that is copied or extracted from data made available on the websites of the Hong Kong Observatory (the "Observatory") including https://www.weather.gov.hk , https://www.hko.gov.hk , and the subdomains of "weather.gov.hk" and "hko.gov.hk". The provision of the information copied or extracted from or a link to the Observatory’s websites shall not be constituted as any form of co-operation or affiliation by the Observatory with any person in relation to this website / publication / product / service or any contents herein. Nothing in this website / publication / product / service shall give rise to any representation, warranty or implication that the Observatory agrees with, approves of, recommends or endorses this website / publication / product / service. The Observatory does not have any liability, obligation or responsibility whatsoever for any loss, destruction or damages (including without limitation consequential loss, destruction or damages) howsoever arising from or in respect of your use or misuse of or reliance on or inability to use any contents herein.

### Official publication-material disclaimer

> Disclaimer This publication / website / product / service contains information that is copied or extracted from data made available in the publications of the Hong Kong Observatory (the "Observatory"). The provision of the information copied or extracted from the Observatory's publications shall not be constituted as any form of co-operation or affiliation by the Observatory with any person in relation to this publication / website / product / service or any contents herein. Nothing in this publication, the product or the service shall give rise to any representation, warranty or implication that the Observatory agrees with, approves of, recommends or endorses this publication / website / product / service. The Observatory does not have any liability, obligation or responsibility whatsoever for any loss, destruction or damages (including without limitation consequential loss, destruction or damages) howsoever arising from or in respect of your use or misuse of or reliance on or inability to use any contents herein.

## Author transformations

HKO did not prepare or endorse this research. Authors select/adjudicate event windows, transform rainfall/sea-level/surge observations, normalize and weight indicators, classify scenarios and calculate conditional sample proportions. CRITIC weights, class assignments and optimization outputs are research calculations, not HKO forecasts or annual flood probabilities. Model costs/resources/benefits include explicitly illustrative author assumptions. No measured avoided damage, protected population or field effectiveness is established.

## Withheld works

Raw HKO snapshots/PDFs are withheld from this lean package, although HKO permits certain conditional non-commercial uses. DSD/CEDD full reports and extracted pages remain local because the applicable public redistribution permission is restricted or unconfirmed. Boston guidance, unreviewed JRC copies and vendored audit helpers also remain local pending file-specific clearance. OSM may be distributed under ODbL with applicable attribution/share-alike duties; no OSM/map database is included here. Census/DATA.GOV.HK/CSDI statistics have source-specific conditional reuse permissions; the optional spatial package is not included.

See [rights and access](audit/Data_Rights_and_Access.md) for official terms by source and [the delivery report](audit/delivery_20261118/DELIVERY_REPORT.md) for the exact selected/withheld boundary. Public availability of a source URL alone is not a redistribution grant. Gurobi is separately licensed; no solver license or credentials are supplied.
