# Hexagonal Boron Nitride (h-BN) ELO Ranking — Final Report

**Sample:** hbn_bulk_001 (Bulk h-BN, orientation 001)  
**Judge:** claude-sonnet-4-6 with extended thinking (CoT)  
**ELO range:** 0.0–100.0 · Start: 50.0 · K=16  
**Total games played:** 36  

## Ground Truth
```
GROUND TRUTH — Hexagonal Boron Nitride Sample (hbn_bulk_001)
=============================================================
Sample type       : Bulk hexagonal boron nitride (h-BN), natural crystal or
                   CVD-grown; crystallographic orientation 001
Abbreviation      : hbn_bulk_001

Expected Raman signature
  E₂g band (~1366 cm⁻¹) : In-plane B–N stretching mode (analogous to graphene's
                           G band); the DOMINANT and typically only first-order
                           Raman-active peak in h-BN. Should be sharp and intense.
  ZO' / overtone (~1366 cm⁻¹ + ~2700 cm⁻¹ region): Second-order features are
                           weaker and broader; unlike graphene, the 2D-equivalent
                           overtone is NOT a strong diagnostic for layer count in
                           bulk h-BN.
  Defect-related bands   : Peaks near 1300–1340 cm⁻¹ or broad features may
                           indicate nitrogen vacancies or stacking disorder;
                           should be LOW or absent in high-quality bulk h-BN.

Key quality indicators
  • E₂g peak: single Lorentzian, FWHM ≈ 7–15 cm⁻¹ for high-quality bulk h-BN
               (monolayer h-BN shows broader FWHM ≈ 15–30 cm⁻¹)
  • Peak position: ~1366 cm⁻¹ (can shift ±5 cm⁻¹ with strain or substrate)
  • No broad defect bands → minimal structural disorder
  • Weak or absent overtone/combination bands → clean crystal
  • IR-active A₂u mode (~783 cm⁻¹) is NOT Raman active; its absence in Raman
    confirms correct assignment

Classification target : HEXAGONAL BORON NITRIDE (h-BN), bulk
Substrate            : None (freestanding) or SiO₂/Si, orientation 001
```

## Final Rankings

| Rank | Model | ELO | W | D | L | Win% |
|------|-------|-----|---|---|---|------|
| 1 | **d** | 100.0 | 8 | 0 | 0 | 100% |
| 2 | **b** | 95.2 | 7 | 0 | 1 | 88% |
| 3 | **f** | 78.5 | 6 | 0 | 2 | 75% |
| 4 | **e** | 64.2 | 5 | 0 | 3 | 62% |
| 5 | **c** | 51.2 | 4 | 0 | 4 | 50% |
| 6 | **h** | 27.9 | 2 | 1 | 5 | 31% |
| 7 | **i** | 21.9 | 1 | 2 | 5 | 25% |
| 8 | **a** | 14.2 | 1 | 1 | 6 | 19% |
| 9 | **g** | 0.0 | 0 | 0 | 8 | 0% |

## Match Results

- **Game 1** · a vs b → **b** wins (conf=0.98)  
  *Candidate B is unambiguously superior: it correctly identifies the material as hexagonal boron nitride, correctly assigns the dominant peak to the E₂g mode, applies appropriate AA' stacking, and constructs physically coherent reasoning that explicitly eliminates graphene/graphite. Candidate A makes a fundamental misidentification (graphite instead of h-BN) with internally contradictory logic (crystalline graphite with only a D-band and no G-band), rendering its output scientifically invalid on every evaluated dimension.*

- **Game 2** · a vs c → **c** wins (conf=0.92)  
  *Candidate B, despite an internal inconsistency between its chain-of-thought and its final material_prediction label, correctly identifies h-BN as the primary candidate through scientifically grounded reasoning and lists it first in the top_candidates. Candidate A fundamentally misidentifies the material as graphite with 0.85 confidence, applies physically incorrect logic throughout, and never considers h-BN — making it far less useful and more dangerous as a classification output. B is the clear winner on all three evaluation dimensions.*

- **Game 3** · a vs d → **d** wins (conf=0.98)  
  *Candidate B correctly identifies the material as hexagonal boron nitride, correctly assigns the dominant 1369 cm⁻¹ peak to the E₂g mode, and uses physically rigorous differential diagnosis to rule out competing materials — all consistent with the ground truth. Candidate A makes a fundamental material misclassification (graphite instead of h-BN) based on an incorrect D-band assignment, demonstrating a failure to recognize the most distinctive spectral fingerprint of h-BN. There is no dimension on which Candidate A equals or surpasses Candidate B.*

- **Game 4** · a vs e → **e** wins (conf=0.97)  
  *Candidate B correctly identifies the material as hexagonal boron nitride and correctly assigns the dominant peak to the E₂g in-plane B–N stretching mode, which are the two most critical classification tasks. Candidate A makes a catastrophic material misidentification (graphite) based on physically incoherent reasoning. Although B incorrectly infers monolayer morphology rather than bulk, this is a secondary error grounded in observable spectral parameters (FWHM 28 cm⁻¹, slight blue-shift), whereas A's errors are foundational and disqualifying.*

- **Game 5** · a vs f → **f** wins (conf=0.97)  
  *Candidate B correctly identifies the material as hexagonal boron nitride and the dominant peak as the E₂g mode, aligning with the ground truth in all primary respects; its only notable error is assigning monolayer rather than bulk morphology, which is a secondary classification mistake. Candidate A commits a fundamental scientific error by misidentifying the sample as graphite and fabricating a physically impossible 'single D-band without G-band' scenario, making it incorrect on every critical dimension. Candidate B is unambiguously superior.*

- **Game 6** · a vs g → **a** wins (conf=0.62)  
  *Both candidates fail the primary task of identifying h-BN, but Candidate A is marginally superior because it acknowledges the physically anomalous absence of a G-band (an implicit clue pointing away from carbon materials), provides more structured reasoning, and reports a slightly lower confidence (0.85 vs 0.90) commensurate with the internal inconsistencies it recognises. Candidate B assigns near-certainty to monolayer graphene based on superficial pattern-matching with no critical evaluation of missing diagnostic peaks, representing a worse epistemic standard.*

- **Game 7** · a vs h → **h** wins (conf=0.65)  
  *Both candidates fail catastrophically by not identifying the material as h-BN, but Candidate B is marginally better due to more appropriate confidence calibration (0.62 vs 0.85), more epistemically honest uncertainty assignments (unknown purity, N/A stacking), and more logically consistent — though still wrong — reasoning. Candidate A compounds its misidentification with physically incorrect Raman physics (claiming crystalline graphite can lack a G-band) and unjustifiably high confidence, making it the worse of two incorrect answers.*

- **Game 8** · a vs i → **draw** wins (conf=0.78)  
  *Both candidates made the identical and fundamental error of misclassifying hexagonal boron nitride as a carbon-based material, with neither ever considering h-BN as a candidate despite the peak at ~1369 cm⁻¹ being the textbook E₂g signature of h-BN. Candidate A is more confidently wrong (0.85 vs 0.62), while Candidate B shows marginally better epistemic calibration and flags one internal inconsistency, but also introduces an unjustified polyethylene candidate. Since both failed completely on the primary classification objective and neither demonstrates any h-BN-specific Raman physics knowledge, a draw is the appropriate verdict—both outputs are equally unsuitable as correct analyses of this spectrum.*

- **Game 9** · b vs c → **b** wins (conf=0.88)  
  *Candidate A delivers a correct final classification of hexagonal boron nitride with appropriate confidence and clear evidence linking the E₂g mode at 1369 cm⁻¹ to h-BN, despite an error in FWHM-to-morphology mapping. Candidate B's chain-of-thought contains some stronger physical insights (especially on FWHM), but its final classification result — the only output that matters operationally — incorrectly labels the sample as graphitic carbon, a fundamental misidentification that disqualifies it regardless of reasoning quality.*

- **Game 10** · b vs d → **d** wins (conf=0.70)  
  *Candidate B produces a more scientifically accurate analysis by correctly interpreting the broader-than-expected FWHM (~30 cm⁻¹) as evidence of polycrystalline or defect-rich character, consistent with the ground truth quality indicators (7–15 cm⁻¹ for high-quality bulk). Candidate A commits a directional physics error by inverting the bulk-vs-monolayer FWHM relationship, undermining its layer-count inference. Both correctly identify h-BN and the E₂g mode, but B's chain-of-thought reasoning is more grounded in established Raman physics for h-BN.*

- **Game 11** · b vs e → **b** wins (conf=0.82)  
  *Candidate A correctly classifies the sample as bulk h-BN in agreement with the ground truth, which is the most critical dimension of the evaluation. Although A contains a factual error in its FWHM reasoning (inverting the FWHM-layer-count relationship), this does not overturn its correct final classification. Candidate B's monolayer assignment directly contradicts the ground truth and is based on an overinterpretation of a 3 cm⁻¹ peak shift that falls within normal experimental uncertainty, making B's classification fundamentally incorrect despite its otherwise structured reasoning.*

- **Game 12** · b vs f → **b** wins (conf=0.82)  
  *Candidate A delivers the correct ground-truth classification of bulk h-BN, supported by a more complete reasoning chain including stacking-order determination and differential diagnosis. Although its FWHM interpretation is inverted relative to established h-BN data (28 cm⁻¹ is outside the 7–15 cm⁻¹ bulk range), this does not change its correct final answer. Candidate B commits a more consequential error by misclassifying the sample as monolayer on the basis of a 3 cm⁻¹ shift that is indistinguishable from strain or substrate effects, and omits FWHM analysis entirely — making A the clearly superior output.*

- **Game 13** · b vs g → **b** wins (conf=0.98)  
  *Candidate A correctly identifies h-BN, assigns the E₂g mode, and provides a logically sound differential diagnosis grounded in established Raman physics, with only a minor and non-fatal FWHM interpretation inconsistency. Candidate B commits a fundamental material misidentification (graphene instead of h-BN), relies on physically unjustified peak assignment, and lacks any meaningful differential reasoning, making it scientifically unreliable. The performance gap between the two candidates is decisive across all evaluated dimensions.*

- **Game 14** · b vs h → **b** wins (conf=0.97)  
  *Candidate A correctly identifies the sample as hexagonal boron nitride with the E₂g mode at 1369 cm⁻¹, provides sound differential reasoning against graphene/graphite, and delivers a complete, well-structured classification result; its sole significant error is inverting the FWHM relationship between bulk and monolayer h-BN. Candidate B makes a fundamental material misidentification (diamond-like carbon), fails to consider h-BN at all, and bases its entire reasoning on an incorrect D-band analogy, rendering its output scientifically useless for this sample. Candidate A is the clear winner on all three evaluation dimensions.*

- **Game 15** · b vs i → **b** wins (conf=0.97)  
  *Candidate A correctly classifies the spectrum as bulk h-BN with the E₂g mode at 1369 cm⁻¹, applies sound differential reasoning against graphite, and produces a complete, well-evidenced result consistent with the ground truth despite a minor FWHM directional error. Candidate B commits a fundamental material misidentification by assigning the spectrum to graphitic carbon, fails to consider h-BN despite the clear spectral signature, and produces an unreliable top-candidate list — making it substantially inferior on all evaluation dimensions.*

- **Game 16** · c vs d → **d** wins (conf=0.95)  
  *Candidate B correctly and consistently identifies the material as hexagonal boron nitride, properly assigns the E2g mode, and uses sound Raman physics to exclude alternative candidates — matching the ground truth on every key dimension. Candidate A's reasoning is partially correct but fatally undermined by a final classification that contradicts its own chain-of-thought and incorrectly labels the material as graphitic carbon, making it scientifically wrong on the most critical output field.*

- **Game 17** · c vs e → **e** wins (conf=0.65)  
  *Correct material identification is the most fundamental criterion, and Candidate B unambiguously names h-BN as the material with its E₂g mode correctly assigned, whereas Candidate A's final output declares graphene/graphitic carbon as the primary label — a factually wrong answer despite better internal reasoning. B's monolayer misclassification and inflated confidence are significant errors but secondary to getting the material right. Neither candidate perfectly matches the ground truth (bulk h-BN, FWHM 7–15 cm⁻¹), but B's output is more useful and less misleading to an end user.*

- **Game 18** · c vs f → **f** wins (conf=0.82)  
  *Candidate B correctly identifies the material as hexagonal boron nitride with clear, physically consistent reasoning, whereas Candidate A contradicts its own chain-of-thought by issuing a final classification of graphitic carbon — a fundamental failure. B's error (layer-count: monolayer vs. ground-truth bulk) is a secondary, less severe mistake compared to A's wrong primary material identification. On all three evaluation dimensions — correctness, reasoning coherence, and classification clarity — Candidate B is the superior output.*

- **Game 19** · c vs g → **c** wins (conf=0.85)  
  *Candidate A, despite a contradictory final label, demonstrates scientifically grounded reasoning that correctly identifies h-BN E₂g as the best spectral match, appropriately rejects graphene based on peak position and absence of G/2D bands, and expresses calibrated uncertainty — all hallmarks of valid Raman analysis. Candidate B commits a fundamental misidentification (graphene monolayer at 0.9 confidence) with no consideration of h-BN and no physically defensible reasoning, making it clearly inferior on all evaluation dimensions.*

- **Game 20** · c vs h → **c** wins (conf=0.87)  
  *Candidate A, despite its inconsistent final label, demonstrates genuine understanding of h-BN Raman physics: it correctly matches 1369 cm⁻¹ to the E₂g mode, lists h-BN as the primary candidate in top_candidates, and uses physically sound arguments (absence of G band, FWHM analysis). Candidate B commits a more serious error by completely ignoring h-BN and confidently misclassifying the spectrum as diamond-like carbon with no physical basis. A partial but informed answer is superior to a confident but entirely incorrect one in a materials identification context.*

- **Game 21** · c vs i → **c** wins (conf=0.87)  
  *Candidate A is clearly superior despite its internal inconsistency between the chain-of-thought and the primary classification field: it correctly identifies h-BN E₂g as the best spectral match in its reasoning and places h-BN as the top-ranked alternative candidate, demonstrating genuine domain knowledge. Candidate B commits entirely to a wrong graphitic carbon assignment, never considers h-BN, and introduces a hallucinated polyethylene candidate, making it scientifically unreliable and further from the ground truth on every evaluated dimension.*

- **Game 22** · d vs e → **d** wins (conf=0.85)  
  *Candidate A correctly classifies the sample as bulk h-BN, consistent with the ground truth, and builds its conclusion on sound elimination reasoning and defensible FWHM interpretation. Candidate B makes a fundamental and unambiguous morphological error—claiming monolayer based on a 3 cm⁻¹ shift that lies within the normal strain/substrate variation range acknowledged by the ground truth—directly contradicting the expected bulk classification. Despite both candidates sharing identical confidence scores and similar formatting quality, Candidate A's scientifically accurate bulk identification makes it the clear winner.*

- **Game 23** · d vs f → **d** wins (conf=0.87)  
  *Candidate A correctly identifies the sample as bulk h-BN, directly matching the ground truth label (hbn_bulk_001), and supports this with FWHM analysis even if the 'polycrystalline' label is imprecise. Candidate B commits a material classification error by asserting monolayer based on a 3 cm⁻¹ peak shift that is within normal bulk h-BN variation, and it omits the FWHM criterion entirely, which is the primary spectroscopic discriminator for layer count in h-BN. The bulk vs. monolayer distinction is the central classification task, and Candidate A gets it right while Candidate B does not.*

- **Game 24** · d vs g → **d** wins (conf=0.98)  
  *Candidate A correctly identifies the sample as hexagonal boron nitride with the E₂g mode at 1369 cm⁻¹, provides a logically sound differential diagnosis, and delivers a complete, well-evidenced classification result. Candidate B misidentifies the sample as monolayer graphene, misassigns the peak, ignores the absence of mandatory graphene bands, and offers no consideration of h-BN—errors that are both fundamental and disqualifying. Candidate A is the clear and unambiguous winner.*

- **Game 25** · d vs h → **d** wins (conf=0.97)  
  *Candidate A correctly identifies hexagonal boron nitride and correctly assigns the dominant 1369 cm⁻¹ feature to the E₂g phonon mode, with sound differential reasoning that excludes carbon and diamond. Candidate B commits a fundamental misidentification — classifying the spectrum as diamond-like/amorphous carbon — by misinterpreting the h-BN E₂g peak as a carbon D-band, never considering h-BN as a candidate. The minor phase-labelling imprecision in Candidate A is inconsequential compared to Candidate B's complete material misclassification.*

- **Game 26** · d vs i → **d** wins (conf=0.97)  
  *Candidate A correctly identifies the material as hexagonal boron nitride and assigns the 1369 cm⁻¹ peak to the E₂g mode with sound, internally consistent reasoning, matching the ground truth on all primary criteria. Candidate B commits a fundamental misclassification by labelling the spectrum as graphitic carbon despite its own evidence (absent G-band) pointing away from carbon, and never considers h-BN at all. The correctness gap between A and B is decisive across every evaluation dimension.*

- **Game 27** · e vs f → **f** wins (conf=0.62)  
  *Both models fail on the critical bulk-vs-monolayer classification, which is the ground truth's defining feature. However, Candidate B demonstrates superior reasoning methodology through systematic differential diagnosis, avoids introducing an unverified FWHM value, assigns more conservative and appropriate confidence, and presents scientifically meaningful alternative candidates. Candidate A's hallucinated or unjustified FWHM of 28 cm⁻¹ and inflated confidence of 0.95 constitute additional penalisable errors absent in B.*

- **Game 28** · e vs g → **e** wins (conf=0.97)  
  *Candidate A correctly identifies the material as h-BN and provides a physically grounded assignment of the E₂g mode, with only a secondary error in morphological classification (monolayer vs. bulk). Candidate B commits a fundamental material misidentification by classifying the spectrum as graphene based on an incorrectly positioned D band assignment, ignoring the complete absence of graphene's diagnostic G and 2D bands. On every evaluated dimension—scientific correctness, reasoning quality, and completeness—Candidate A is clearly superior.*

- **Game 29** · e vs h → **e** wins (conf=0.97)  
  *Candidate A correctly identifies the material as h-BN and its dominant E₂g Raman mode, which is the primary classification objective; its only error is assigning monolayer rather than bulk morphology, a secondary determination that is at least physically argued from FWHM and peak-shift data. Candidate B commits a fundamental error by misidentifying the material entirely as diamond-like carbon, rendering its entire analysis irrelevant to the ground truth. On every evaluation dimension—scientific correctness, reasoning quality, and completeness—Candidate A is substantially superior.*

- **Game 30** · e vs i → **e** wins (conf=0.95)  
  *Candidate A makes the correct material identification (h-BN) and correct band assignment (E₂g), with only a secondary error in classifying the morphology as monolayer rather than bulk — an error partially defensible by the observed FWHM. Candidate B completely misidentifies the material as graphitic carbon, fails to consider h-BN at any stage, and ignores a critical disqualifying clue (absence of G band), making it wrong on every scientifically essential dimension. Candidate A is unambiguously superior.*

- **Game 31** · f vs g → **f** wins (conf=0.97)  
  *Candidate A correctly identifies the material as hexagonal boron nitride and correctly assigns the peak to the E₂g mode, making only a secondary error in layer-count inference (monolayer vs. bulk). Candidate B misidentifies the material as graphene entirely, committing a fundamental spectroscopic error by ignoring the absence of the required G band. On every evaluated dimension—scientific correctness, reasoning quality, and classification completeness—Candidate A is unambiguously superior.*

- **Game 32** · f vs h → **f** wins (conf=0.97)  
  *Candidate A correctly identifies hexagonal boron nitride and its diagnostic E₂g mode at 1369 cm⁻¹, with only a minor and partially defensible error in layer-count assignment (monolayer vs bulk). Candidate B commits a fundamental misidentification—labelling h-BN as diamond-like amorphous carbon—and its entire reasoning chain is built on misattributing a well-known h-BN signature to a carbon D-band. On all three evaluation dimensions (scientific correctness, reasoning quality, completeness), Candidate A is decisively superior.*

- **Game 33** · f vs i → **f** wins (conf=0.95)  
  *Candidate A correctly identifies the material as hexagonal boron nitride and properly assigns the dominant E₂g mode — the central task — with coherent, physically grounded reasoning, making only a secondary error in layer-count assignment. Candidate B misidentifies the material entirely as graphitic carbon despite contradictory evidence within its own reasoning chain, providing no actionable or correct characterisation of the h-BN sample. Candidate A is unambiguously superior across all evaluation dimensions.*

- **Game 34** · g vs h → **h** wins (conf=0.78)  
  *Both candidates failed the core task of identifying h-BN, but Candidate B is clearly superior in reasoning quality, uncertainty quantification, and methodological rigour. Candidate A's assignment of the 1369 cm⁻¹ peak to graphene's D band at 90% confidence is scientifically indefensible and internally contradictory, while B at least systematically evaluated alternatives, reported FWHM, and expressed appropriate uncertainty. Neither output is satisfactory against the ground truth, but B's errors are of omission rather than commission.*

- **Game 35** · g vs i → **i** wins (conf=0.65)  
  *Both candidates fundamentally failed to identify the material as h-BN, which is the critical error. However, Candidate B demonstrates superior scientific reasoning by flagging the absence of the G-band as inconsistent with a carbon assignment, expressing appropriate uncertainty with a lower confidence score (0.62 vs 0.9), and considering multiple alternative hypotheses. Candidate A's overconfident misclassification as monolayer graphene with circular reasoning and no acknowledgment of spectral inconsistencies makes it the clearly weaker response, even though neither model arrived at the correct answer.*

- **Game 36** · h vs i → **draw** wins (conf=0.72)  
  *Both candidates made the identical and critical error of misassigning the h-BN E₂g band (~1369 cm⁻¹) to a carbon D-band, and neither considered hexagonal boron nitride at any point in their analysis. The marginal differences—A's use of 'unknown' as a fallback versus B's less credible inclusion of polyethylene—do not constitute a meaningful scientific advantage for either model, making a draw the most honest outcome.*
