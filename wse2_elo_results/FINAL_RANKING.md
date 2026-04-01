# Tungsten Diselenide (WSe₂) ELO Ranking — Final Report

**Sample:** wse2_mono_sio2_001 (Monolayer WSe₂ on SiO₂/Si)  
**Judge:** claude-sonnet-4-6 with extended thinking (CoT)  
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
| 2 | **f** | 99.9 | 7 | 1 | 0 | 94% |
| 3 | **c** | 65.1 | 4 | 2 | 2 | 62% |
| 4 | **i** | 64.1 | 4 | 2 | 2 | 62% |
| 5 | **b** | 57.2 | 4 | 1 | 3 | 56% |
| 6 | **d** | 44.2 | 3 | 1 | 4 | 44% |
| 7 | **h** | 6.5 | 0 | 2 | 6 | 12% |
| 8 | **a** | 6.4 | 0 | 2 | 6 | 12% |
| 9 | **g** | 5.6 | 0 | 2 | 6 | 12% |

## Match Results

- **Game 1** · a vs b → **b** wins (conf=0.63)  
  *Both candidates failed the primary classification task entirely, never identifying WSe₂ or applying monolayer WSe₂ Raman diagnostics. Candidate B is marginally superior because it correctly anchored on the dominant ~248 cm⁻¹ peak, explicitly and correctly dismissed carbon-based materials, included a TMD (MoS₂) in its differential, maintained lower and better-calibrated confidence, and acknowledged instrumental artifacts. Candidate A's high-confidence graphite assignment based on hallucinated D/G-band evidence and a fabricated 'graphite shear mode' represents a more severe reasoning failure with no redeeming diagnostic steps.*

- **Game 2** · a vs c → **c** wins (conf=0.62)  
  *Neither candidate correctly identified the material as WSe₂ or applied any WSe₂/TMD Raman physics, making both answers fundamentally incorrect. Candidate B is marginally superior because it assigned a lower, more appropriate confidence (0.52 vs 0.92), correctly identified the SiO₂/Si substrate contribution at ~518 cm⁻¹, flagged the high-wavenumber region as likely photoluminescence, and avoided the wholesale hallucinations (graphite D/G bands, C-H overtones, AB shear mode) that undermine Candidate A's entire reasoning chain. The margin is small given both candidates failed the core classification task.*

- **Game 3** · a vs d → **d** wins (conf=0.62)  
  *Neither candidate correctly identified the material as WSe₂ or applied any WSe₂ Raman physics; both outputs are scientifically wrong and would be useless in practice. Candidate B is marginally preferred because it identified a real spectral feature consistent with the known SiO₂/Si substrate, explicitly flagged the primary WSe₂ peak (~249 cm⁻¹) as an unresolved anomaly rather than forcing a false assignment, maintained lower confidence, and avoided the high-confidence hallucination of an entirely fabricated graphite narrative that characterises Candidate A. In a real analytical workflow, B's acknowledged uncertainty would prompt further investigation, whereas A's confident misclassification would not.*

- **Game 4** · a vs e → **e** wins (conf=0.97)  
  *Candidate B correctly identified the material as WSe₂ and provided physically grounded reasoning for the primary spectral features, making it far superior to Candidate A, which completely misidentified the sample as bulk graphite through wholesale hallucination. B's primary failure — classifying the sample as few-layer rather than monolayer and omitting the critical 2LA(M) monolayer diagnostic — is a significant but secondary error compared to A's total material misidentification. B is the clear winner.*

- **Game 5** · a vs f → **f** wins (conf=0.97)  
  *Candidate A failed at the most fundamental level by misidentifying the material as graphite, constructing an entirely hallucinated reasoning chain around sp² carbon physics, and assigning high confidence to a completely wrong answer. Candidate B correctly identified WSe₂, applied sound substrate-calibration logic, and used legitimate TMD mode assignments, making it scientifically far superior despite its failure to identify the 2LA(M) monolayer diagnostic and its incorrect few-layer layer-count conclusion. B's errors are errors of omission and a single mis-applied selection-rule argument; A's errors are total misidentification — B wins decisively.*

- **Game 6** · a vs g → **draw** wins (conf=0.82)  
  *Both candidates catastrophically failed the primary task of identifying the sample as monolayer WSe₂, applied no WSe₂-specific Raman physics, and produced overconfident wrong classifications. Candidate A's output is more elaborate but more hallucinatory (fabricating graphite D/G band assignments), while Candidate B's output is simpler but anchors on the real substrate Si peak without recognising it as such. Neither demonstrates any advantage in correctness, reasoning quality, or completeness relative to the WSe₂ ground truth, making a draw the only defensible outcome.*

- **Game 7** · a vs h → **draw** wins (conf=0.82)  
  *Both candidates failed completely and equally to identify the material as monolayer WSe₂ — the single most important criterion — and neither applied any WSe₂ or TMD Raman physics in their reasoning. Candidate A hallucinated graphite-specific features with higher false confidence (0.92), while Candidate B offered a more cautious but equally wrong ice assignment (0.76) with slightly cleaner internal logic. These marginal stylistic differences do not outweigh the shared, total failure on material classification, layer-count determination, and spectral interpretation, warranting a draw.*

- **Game 8** · a vs i → **i** wins (conf=0.58)  
  *Both candidates fail entirely to identify the WSe₂ monolayer spectrum and demonstrate no knowledge of relevant WSe₂ Raman physics. Candidate B is marginally preferred because it expresses lower and more appropriate confidence (0.62 vs 0.92), explicitly acknowledges that large portions of the spectrum cannot be explained by its proposed material, flags purity as unknown, and includes a TMDC (MoS₂) among its candidates — all signs of better calibrated uncertainty. Candidate A's high-confidence fabrication of an entirely wrong graphite narrative with no self-doubt is the more egregious failure.*

- **Game 9** · b vs c → **draw** wins (conf=0.55)  
  *Both candidates failed entirely at the core task: neither identified the material as WSe₂ or invoked any WSe₂-specific Raman physics (merged E¹₂g/A₁g, 2LA(M) monolayer enhancement, B¹₂g suppression). Candidate A was more confidently wrong (0.72 for sulfur) while Candidate B was less confidently wrong (0.52 for cinnabar) and partially redeemed itself by correctly attributing the ~518 cm⁻¹ feature to the Si substrate; however, cinnabar is a far more exotic and implausible assignment than sulfur. These marginal differences do not meaningfully distinguish the two responses given their shared and complete failure to classify the spectrum correctly.*

- **Game 10** · b vs d → **b** wins (conf=0.58)  
  *Both candidates failed entirely to identify WSe₂ and neither applied any monolayer TMD Raman diagnostics. Candidate A is marginally superior because it correctly focused analytical attention on the dominant ~248 cm⁻¹ peak — the actual WSe₂ E¹₂g/A₁g feature — as the primary identification anchor, which is methodologically sounder than Candidate B's approach of anchoring on the substrate Si signal (~518 cm⁻¹) and dismissing the material's own dominant peak as anomalous. Candidate B also expresses higher (85%) confidence in a more fundamentally misguided conclusion, compounding its error.*

- **Game 11** · b vs e → **e** wins (conf=0.97)  
  *Candidate B correctly identifies the material as WSe₂ and provides physically grounded reasoning rooted in WSe₂ Raman spectroscopy, whereas Candidate A catastrophically misidentifies the sample as elemental sulfur—a complete failure on the primary classification task. Although B errs on layer count (few-layer instead of monolayer) and omits the critical 2LA(M) monolayer diagnostic, these are secondary errors that do not invalidate the core identification. B is unambiguously superior overall.*

- **Game 12** · b vs f → **f** wins (conf=0.97)  
  *Candidate B correctly identified the material as WSe₂ with appropriate mode assignments and a reasonable physical reasoning chain, making it vastly superior to Candidate A which produced a complete material misidentification (sulfur). B's primary shortcoming — classifying the sample as few-layer rather than monolayer, and omitting the 2LA(M) monolayer diagnostic — is a meaningful error against the ground truth but does not negate the fundamentally correct material identification and WSe₂-specific spectroscopic reasoning.*

- **Game 13** · b vs g → **b** wins (conf=0.67)  
  *Both candidates failed the primary classification task by not identifying WSe₂, but Candidate A is the lesser failure: it correctly anchored its analysis to the actual dominant spectral feature (~248 cm⁻¹, the true WSe₂ merged mode), noted the ~306 cm⁻¹ region (near B¹₂g), provided more thorough multi-step reasoning, and expressed appropriate uncertainty (0.72 vs 0.95). Candidate B compounded its error by building a high-confidence silicon identification on a secondary substrate peak while ignoring the most prominent spectral feature — a more serious analytical failure than A's misidentification of the correct dominant peak.*

- **Game 14** · b vs h → **b** wins (conf=0.58)  
  *Neither candidate correctly identifies the material as WSe₂ monolayer, so both fail on the primary criterion. However, Candidate A is marginally less wrong: it correctly anchors its analysis in the low-frequency fingerprint region (130–520 cm⁻¹) that contains all genuine spectral information, and its reasoning about peak positions is at least grounded in real features of the spectrum. Candidate B makes the more severe error of constructing its entire classification around high-wavenumber spike-noise artifacts while dismissing the only diagnostically meaningful peaks, producing an answer (water ice) that is further from the ground truth and based on a more fundamentally flawed methodology.*

- **Game 15** · b vs i → **i** wins (conf=0.58)  
  *Both candidates failed the primary task by misidentifying monolayer WSe₂ as orthorhombic sulfur and neither applied any WSe₂-specific Raman diagnostics. B is marginally preferred solely because it demonstrated better epistemic calibration: lower confidence score (0.62 vs 0.72), honest 'unknown' purity designation, and more careful identification of high-wavenumber peaks as artifacts — all reflecting appropriate uncertainty for what is ultimately an incorrect classification. The margin is small because the core scientific error is identical in both cases.*

- **Game 16** · c vs d → **c** wins (conf=0.62)  
  *Both candidates fail entirely to identify the correct material (monolayer WSe₂) and neither applies any WSe₂ Raman physics; both answers are scientifically incorrect relative to the ground truth. Candidate A is marginally preferable because it correctly prioritises the dominant ~247 cm⁻¹ peak as the primary diagnostic feature (which does correspond to the WSe₂ E¹₂g/A₁g/2LA(M) complex region), appropriately treats the ~518 cm⁻¹ peak as a secondary substrate contribution, and expresses calibrated uncertainty (0.52 confidence). Candidate B is logically self-contradictory — explicitly noting the ~249 cm⁻¹ feature is nearly twice as intense as the ~518 cm⁻¹ peak yet classifying the sample as silicon with 0.85 confidence — making its reasoning quality inferior.*

- **Game 17** · c vs e → **e** wins (conf=0.93)  
  *Candidate B correctly identifies the material as WSe₂ and provides physically grounded peak assignments consistent with WSe₂ Raman physics, whereas Candidate A catastrophically misidentifies the material as cinnabar (HgS), rendering its entire analysis irrelevant to the ground truth. Although B incorrectly classifies the layer number as few-layer and omits the critical 2LA(M) monolayer diagnostic, these are secondary errors compared to A's complete material misidentification. B is the clear winner despite its imperfections.*

- **Game 18** · c vs f → **f** wins (conf=0.95)  
  *Candidate B correctly identifies the material as WSe₂ with appropriate peak assignments and substrate recognition, which represents the primary classification objective; its errors are confined to the secondary task of layer-number determination and the omission of 2LA(M) analysis. Candidate A fails at the most fundamental level by misidentifying the entire material as cinnabar (HgS), applying no WSe₂ or TMD physics, and producing a result with zero scientific utility for this sample. B is unambiguously superior despite its layer-count error.*

- **Game 19** · c vs g → **c** wins (conf=0.72)  
  *Both candidates fail to identify WSe₂, but Candidate A is meaningfully less wrong: it correctly identifies the ~247 cm⁻¹ peak as the dominant spectral feature (consistent with the WSe₂ E¹₂g/A₁g position) and appropriately demotes the Si substrate peak to a secondary role, whereas Candidate B inverts this hierarchy entirely and delivers a highly overconfident wrong answer based on ignoring the primary diagnostic peak. Candidate A also employs more thorough multi-step reasoning and calibrates its uncertainty more honestly, even though its final material assignment is incorrect.*

- **Game 20** · c vs h → **c** wins (conf=0.62)  
  *Both candidates fail entirely to identify WSe₂, making neither scientifically correct. However, Candidate A is marginally less wrong: it focused on the diagnostically relevant low-wavenumber spectral region (~247 cm⁻¹, ~306 cm⁻¹), correctly identified the Si substrate contribution at ~518 cm⁻¹, and expressed appropriate uncertainty (0.52). Candidate B compounded its error by building a high-confidence (0.76) case on high-wavenumber artifact/PL features while dismissing the only region that contains genuine Raman information about the sample, making its reasoning both more confident and more fundamentally misdirected.*

- **Game 21** · c vs i → **draw** wins (conf=0.72)  
  *Both candidates are equally and completely incorrect in their material identification, neither approaching WSe₂ or applying any monolayer TMDC selenide Raman diagnostics. Candidate A shows marginally better substrate awareness (recognising the ~518 cm⁻¹ Si phonon as a possible substrate contribution) and more appropriate uncertainty (confidence 0.52 vs 0.62), while Candidate B shows marginally broader TMDC awareness by explicitly ruling out MoS₂ and WS₂ yet still never considering WSe₂. These minor relative merits cancel out, making a draw the only defensible verdict.*

- **Game 22** · d vs e → **e** wins (conf=0.97)  
  *Candidate B correctly identifies the sample as WSe₂ — the fundamental classification task — and grounds its reasoning in TMD Raman physics, despite making a secondary error in layer-number determination by misusing the B¹₂g criterion and omitting the 2LA(M) monolayer diagnostic. Candidate A fails at the most basic level by classifying the sample as silicon, rendering all subsequent analysis irrelevant. In every dimension — material identity, reasoning validity, and result completeness — Candidate B is unambiguously superior.*

- **Game 23** · d vs f → **f** wins (conf=0.97)  
  *Candidate B correctly identifies the material as WSe₂ and applies relevant TMD Raman physics, while Candidate A commits a fundamental error by classifying the sample as silicon based solely on the substrate peak. Although B incorrectly determines the layer count as few-layer (misusing B¹₂g logic) and omits the 2LA(M) monolayer diagnostic, these are secondary errors compared to A's complete misidentification of the material. B is unambiguously the better response across all evaluation dimensions.*

- **Game 24** · d vs g → **d** wins (conf=0.78)  
  *Both candidates fail fundamentally by misidentifying monolayer WSe₂ as crystalline silicon and neither applies any WSe₂-relevant Raman physics. Candidate A is the lesser failure because it correctly recognised that the ~249 cm⁻¹ peak being more intense than the supposed silicon first-order peak is highly anomalous, appropriately reduced its confidence, and flagged the spectrum as non-standard — demonstrating better scientific skepticism. Candidate B compounded its wrong identification with overconfidence (0.95), a false claim of spectral simplicity, and shallower reasoning, making it the worse output overall.*

- **Game 25** · d vs h → **d** wins (conf=0.62)  
  *Neither candidate correctly identified the material as WSe₂, making both fundamentally wrong for the stated task. However, Candidate A's failure is less severe: it correctly identifies real spectral features present in the data (the SiO₂/Si substrate Si peak at 518 cm⁻¹, the anomalously prominent ~249 cm⁻¹ WSe₂ feature, the ~304 cm⁻¹ peak), and its reasoning, though misapplied, is physically grounded. Candidate B constructed an entirely fictitious water-ice interpretive framework with no physical basis for this spectrum, representing a more complete reasoning failure. Candidate A is therefore marginally preferred, though both responses are of very low scientific value for a WSe₂ classification task.*

- **Game 26** · d vs i → **draw** wins (conf=0.82)  
  *Both candidates failed completely and equally to identify the sample as monolayer WSe₂ on SiO₂/Si, and neither applied any WSe₂ Raman physics (E¹₂g/A₁g near-degeneracy, 2LA(M) enhancement, B¹₂g suppression) in their reasoning. Candidate A's incidental correct identification of the Si substrate peak does not constitute a meaningful advantage, and Candidate B's sulfur assignment contains its own factual errors in mode assignments. Across all three evaluation dimensions — scientific correctness, reasoning quality, and completeness — the two outputs are indistinguishably poor, warranting a draw.*

- **Game 27** · e vs f → **draw** wins (conf=0.82)  
  *Both candidates produce virtually identical outputs — same peak list, same material identification, same (incorrect) few-layer assignment, same confidence score, and the same omission of the 2LA(M) mode and B¹₂g-suppression criterion that are essential for monolayer confirmation. Candidate B's calibration-correction step is a marginal methodological improvement, but it neither fixes the layer-count error nor recovers the missing 2LA(M) analysis, making the overall quality of both responses indistinguishably poor relative to the ground truth. A draw is the only defensible verdict.*

- **Game 28** · e vs g → **e** wins (conf=0.97)  
  *Candidate A, despite incorrectly concluding 'few-layer' and missing the 2LA(M) monolayer diagnostic, at least correctly identifies the material as WSe₂ and engages meaningfully with its Raman physics. Candidate B misidentifies the entire sample as bulk silicon — a catastrophic, fundamental error that renders its output scientifically worthless for this task. On every evaluated dimension Candidate A is unambiguously superior.*

- **Game 29** · e vs h → **e** wins (conf=0.97)  
  *Candidate A correctly identifies the material as WSe₂ with an accurate primary peak assignment, correct substrate identification, and partially valid mode labelling — errors are limited to an incorrect few-layer conclusion and the omission of the 2LA(M) monolayer diagnostic. Candidate B is a complete misclassification, identifying the spectrum as crystalline water ice by confusing high-wavenumber instrumental noise for OH-stretch bands, rendering it scientifically worthless for this task. Candidate A is unambiguously the better response despite its layer-count and completeness shortcomings.*

- **Game 30** · e vs i → **e** wins (conf=0.93)  
  *Candidate A correctly identifies WSe₂ as the material — the most fundamental requirement — and provides physically grounded reasoning around TMDC vibrational modes, even though it incorrectly concludes few-layer by misusing the B¹₂g feature and omits the critical 2LA(M) monolayer diagnostic. Candidate B fails at the most basic level by misidentifying the spectrum as orthorhombic sulfur and misassigning the Si substrate peak, making its entire analysis scientifically invalid. A's errors are consequential but partial; B's error is total.*

- **Game 31** · f vs g → **f** wins (conf=0.97)  
  *Candidate A, despite incorrectly classifying the layer count as few-layer and missing the critical 2LA(M) monolayer diagnostic, at least correctly identifies the material as WSe₂ and grounds its reasoning in TMD Raman physics. Candidate B commits a fundamental error by misidentifying the entire sample as bulk silicon, confusing the SiO₂/Si substrate peak for the sample signal and ignoring all WSe₂ spectral features. A's partial correctness vastly outweighs B's complete misidentification on every evaluation dimension.*

- **Game 32** · f vs h → **f** wins (conf=0.97)  
  *Candidate A correctly identifies the material as WSe₂ and provides physically motivated peak assignments, making it unambiguously superior to Candidate B, which catastrophically misidentifies the sample as water ice by confusing instrument noise spikes with OH-stretch bands. Although A makes significant errors—wrong layer count (few-layer instead of monolayer), omission of the 2LA(M) diagnostic, and inverted B¹₂g logic—these are analytical shortcomings within a correct material framework, whereas B fails at the most fundamental classification step and provides no useful spectroscopic insight for a WSe₂ sample.*

- **Game 33** · f vs i → **f** wins (conf=0.91)  
  *Candidate A at least correctly identifies the material as WSe₂ with plausible mode assignments and a calibration-correction rationale, making its error one of layer-count determination rather than material identity. Candidate B's complete misidentification of the sample as orthorhombic sulfur—misreading both the primary WSe₂ Raman signature and the Si substrate reference peak—constitutes a categorical failure that renders all subsequent analysis invalid. Despite A's significant omission of 2LA(M) analysis and incorrect 'few-layer' conclusion, it is clearly superior to B on every evaluated dimension.*

- **Game 34** · g vs h → **draw** wins (conf=0.82)  
  *Both candidates failed completely and equally on the primary task: neither identified the material as WSe₂, neither applied any WSe₂ Raman physics, and neither produced any of the required classification outputs (merged E¹₂g/A₁g, 2LA(M) intensity, B¹₂g absence, monolayer confirmation). Candidate A is more overconfident and shallower in reasoning; Candidate B is marginally more systematic and less overconfident, but equally wrong in its final answer. These marginal differences in secondary qualities do not justify declaring a winner when both outputs are fundamentally useless for the stated task.*

- **Game 35** · g vs i → **i** wins (conf=0.72)  
  *Both candidates fail to identify the sample as monolayer WSe₂ and neither applies any WSe₂-specific Raman physics. However, Candidate B is the lesser of two errors: it correctly focuses on the ~249 cm⁻¹ dominant feature (the actual WSe₂ merged E¹₂g/A₁g peak), shows appropriately calibrated lower confidence, correctly dismisses the dense high-wavenumber peaks as artifacts, and at least lists a TMDC (MoS₂) among alternatives. Candidate A is confidently wrong at 0.95, misidentifying the entire spectrum as bulk silicon by fixating on a substrate-related peak while ignoring the primary spectral signature of the actual 2D material.*

- **Game 36** · h vs i → **i** wins (conf=0.58)  
  *Both candidates completely failed to identify the material as monolayer WSe₂ and neither applied any WSe₂-specific Raman physics. Candidate B is marginally less wrong because it correctly prioritised the low-wavenumber region as the primary diagnostic zone, appropriately flagged the anomalous high-wavenumber peaks as artifacts, considered TMDC materials (MoS₂, WS₂) in its reasoning, and assigned a lower (more appropriate) confidence score. Candidate A's reasoning was entirely off-target in the domain of water ice physics, actively excluded semiconductors and 2D materials from consideration, and assigned a higher confidence (0.76) to an incorrect assignment, making it the worse output overall.*
