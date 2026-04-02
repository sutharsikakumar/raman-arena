# Tungsten Diselenide (WSe₂) ELO Ranking — Final Report

**Sample:** wse2_mono_sio2_001 (Monolayer WSe₂ on SiO₂/Si)  
**Judge:** grok-4.20-0309-reasoning  
**ELO range:** 0.0–100.0 · Start: 50.0 · K=16  
**Total games played:** 36  

## Ground Truth
```
GROUND TRUTH — Tungsten Diselenide Sample (wse2_mono_sio2_001)
===============================================================
Sample type       : Monolayer WSe₂ grown by CVD or mechanically exfoliated,
                   on SiO₂/Si substrate; crystallographic orientation 001
Abbreviation      : wse2_mono_sio2_001

Expected Raman signature
  E¹₂g band (~250 cm⁻¹)      : In-plane W–Se stretching mode. In monolayer WSe₂
                               this mode is nearly degenerate with the A₁g mode,
                               making them difficult to resolve without high-
                               resolution spectroscopy.
  A₁g  band (~250–252 cm⁻¹)  : Out-of-plane Se–W–Se symmetric breathing mode.
                               Nearly overlaps with E¹₂g in monolayer — the two
                               peaks merge into a single broad feature or show
                               a slight asymmetry around 250 cm⁻¹.
  2LA(M) band (~260 cm⁻¹)    : Second-order longitudinal acoustic mode at the
                               M point; STRONGLY enhanced in monolayer WSe₂ and
                               is a key monolayer indicator. Often the dominant
                               or co-dominant peak in monolayer spectra.
  B¹₂g  band (~308 cm⁻¹)     : IR-active out-of-plane mode that becomes weakly
                               Raman-active in few-layer / bulk; its ABSENCE or
                               extreme weakness confirms monolayer character.
  Defect / disorder bands     : Broad features or additional peaks indicate
                               Se vacancies or grain-boundary disorder; should
                               be absent in high-quality monolayer.

Key quality indicators
  • Dominant feature near ~250 cm⁻¹ (merged E¹₂g / A₁g)
  • Strong 2LA(M) peak at ~260 cm⁻¹; I(2LA)/I(A₁g) ≥ 1 typical for monolayer
  • Absence or near-absence of B¹₂g at ~308 cm⁻¹ → confirms monolayer
  • Sharp lineshapes (FWHM ≈ 5–10 cm⁻¹ for main peak)
  • No WO₃ oxidation peak near ~800 cm⁻¹ → no surface degradation
  • Distinguishable from MoSe₂ (~240 cm⁻¹ A₁g) and WS₂ (~350 cm⁻¹ / ~420 cm⁻¹)
    by peak positions

Classification target : TUNGSTEN DISELENIDE (WSe₂), monolayer
Substrate            : SiO₂/Si, orientation 001
```

## Final Rankings

| Rank | Model | ELO | W | D | L | Win% |
|------|-------|-----|---|---|---|------|
| 1 | **e** | 100.0 | 7 | 1 | 0 | 94% |
| 2 | **f** | 99.5 | 7 | 1 | 0 | 94% |
| 3 | **d** | 57.9 | 3 | 3 | 2 | 56% |
| 4 | **c** | 51.1 | 2 | 4 | 2 | 50% |
| 5 | **b** | 43.9 | 2 | 3 | 3 | 44% |
| 6 | **i** | 43.5 | 2 | 3 | 3 | 44% |
| 7 | **a** | 35.3 | 0 | 6 | 2 | 38% |
| 8 | **h** | 13.1 | 0 | 3 | 5 | 19% |
| 9 | **g** | 5.2 | 0 | 2 | 6 | 12% |

## Match Results

- **Game 1** · a vs b → **draw** wins (conf=0.85)  
  *Both models are equally incorrect on material identification, key peak assignment, monolayer diagnostics, and overall reasoning grounded in WSe₂ physics. Their structured outputs are comparable in format but neither engages with the ground-truth spectrum characteristics.*

- **Game 2** · a vs c → **draw** wins (conf=0.95)  
  *Both models are equally poor: zero overlap with ground-truth WSe₂ features, no use of 2LA(M) enhancement or B¹₂g suppression, and confident misidentification of unrelated materials. Neither is closer to correct than the other.*

- **Game 3** · a vs d → **draw** wins (conf=0.95)  
  *Neither candidate shows any scientific correctness, reasoning grounded in WSe₂ Raman signatures, or completeness on the required classification elements. They are equally erroneous overall, with A hallucinating graphite features and B latching onto the substrate Si peak while both ignore the ~250-260 cm⁻¹ region that defines monolayer WSe₂.*

- **Game 4** · a vs e → **e** wins (conf=0.88)  
  *A fails at the most basic step by assigning the wrong material class; B correctly identifies WSe₂ and several of its characteristic modes even though the layer number is off. B is therefore the better overall output by a wide margin.*

- **Game 5** · a vs f → **f** wins (conf=0.88)  
  *B is the only candidate that recognizes the material as WSe₂ and correctly assigns the primary low-frequency modes; A is a complete misclassification. Although B errs on layer number, it is vastly superior in scientific relevance, reasoning, and completeness relative to the WSe₂ ground truth.*

- **Game 6** · a vs g → **draw** wins (conf=0.90)  
  *Both are equally wrong on material, layer number, and all key Raman signatures of monolayer WSe₂. Their chains of thought show no engagement with TMD Raman physics or the provided ground-truth features, making them indistinguishable in failure.*

- **Game 7** · a vs h → **draw** wins (conf=0.90)  
  *Both candidates are equally invalid with zero overlap to ground-truth WSe₂ monolayer signatures. A and B hallucinate unrelated materials and peak interpretations, failing all three evaluation dimensions identically.*

- **Game 8** · a vs i → **draw** wins (conf=0.90)  
  *Both models failed every evaluation dimension by misclassifying the spectrum as unrelated materials and showing zero engagement with WSe₂ Raman signatures or monolayer diagnostics. They are equally poor in scientific correctness, reasoning quality, and completeness relative to the provided ground truth.*

- **Game 9** · b vs c → **draw** wins (conf=0.90)  
  *Neither model identified WSe₂ or used any of its Raman signatures/monolayer diagnostics from the ground truth. Their errors in material assignment, peak interpretation, and omission of all relevant TMD criteria are equivalent, justifying a draw.*

- **Game 10** · b vs d → **d** wins (conf=0.75)  
  *B is superior overall for correctly identifying the Si substrate peak at ~518 cm⁻¹ and recognizing the ~249 cm⁻¹ peak as atypical, which aligns with the dominant WSe₂ monolayer feature, whereas A hallucinates an elemental sulfur spectrum. Neither candidate references the merged E¹₂g/A₁g, strong 2LA(M), B¹₂g absence, or monolayer criteria, but B's partial substrate awareness makes it less erroneous.*

- **Game 11** · b vs e → **e** wins (conf=0.82)  
  *B is superior on every dimension: it identifies the correct material, recognizes the characteristic merged E²g/A₁g mode and substrate Si peak, and offers physically grounded layer reasoning, whereas A hallucinates an unrelated sulfur spectrum. The layer-number mismatch in B is a flaw but far less severe than A's total misidentification.*

- **Game 12** · b vs f → **f** wins (conf=0.85)  
  *A hallucinates an unrelated material (sulfur) with zero overlap to the GT WSe₂ monolayer signature. B correctly identifies WSe₂, accounts for instrumental offset, and uses the correct Raman modes for analysis, only erring on layer number. This makes B far superior overall despite the layer discrepancy.*

- **Game 13** · b vs g → **b** wins (conf=0.70)  
  *Neither output is scientifically correct on material or monolayer identification. A is better overall due to more thorough, less contradictory reasoning that engages the actual dominant ~248 cm⁻¹ peak and evaluates alternatives, whereas B's analysis is superficial, inconsistent with peak prominence, and ignores most spectral features.*

- **Game 14** · b vs h → **b** wins (conf=0.85)  
  *Neither output is scientifically correct for WSe₂, but A is clearly superior: it examines the correct spectral window, dismisses noise properly, and considers related materials. B's ice assignment is wholly disconnected from the problem domain and ground truth.*

- **Game 15** · b vs i → **draw** wins (conf=0.90)  
  *Both models show identical core errors in material identification, total absence of WSe₂-specific Raman analysis, and equivalent reasoning quality. No meaningful difference exists across scientific correctness, chain-of-thought, or output completeness.*

- **Game 16** · c vs d → **draw** wins (conf=0.75)  
  *Both models are equally incorrect on material, monolayer indicators, and Raman physics for WSe₂; neither is closer to ground truth. B notes the Si peak correctly but this does not outweigh the total absence of TMD reasoning in either output.*

- **Game 17** · c vs e → **e** wins (conf=0.85)  
  *B is substantially better overall as it correctly recognizes WSe₂, the dominant ~250 cm⁻¹ feature, and substrate Si peak using appropriate TMD Raman knowledge, while A misidentifies the material entirely as HgS. The layer-number error in B is notable but does not outweigh A's total failure on material identification and reasoning.*

- **Game 18** · c vs f → **f** wins (conf=0.88)  
  *A completely fails by assigning the spectrum to cinnabar instead of WSe₂ and ignores all 2D-material Raman signatures. B correctly identifies the material, correctly interprets the dominant ~250 cm⁻¹ band and Si substrate, and only errs on layer number; its chain-of-thought is solidly grounded in TMD spectroscopy and therefore superior on every evaluated dimension.*

- **Game 19** · c vs g → **c** wins (conf=0.75)  
  *A is better overall due to correctly noting the dominant 247 cm⁻¹ peak, acknowledging the complex mixed spectrum with PL, and using lower appropriate confidence. B is overconfident, internally inconsistent, and dismisses key low-wavenumber features. Both are scientifically incorrect on material and monolayer identification.*

- **Game 20** · c vs h → **c** wins (conf=0.85)  
  *Neither output is scientifically correct for WSe₂, but A is superior overall: it correctly flags the Si substrate peak at 518 cm⁻¹ and assigns the dominant low-wavenumber mode to a plausible (if wrong) inorganic phase, while B's ice interpretation is physically incompatible with the observed lattice peaks and the known 2D-material context. A's chain-of-thought is more rigorous and less hallucinatory.*

- **Game 21** · c vs i → **draw** wins (conf=0.85)  
  *Neither candidate identified WSe₂ or used any of its Raman diagnostics; both are equally incorrect on every evaluation axis.*

- **Game 22** · d vs e → **e** wins (conf=0.82)  
  *B is the clear winner because it correctly identifies the material as WSe₂ and assigns the primary ~250 cm⁻¹ feature, while A misses the TMD entirely and focuses only on the substrate. Although B incorrectly labels the sample few-layer and omits the 2LA(M) indicator, its reasoning is grounded in actual WSe₂ physics and is far closer to the ground-truth reference than A's silicon-only analysis.*

- **Game 23** · d vs f → **f** wins (conf=0.82)  
  *B correctly identifies WSe₂, handles substrate/calibration, and uses appropriate mode assignments, while A entirely misses the material and treats the main WSe₂ peak as an anomaly. Although B errs on layer number, its overall scientific grounding and completeness far exceed A's total misclassification.*

- **Game 24** · d vs g → **d** wins (conf=0.75)  
  *Both are scientifically wrong on material identification and ignore all ground-truth WSe₂ signatures. A is marginally better because its chain-of-thought explicitly acknowledges the strong 249 cm⁻¹ peak and spectral complexity (the actual WSe₂ features), whereas B is overconfident and factually inconsistent with its own peak list.*

- **Game 25** · d vs h → **draw** wins (conf=0.90)  
  *Both models are equally poor: zero overlap with ground-truth WSe₂ identification, monolayer diagnostics, or correct peak assignments. A at least recognizes the substrate Si peak, but this does not salvage the total misclassification; B is wholly delusional. Draw on every evaluation dimension.*

- **Game 26** · d vs i → **d** wins (conf=0.75)  
  *A is better overall for correctly detecting the dominant Si substrate peak and flagging the 249 cm⁻¹ band as anomalous (actually the WSe₂ signature), while B's sulfur assignment is wholly erroneous and ignores the Si feature. Both miss the ground-truth WSe₂ monolayer classification.*

- **Game 27** · e vs f → **draw** wins (conf=0.75)  
  *Candidates are essentially duplicates in classification (both incorrectly output few-layer WSe2), observed peaks, and reasoning, making identical core mistakes relative to GT monolayer expectations and 2LA(M)/B¹₂g rules. Neither outperforms the other on correctness, reasoning quality, or completeness.*

- **Game 28** · e vs g → **e** wins (conf=0.82)  
  *A is superior overall as it correctly detects WSe₂ and key ~248 cm⁻¹ mode plus substrate, aligning with ground truth on material; B fails fundamentally by calling it silicon. A's layer error and omission of 2LA(M) prevent full credit but it remains closer on scientific correctness and reasoning depth.*

- **Game 29** · e vs h → **e** wins (conf=0.90)  
  *A is far superior as it correctly recognizes WSe2 and key low-frequency modes with only a layer-count error, while B is a total failure misclassifying noise as ice. This aligns with ground truth on material even if A misses monolayer confirmation via absent B1 2g and strong 2LA.*

- **Game 30** · e vs i → **e** wins (conf=0.88)  
  *A correctly identifies WSe₂ and its characteristic overlapping E₂g/A₁g mode plus substrate Si peak, using appropriate TMDC Raman knowledge; B's sulfur assignment is a complete misclassification unrelated to the ground-truth monolayer WSe₂. Although A errs on layer number, its overall accuracy, reasoning depth, and relevance vastly outperform B.*

- **Game 31** · f vs g → **f** wins (conf=0.85)  
  *A correctly identified WSe₂ and relevant modes plus calibration offset while B completely missed the material; although A erred on layer number, it is substantially closer to GT expectations than B's total misclassification.*

- **Game 32** · f vs h → **f** wins (conf=0.92)  
  *A correctly recognizes WSe₂ and relevant low-frequency modes with proper calibration handling, while B produces an entirely hallucinatory ice assignment. Although A mislabels the layer count, it is the only output aligned with the ground-truth material and Raman signatures.*

- **Game 33** · f vs i → **f** wins (conf=0.82)  
  *A correctly identifies WSe₂ and handles the Si substrate/calibration, making it much closer to ground truth despite the layer-number error and missing 2LA(M). B's sulfur assignment is fundamentally wrong. Overall A is the superior output on correctness, reasoning, and relevance.*

- **Game 34** · g vs h → **draw** wins (conf=0.85)  
  *Both candidates are equally poor: zero scientific correctness on WSe₂ identification, no use of monolayer Raman markers, and conclusions unrelated to ground truth. A at least stayed in the proper spectral window but still missed the material; B is more bizarre. Clear draw on all evaluation dimensions.*

- **Game 35** · g vs i → **i** wins (conf=0.75)  
  *B is better overall: its chain-of-thought is grounded in systematic comparison across material families (including TMDCs), correctly flags the dominant low-wavenumber band, and expresses appropriate uncertainty, while A ignores the actual material peaks entirely.*

- **Game 36** · h vs i → **i** wins (conf=0.68)  
  *Both failed the core task of recognizing monolayer WSe₂, but B is clearly superior: it examined the physically relevant spectral region for TMDs, recognized possible artifacts, and considered a related TMD, while A was wholly distracted by noise into an unrelated molecular-ice assignment.*
