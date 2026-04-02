# Hexagonal Boron Nitride (h-BN) ELO Ranking — Final Report

**Sample:** hbn_bulk_001 (Bulk h-BN, orientation 001)  
**Judge:** grok-4.20-0309-reasoning  
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
| 3 | **e** | 71.6 | 5 | 1 | 2 | 69% |
| 4 | **f** | 71.2 | 5 | 1 | 2 | 69% |
| 5 | **c** | 51.2 | 4 | 0 | 4 | 50% |
| 6 | **i** | 21.7 | 1 | 2 | 5 | 25% |
| 7 | **h** | 21.2 | 1 | 2 | 5 | 25% |
| 8 | **a** | 14.4 | 0 | 3 | 5 | 19% |
| 9 | **g** | 0.0 | 0 | 1 | 7 | 6% |

## Match Results

- **Game 1** · a vs b → **b** wins (conf=0.92)  
  *B is scientifically correct on material identification and provides accurate Raman reasoning for h-BN's E₂g mode while A completely mistakes it for graphite. B better matches ground truth on all key dimensions despite a small FWHM note.*

- **Game 2** · a vs c → **c** wins (conf=0.78)  
  *B is better overall as it correctly references the E2g mode, distinguishes from graphene signatures, and ranks h-BN highest despite imperfect final label. A shows fundamental misunderstanding of h-BN Raman physics with no recovery.*

- **Game 3** · a vs d → **d** wins (conf=0.92)  
  *B matches ground truth on material, peak assignment, and key diagnostics while properly excluding carbon; A is entirely erroneous on the core identification. B's chain-of-thought is logically sound and free of hallucinations.*

- **Game 4** · a vs e → **e** wins (conf=0.82)  
  *B correctly identifies the material as h-BN and the dominant peak as the E₂g mode, while A hallucinates a graphite D-band. Although B errs on monolayer vs bulk, this is minor compared with A's total misclassification. Overall B is far closer to the ground-truth reference.*

- **Game 5** · a vs f → **f** wins (conf=0.85)  
  *B alone identifies the material as h-BN and correctly invokes the E₂g mode as the sole prominent feature, while A hallucinates a graphite D-band interpretation incompatible with the observed single-peak spectrum. Although B incorrectly labels the sample monolayer rather than bulk, this is a secondary error compared with A's total misclassification. B is therefore the clearly superior output on scientific correctness, reasoning quality, and overall fidelity to the ground-truth h-BN signature.*

- **Game 6** · a vs g → **draw** wins (conf=0.85)  
  *Neither candidate recognized the material as h-BN or the peak as the E₂g band; both exhibit fundamental scientific errors and lack any correct h-BN reasoning. The outputs are equally poor across all evaluated dimensions.*

- **Game 7** · a vs h → **draw** wins (conf=0.85)  
  *Both candidates completely failed to recognize the h-BN E₂g band at ~1366 cm⁻¹ and confused the spectrum with carbon materials. Their chains of thought lack any Raman physics specific to BN or 2D materials. The errors are fundamental and comparable, resulting in a draw.*

- **Game 8** · a vs i → **draw** wins (conf=0.85)  
  *Neither model recognized the E₂g band of hexagonal boron nitride or applied appropriate 2D-materials Raman knowledge; both applied identical carbon misinterpretation. They are equally flawed across all evaluation dimensions.*

- **Game 9** · b vs c → **b** wins (conf=0.88)  
  *A is scientifically correct on the core identification and produces a high-confidence, logically sound output aligned with ground truth. B fails to select h-BN as the answer, mixes it with graphene D-band confusion, and shows factual errors on phonon mode labels. Overall, A is clearly superior on correctness, reasoning quality, and completeness.*

- **Game 10** · b vs d → **d** wins (conf=0.78)  
  *B is better overall: it avoids A's explicit contradiction of GT FWHM guidelines for bulk vs monolayer and more accurately interprets the observed broad peak as non-ideal crystallinity. Both succeed on core h-BN identification and graphene exclusion, but A's hallucination on layer-number physics is a significant flaw.*

- **Game 11** · b vs e → **b** wins (conf=0.65)  
  *A is better overall because it matches the GT sample classification target of bulk h-BN, includes stacking order, and avoids the critical layer-number error of B. Although both have flaws (A on FWHM expectations, B on layer), A aligns closer to the provided ground truth reference.*

- **Game 12** · b vs f → **b** wins (conf=0.72)  
  *A is superior overall because it correctly identifies the bulk morphology matching the ground truth sample label, despite a secondary FWHM misconception. B's layer assignment error is more fundamental for this specific spectrum. Both show strong Raman reasoning and high confidence, but A's final classification aligns better with the provided GT.*

- **Game 13** · b vs g → **b** wins (conf=0.88)  
  *A is scientifically far superior, correctly recognizing the hallmark single E₂g peak of h-BN and ruling out graphene, while B fundamentally mistakes the spectrum for graphene's D-band. The minor FWHM interpretation flaw in A does not outweigh B's complete misidentification. A provides complete, high-confidence output aligned with ground truth.*

- **Game 14** · b vs h → **b** wins (conf=0.95)  
  *A is scientifically accurate on every key point (material, peak assignment, ruling out graphene) and delivers a complete, high-confidence classification aligned with ground truth. B fails at the first step by misidentifying h-BN as disordered carbon. The large correctness gap makes A the clear winner.*

- **Game 15** · b vs i → **b** wins (conf=0.88)  
  *A is scientifically correct on material identification and provides logical Raman-specific reasoning that aligns with ground truth, despite one FWHM nuance error. B fails at the most basic step by confusing h-BN E₂g with carbon D-band. A is clearly superior overall.*

- **Game 16** · c vs d → **d** wins (conf=0.88)  
  *B is scientifically accurate on material and mode, shows better Raman-specific reasoning, and delivers a clear classification aligned with ground truth. A fails on primary identification and internal consistency despite partial credit for considering h-BN.*

- **Game 17** · c vs e → **e** wins (conf=0.72)  
  *B correctly identifies the material as h-BN with focused Raman reasoning and high clarity, while A selects the wrong class despite noting h-BN as strong alternative. B's monolayer assignment deviates from GT bulk label but aligns better with observed FWHM=28 cm⁻¹ and literature; overall B is scientifically closer and higher quality.*

- **Game 18** · c vs f → **f** wins (conf=0.72)  
  *B is better overall: correctly identifies h-BN as primary material and properly distinguishes from graphene/carbon, aligning with GT on E2g dominance. A's primary graphitic prediction and internal contradictions outweigh its uncertainty acknowledgment. B's monolayer claim is a flaw but less severe than A's material error.*

- **Game 19** · c vs g → **c** wins (conf=0.82)  
  *A demonstrates substantive Raman knowledge of h-BN E2g, correctly flags distinguishing features and lists h-BN first, while B is confidently wrong on graphene. A is better overall despite imperfect final label.*

- **Game 20** · c vs h → **c** wins (conf=0.78)  
  *A correctly flags the E₂g mode and lists h-BN as the leading candidate with appropriate caveats, while B completely fails to recognize h-BN; neither output is perfect, but A is clearly superior across all evaluation dimensions.*

- **Game 21** · c vs i → **c** wins (conf=0.75)  
  *A demonstrates better scientific awareness of h-BN's E2g mode and properly contrasts it with carbon D-band in reasoning, despite contradictory final output. B completely misses the h-BN possibility and shows no Raman-specific differentiation. A is therefore superior overall on correctness and reasoning quality.*

- **Game 22** · d vs e → **d** wins (conf=0.75)  
  *A matches GT on bulk classification, avoids B's layer-number hallucination, and provides stronger alternative-material elimination. B's monolayer claim directly contradicts the supplied ground-truth sample type despite similar confidence.*

- **Game 23** · d vs f → **d** wins (conf=0.75)  
  *A is superior overall: accurate bulk assignment, no hallucinations on peak-shift layer dependence, and better alignment with GT's emphasis on FWHM and single E2g peak. B's monolayer error is a clear scientific mistake for the provided bulk h-BN reference spectrum.*

- **Game 24** · d vs g → **d** wins (conf=0.92)  
  *A is scientifically accurate on all key points (material, mode, bulk assignment) with solid chain-of-thought that correctly differentiates from graphene; B is fundamentally wrong on material identification and band assignment. A provides clear, complete classification aligned with ground truth while B does not.*

- **Game 25** · d vs h → **d** wins (conf=0.92)  
  *A accurately identifies the material, peak assignment, and quality indicators consistent with GT; B completely misclassifies the spectrum as disordered carbon. A demonstrates proper Raman knowledge for 2D materials while B does not.*

- **Game 26** · d vs i → **d** wins (conf=0.92)  
  *A is clearly superior: it matches ground truth on material, peak assignment, and differentiation from carbon, while B fails at the most basic identification step. A's reasoning is grounded in h-BN Raman signatures and its confidence is appropriately high.*

- **Game 27** · e vs f → **draw** wins (conf=0.75)  
  *Both models make identical core errors on layer number (monolayer vs GT bulk) and over-interpret the 3 cm^-1 shift; reasoning quality, graphene distinction, and output clarity are essentially equal, so neither is superior overall.*

- **Game 28** · e vs g → **e** wins (conf=0.85)  
  *A accurately detects the h-BN E2g signature with supporting physics and rules out graphene, outweighing its layer-number discrepancy with GT. B's graphene misclassification is a critical scientific error. A is superior on all evaluation dimensions.*

- **Game 29** · e vs h → **e** wins (conf=0.88)  
  *A accurately recognizes the characteristic h-BN E2g peak and rules out graphene, aligning closely with ground truth on material and peak assignment. B's carbon misidentification is a critical error. The layer discrepancy in A is minor compared to B's complete failure on material identification.*

- **Game 30** · e vs i → **e** wins (conf=0.82)  
  *A accurately recognizes the spectrum as h-BN via the E₂g peak at 1369 cm⁻¹ with appropriate FWHM and rules out carbon, aligning with the provided GT Raman signature for h-BN despite a monolayer vs bulk discrepancy. B completely misclassifies it as disordered carbon, which is inconsistent with h-BN physics and the absence of a G band. Overall A is the clearly superior output.*

- **Game 31** · f vs g → **f** wins (conf=0.82)  
  *A correctly classifies the material as hexagonal boron nitride, recognizes the E2g mode, and methodically excludes carbon alternatives, aligning closely with GT except for the layer assignment. B confuses the spectrum with graphene's defect band and shows no understanding of h-BN Raman signatures. Overall A is substantially more accurate and useful.*

- **Game 32** · f vs h → **f** wins (conf=0.82)  
  *A is superior overall by correctly recognizing h-BN and the E2g mode with sound Raman reasoning, while B fails at the most basic step of material identification. The layer-number discrepancy in A is minor compared to B's complete misclassification as amorphous carbon. This aligns with ground-truth expectations on material and primary peak.*

- **Game 33** · f vs i → **f** wins (conf=0.82)  
  *A accurately detects h-BN E2g signature, correctly excludes carbon, and provides solid Raman-based reasoning. B's carbon misclassification is a basic error for this spectrum. Although A wrongly assigns monolayer, it is far superior overall on all evaluation dimensions.*

- **Game 34** · g vs h → **h** wins (conf=0.75)  
  *Neither model identified h-BN, making both scientifically wrong. B is better overall due to more rigorous, less hallucinatory chain-of-thought that properly notes peak width and missing bands, plus appropriately lower confidence. A is overconfident in a classic h-BN/graphene confusion.*

- **Game 35** · g vs i → **i** wins (conf=0.75)  
  *Neither identified h-BN or the E₂g mode, so both fail scientifically. B is superior overall due to more detailed, logically structured reasoning, explicit consideration of peak width and absent companion bands, and appropriately lower confidence. A’s output is shallow and internally inconsistent.*

- **Game 36** · h vs i → **draw** wins (conf=0.85)  
  *Both models made the identical core mistake of mistaking h-BN's E₂g phonon for a carbon D-band, showing equivalent lack of domain knowledge. No meaningful difference in reasoning quality or completeness exists; both are equally poor.*
