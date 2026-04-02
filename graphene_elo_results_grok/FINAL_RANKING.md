# Graphene ELO Ranking — Final Report

**Sample:** mono_g_cu_001 (Monolayer graphene on Cu)  
**Judge:** grok-4.20-0309-reasoning  
**ELO range:** 0.0–100.0 · Start: 50.0 · K=16  
**Total games played:** 36  

## Ground Truth
```
GROUND TRUTH — Graphene Sample (mono_g_cu_001)
===============================================
Sample type       : Monolayer graphene grown by CVD on copper foil (Cu 001)
Abbreviation      : mono_g_cu_001

Expected Raman signature
  D  band  (~1350 cm⁻¹) : Defect-activated; should be LOW or absent in
                           high-quality monolayer graphene.
  G  band  (~1580 cm⁻¹) : E₂g phonon at Γ point; should be present and
                           moderately intense.
  2D band  (~2700 cm⁻¹) : Overtone of D; DOMINANT peak for monolayer —
                           I(2D)/I(G) > 2 is the canonical monolayer criterion.
  D' band  (~1620 cm⁻¹) : Defect-related shoulder on G; should be absent
                           in pristine graphene.

Key quality indicators
  • 2D peak: single Lorentzian, FWHM ≈ 25–35 cm⁻¹ for monolayer
  • I(2D)/I(G) ratio > 2 confirms monolayer character
  • Low D-band intensity → minimal defect density
  • G-band position ~1580 cm⁻¹ (strain shifts it slightly)
  • No D' band → absence of edge/grain-boundary defects

Classification target : GRAPHENE (monolayer)
Substrate            : Copper (Cu), orientation 001
```

## Final Rankings

| Rank | Model | ELO | W | D | L | Win% |
|------|-------|-----|---|---|---|------|
| 1 | **e** | 100.0 | 7 | 1 | 0 | 94% |
| 2 | **f** | 99.6 | 7 | 1 | 0 | 94% |
| 3 | **c** | 79.1 | 6 | 0 | 2 | 75% |
| 4 | **i** | 57.6 | 4 | 1 | 3 | 56% |
| 5 | **b** | 57.6 | 4 | 1 | 3 | 56% |
| 6 | **a** | 36.1 | 3 | 0 | 5 | 38% |
| 7 | **h** | 14.4 | 1 | 1 | 6 | 19% |
| 8 | **d** | 14.4 | 1 | 1 | 6 | 19% |
| 9 | **g** | 0.0 | 0 | 0 | 8 | 0% |

## Match Results

- **Game 1** · a vs b → **b** wins (conf=0.75)  
  *B is better overall due to scientifically accurate peak identification and logical Raman analysis, while A contains fundamental errors that invalidate its conclusions. Neither fully matches GT substrate or monolayer label, but B's physics is sound.*

- **Game 2** · a vs c → **c** wins (conf=0.85)  
  *B is superior overall with correct spectral interpretation, proper band identification, defect assessment, and use of I(2D)/I(G) and FWHM, despite layer/substrate mismatch with GT. A's complete misassignment of major peaks renders its output scientifically invalid.*

- **Game 3** · a vs d → **a** wins (conf=0.70)  
  *A is closer to truth by identifying sp² carbon and the 2D band despite wrong labels and bulk conclusion; B's silicon assignment is fundamentally incompatible with the graphene ground truth. Both fail basic correctness but A better preserves Raman carbon signatures.*

- **Game 4** · a vs e → **e** wins (conf=0.88)  
  *B is superior overall with accurate material identification, correct G/2D assignments, and logically sound Raman analysis matching GT's graphene target. A hallucinates band identities and wrongly concludes bulk graphite, rendering it scientifically invalid for this spectrum.*

- **Game 5** · a vs f → **f** wins (conf=0.88)  
  *B alone correctly identifies the graphene G and 2D bands and reaches the ground-truth monolayer classification; A's erroneous band assignments make its output scientifically invalid. B's minor discrepancies (2D/G ratio, substrate) do not outweigh A's fundamental errors.*

- **Game 6** · a vs g → **a** wins (conf=0.75)  
  *A is better overall because it at least acknowledges sp² carbon, the 2D band, and crystalline order, while B completely misses the defining graphene signatures. Both fail scientific correctness on material and band identification, but A's output stays closer to relevant 2-D carbon physics. B's silicon conclusion is a more severe disconnect from the provided spectrum and ground truth.*

- **Game 7** · a vs h → **a** wins (conf=0.55)  
  *A is better overall because it at least detected sp² carbon and the 2D overtone, placing graphite (and few-layer graphene in top candidates) while B missed carbon entirely. However both have major scientific errors in band assignment and fail to match the monolayer graphene ground truth.*

- **Game 8** · a vs i → **i** wins (conf=0.70)  
  *B is better overall due to accurate peak identification and absence of basic errors, despite both missing the monolayer-graphene label. A's fundamental misassignment of D/G bands disqualifies it as expert Raman analysis.*

- **Game 9** · b vs c → **c** wins (conf=0.68)  
  *B is superior overall: it recognizes the spectrum as graphene on Si/SiO2 (standard practice despite GT mismatch), delivers deeper layer-number reasoning, and focuses on the 2D-material signals rather than declaring Si the main phase. Both deviate from GT on substrate and layer, but B aligns better with Raman analysis of transferred CVD graphene.*

- **Game 10** · b vs d → **b** wins (conf=0.68)  
  *A is better overall: it accurately assigns and analyzes the graphitic G/2D bands with defect/ratio insights while still acknowledging Si substrate, whereas B ignores key spectral features. Both mismatch GT on primary graphene classification, likely due to actual spectrum containing strong Si peaks unexpected for mono_g_cu_001.*

- **Game 11** · b vs e → **e** wins (conf=0.82)  
  *B aligns with the GT classification target (monolayer graphene) and applies appropriate Raman metrics for 2-D carbon, while A mislabels the sample as Si-primary. B's chain-of-thought is more complete on graphene quality indicators even though both note the Si substrate peaks.*

- **Game 12** · b vs f → **f** wins (conf=0.82)  
  *B correctly classifies the spectrum as monolayer graphene (the GT target) while treating Si as substrate, whereas A misidentifies the primary material as silicon with only contamination. B's chain-of-thought applies standard Raman metrics (absent D, 2D shape, 2D/G ratio) more appropriately for 2D-material analysis.*

- **Game 13** · b vs g → **b** wins (conf=0.82)  
  *A is superior overall for correctly recognizing and assigning all spectral features (including graphitic G/2D) with coherent reasoning; B hallucinates purity by disregarding prominent carbon bands. Neither matched the graphene ground truth, but A is far closer scientifically.*

- **Game 14** · b vs h → **b** wins (conf=0.78)  
  *Neither matches GT graphene-on-Cu classification, likely due to spectrum showing dominant Si phonon incompatible with Cu substrate. A is superior overall for accurate G/2D identification, defect assessment, and avoidance of unphysical assignments that B makes.*

- **Game 15** · b vs i → **draw** wins (conf=0.75)  
  *Neither model identified the sample as monolayer graphene on Cu as required by GT; both gave consistent, high-quality reasoning for an alternate (Si+carbon) interpretation. They are essentially equal in correctness, reasoning quality, and completeness, so declared a draw.*

- **Game 16** · c vs d → **c** wins (conf=0.88)  
  *A correctly detects and assigns all graphene bands with supporting metrics while B fails to recognize graphene on SiO2/Si; although A mismatches ground-truth layer and substrate, it is far more scientifically sound and complete than B's outright misclassification.*

- **Game 17** · c vs e → **e** wins (conf=0.68)  
  *B aligns with GT monolayer classification and correctly identifies material quality indicators while addressing instrumental effects. A misclassifies layer number despite accurate peak math. Both err on substrate, but B is superior overall on correctness to reference and reasoning coherence.*

- **Game 18** · c vs f → **f** wins (conf=0.60)  
  *Using GT as reference, B correctly labels the material as monolayer graphene while A mislabels it bilayer; both err on substrate but B's classification, confidence, and overall alignment with the provided standard are superior.*

- **Game 19** · c vs g → **c** wins (conf=0.88)  
  *A correctly identifies and assigns all major Raman features (Si + graphene G/2D) with solid physics-based reasoning while B fails to recognize the graphene component at all. Although neither fully matches GT substrate/layer, A is substantially more accurate, complete and useful overall.*

- **Game 20** · c vs h → **c** wins (conf=0.88)  
  *A correctly recognizes both the Si substrate and the graphene G/2D bands with proper assignments and quality metrics, despite layer and substrate mismatch with GT. B fails to detect graphene at all. On scientific correctness, reasoning quality and completeness A is clearly superior.*

- **Game 21** · c vs i → **c** wins (conf=0.78)  
  *A correctly detects and assigns all graphene Raman features, uses standard I(2D)/I(G) and FWHM criteria, and reports appropriate confidence with evidence. B fails to recognize the graphene as the intended material. A is superior on correctness, reasoning, and completeness despite shared substrate mismatch with GT.*

- **Game 22** · d vs e → **e** wins (conf=0.92)  
  *B alone matches the ground-truth classification target of monolayer graphene, correctly interprets all relevant peaks and quality metrics (no D, high 2D/G ratio, narrow 2D), while A fails to detect graphene. B's only flaw is calling the substrate silicon instead of copper, which is minor compared to A's total misclassification.*

- **Game 23** · d vs f → **f** wins (conf=0.82)  
  *B accurately recognizes the monolayer graphene signatures on a substrate while A fails to detect graphene at all. B's chain-of-thought is complete and physically sound; the minor 2D/G and substrate discrepancies do not outweigh A's total misclassification.*

- **Game 24** · d vs g → **d** wins (conf=0.75)  
  *A is better overall due to more detailed CoT that at least considers the graphene bands and provides clearer analysis steps, despite both being fundamentally wrong on the core classification.*

- **Game 25** · d vs h → **draw** wins (conf=0.75)  
  *Both models commit the identical fundamental error of assigning the spectrum to silicon instead of graphene, with comparable reasoning quality and completeness. Neither correctly reports monolayer indicators or band assignments per the ground truth, making them equally incorrect overall.*

- **Game 26** · d vs i → **i** wins (conf=0.75)  
  *Both fail Step 1 by not classifying as monolayer graphene on Cu, contradicting the expected dominant 2D band and low defects. B is better overall for correctly assigning the 1580/2670 cm⁻¹ features as graphitic (G/2D) rather than ignoring them, producing more complete peak lists and acknowledging contamination. This makes B's output scientifically closer despite the shared material error.*

- **Game 27** · e vs f → **draw** wins (conf=0.85)  
  *A and B are essentially identical in classification accuracy, confidence, peak lists and overall reasoning quality. Both deviate equally from GT on substrate and exact I(2D)/I(G) >2 criterion, making them tied.*

- **Game 28** · e vs g → **e** wins (conf=0.92)  
  *A is scientifically accurate on the graphene signature and layer count, follows proper Raman interpretation, and produces a complete classification; B fails to recognize the graphene peaks and misclassifies the entire spectrum. The substrate mismatch in A is minor compared to B's total omission of the analyte.*

- **Game 29** · e vs h → **e** wins (conf=0.88)  
  *A accurately recognizes the graphene Raman signature and monolayer indicators while correctly interpreting the Si substrate peaks. B fundamentally misassigns the G and 2D bands, showing a critical error in Raman interpretation. Overall A is scientifically correct, logically sound, and matches the ground-truth target of monolayer graphene.*

- **Game 30** · e vs i → **e** wins (conf=0.92)  
  *A correctly recognizes the graphene monolayer signature and reaches the ground-truth material classification; B misclassifies the entire sample as contaminated silicon. A's chain-of-thought is Raman-physics grounded while B's is not.*

- **Game 31** · f vs g → **f** wins (conf=0.92)  
  *A accurately extracts and interprets all graphene Raman signatures consistent with GT criteria (low D, clear G+2D, monolayer indicators) while B fails to recognize graphene at all. The substrate mismatch is minor compared to B's total omission of the carbon bands.*

- **Game 32** · f vs h → **f** wins (conf=0.88)  
  *A accurately detects and interprets the graphene signature while correctly using substrate peaks as context; B completely misses the graphene component. A is superior on correctness, reasoning quality, and alignment with the ground-truth classification target.*

- **Game 33** · f vs i → **f** wins (conf=0.88)  
  *A is superior on all three evaluation dimensions: it correctly recognizes and classifies the graphene spectrum while B fails at the most basic material identification. Minor discrepancies in A (ratio, substrate) do not outweigh its overall scientific accuracy and reasoning quality.*

- **Game 34** · g vs h → **h** wins (conf=0.75)  
  *Both are scientifically wrong on material identification, but B is superior in reasoning quality and completeness by systematically evaluating all observed peaks and ruling out alternatives. This makes B better overall despite the shared erroneous silicon conclusion.*

- **Game 35** · g vs i → **i** wins (conf=0.78)  
  *B is better overall because it accurately detects and assigns the graphene G and 2D bands rather than ignoring them, producing more complete and logically grounded reasoning even though both candidates wrongly conclude the material is silicon instead of monolayer graphene on Cu.*

- **Game 36** · h vs i → **i** wins (conf=0.72)  
  *Both fail Step 1 by not classifying as monolayer graphene, but B is superior in Steps 1-2 for correct G/2D band assignment and avoidance of clear scientific error on Si phonon limits. B is therefore better overall.*
