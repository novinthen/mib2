# MIB 2.0 Submission-Readiness Stages 1-8: Controlled Requirements

**Control status:** Stage 9 traceability reconstruction dated 2026-08-10.

## Provenance limitation

The repository did not retain the original chat prompts as files, hashes, or verbatim transcripts. Git preserves the implementation evidence through PR bodies, commits, audit records, and the final tree, but those records are not proof of the exact wording used in chat. `STAGE_TRACEABILITY_REGISTER.csv` therefore labels every requirement `reconstructed_from_preserved_evidence_not_verbatim`. No row may be represented as a verbatim prompt unless a future source artifact is committed and independently linked.

The controlled requirements below are the minimum acceptance contract recoverable from preserved evidence. The register is authoritative for requirement IDs, file evidence, verifier checks, PR numbers, head commits, merge commits, internal status, and external status.

## SR-01 - Document integrity

Reconcile authored and generated figures to the canonical registers; generate repeated financial and phase content deterministically; standardise portfolio counts; preserve the Year 2 and Year 3 gates; and detect narrative, reference, and financial drift.

**Git:** PR #2, head `cf2801d4e22fc8179ed693bb20179b13105e2654`, merge `9a87816ff3eda217d05b9f1cd66eac6e8042ee82`.

## SR-02 - Cabinet decision scope

Separate five immediate approvals, four conditional endorsements, and seven express deferrals. Keep the six-year fiscal scenario indicative. Prevent preliminary approval from creating an appropriation, reallocation, programme launch, permanent establishment, entitlement, procurement, contract, or third-party commitment.

**Git:** PR #3, head `30bf112f47f9fe3aaae7421b1160657a1c8db06c`, merge `25e58767f31a9fbfaa8139f3bd372cb2eae07822`.

## SR-03 - Validation gates

Classify all thirty validation items into five gate categories; preserve the six strict gates and four decision-dependent critical items; record ownership, evidence, deadline, escalation, financial consequence, decision links, and status; and prevent one unresolved dependency from cascading beyond its mapped decision or programme.

**Git:** PR #4, head `9e473681c914895bc61e78dd2c7e8676c9108e66`, merge `01947887080c896a91e0d0f0844b94f465e3528c`.

## SR-04 - Legal and jurisdictional clearance

Control eighteen legal issues, separated into ten pre-submission and eight programme-launch clearances. Cover every programme, preserve the six distinct PRG-04 pathways, treat current procurement commencement and transition as unresolved where official confirmation is required, and record no clearance without competent-authority evidence and an acceptance date.

**Git:** PR #5, head `535779802a01e75ef67836a8b0a8630cabb000e0`, merge `bffd003ac63251b3545e3375742343305910a79b`.

## SR-05 - Treasury validation

Control ten fiscal questions: five Phase 1 ceiling gates, four programme-cost gates, and one later-phase gate. Generate the gross Phase 1 schedule from the model, do not infer a confirmed Phase 1 financing split from six-year assumptions, and record no fiscal validation without MOF evidence and an acceptance date.

**Git:** PR #6, head `fa6e56a09a9e40c9cb8a10a208819183278457c4`, merge `dcf8d75c33b95cb01cf7cf1e08c0da3f1f8429c9`.

## SR-06 - Programme delivery designs

Maintain a complete generated implementation design for every retained programme, including authority, delivery, volume, cost, KPI, remedy, data, dependencies, and stop, redesign, and expansion tests. Reconcile service volumes to formulas and reach units. Treat every design as pending until written accounting-officer acceptance exists.

**Git:** PR #7, head `74bd4a1f6591834d8aed8eb9c3922ce2c9ff8288`, merge `eccfa9ecb391f0f1d13275ea89adf7194c861d30`.

## SR-07 - Service commitments

Control exactly seven administrative service commitments, map them only to applicable programmes, require workflow and capacity evidence before numeric deadlines, prohibit statutory and third-party outcome guarantees, and record no adoption without responsible-agency evidence and an acceptance date.

**Git:** PR #8, head `1eea7d2814a3a6c136bbf4bc658fdd7e58c3a188`, merge `b8179b7cb8597427f4c4b9e4b16851ad29248581`.

## SR-08 - Governance continuity

Control exactly eight continuity mechanisms, apply the delegated escalation spine across all sixteen retained programmes, remove personal Prime Ministerial meeting attendance as the daily operating dependency, preserve Cabinet and statutory/accounting boundaries, and record no adoption without the required instruments and dates.

**Git:** PR #9, head `df2e7e1378117a2f208288ab2282aa1dcd5fe7b7`, merge `07450be6d38e5364f7dc49eb92af175178378e0b`.

## Interpretation rule

`internally_verified` means the final repository state satisfies its machine-tested design contract. It does not mean Cabinet approval, legal clearance, Treasury validation, accounting-officer acceptance, agency adoption, implementation authority, or funding approval. External status is controlled separately in the traceability register and the Stage 9 assurance report.
