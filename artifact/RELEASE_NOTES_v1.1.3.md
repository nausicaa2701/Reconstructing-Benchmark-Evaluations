# v1.1.3 — stable DOI and release-integrity correction

This maintenance release makes the archived artifact self-consistent by using
the stable Zenodo concept DOI throughout the files packaged in the release:
[10.5281/zenodo.21617012](https://doi.org/10.5281/zenodo.21617012).

- Updates both citation files and the artifact README to use the concept DOI.
- Updates release metadata to version `v1.1.3`.
- Regenerates `MANIFEST.json` and `MANIFEST.sha256` from the exact release tree.
- Records the SHA-256 digest of the current final paper PDF in the manifest.

No frozen cohort label, audit decision, experimental output, or reported
endpoint changes in this release.
