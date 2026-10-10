# Third-party data and attribution

The medical decision dataset combines selected records and annotations from upstream datasets. The repository's [MIT code license](LICENSE) does not relicense third-party text, annotations, or other source material. Adapted questions retain the corresponding source license.

The [source register](benchmarks/medical_decision_v1/SOURCES.md) provides each source's publisher, citation, license, material type, and answer provenance. Original license and citation evidence is retained under `benchmarks/medical_decision_v1/sources/`. Each sample records its source, pinned resource version, URL, SHA-256, annotation locator, and adaptation metadata.

The [release packages](releases/README.md) separate the 3,667-question open-license core from the 1,543-question noncommercial research supplement. Each package includes `LICENSE-DATA.md`, original license evidence, and a per-question `provenance.jsonl`. Attribution and share-alike obligations remain applicable where required. The research supplement includes DDI, TCM-SD, E3C, CT-EBM-SP, and CARE-Bench and retains their noncommercial restrictions.

Materials include synthetic cases, published case reports, clinical text, and examination-derived questions. Source annotations and mechanically mapped labels are not equivalent to independent clinical validation. Sources listed as reference-only contribute no question text to this dataset.

The v0.5.0 additions use MEDDOCAN (Marimon et al., 2019), PhysioNet Challenge 2019 (Reyna et al., 2019), and LabQAR (Bhasuran et al., 2026), each under CC-BY-4.0. Adaptations are token-level PHI membership, fixed-landmark outcome selection, and reference-context matching, respectively. See the [adaptation protocols](docs/GAP_AUDIT_V050.md) and original license evidence in each package.
