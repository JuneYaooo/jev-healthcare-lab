# Data and upstream projects

The `scenarios/` archive contains the exact evaluated subsets: input text, gold labels, adapted Jev questions, cached responses, and experiment metadata. The ASR task also includes its original acted-patient audio and transcripts; the OCR task includes the six selected scans and texts. These are experiment subsets, not complete upstream datasets.

Source links and adaptation scope are recorded in each task's README and provenance.json, and in results/medical_catalog.json. Dataset texts, annotations, media, upstream code and provider outputs remain subject to their original rights and access conditions; the repository's MIT code license does not relicense them. In particular, research-only/noncommercial source restrictions remain applicable, including TCM-SD's CC BY-NC-SA 4.0 conditions noted in the original adapter.

Credentials, model weights, unrelated media-domain experiments and unselected source corpora are not included. Public benchmark and acted/synthetic records are not newly collected patient data. Adapted task metrics are not official leaderboard submissions; closed-model training exposure is unknown.
