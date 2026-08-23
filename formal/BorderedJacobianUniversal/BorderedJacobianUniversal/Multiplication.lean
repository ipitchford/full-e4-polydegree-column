/-
Copyright (c) 2026 HC4JC2 successor project. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: HC4JC2 successor project contributors
-/
import BorderedJacobianUniversal.General
import Mathlib.Algebra.BigOperators.Intervals

/-!
# The convolution Jacobian and its canonical kernel vector

The two coefficient blocks are first indexed by a sum type.  This exposes the
convolution symmetry without any casts.  An explicit order-preserving
equivalence then gives the single finite index used by the bordered determinant.
-/

namespace BorderedJacobianUniversal

open Finset Matrix

variable {R : Type*} [CommRing R]

/-- Extend a coefficient vector by zero outside its declared degree bound. -/
def coeffExt {n : ℕ} (c : Fin (n + 1) → R) : ℕ → R :=
  fun i ↦ if h : i < n + 1 then c ⟨i, h⟩ else 0

@[simp]
theorem coeffExt_apply_fin {n : ℕ} (c : Fin (n + 1) → R) (i : Fin (n + 1)) :
    coeffExt c i = c i := by
  unfold coeffExt
  rw [dif_pos i.isLt]

@[simp]
theorem coeffExt_eq_zero_of_le {n i : ℕ} (c : Fin (n + 1) → R)
    (h : n + 1 ≤ i) : coeffExt c i = 0 := by
  simp [coeffExt, Nat.not_lt.mpr h]

/-- A bounded finite sum may be extended to the whole convolution range because
`coeffExt` vanishes beyond the coefficient vector. -/
theorem sum_fin_if_le_eq_range {n k : ℕ} (c : Fin (n + 1) → R) (f : ℕ → R) :
    ∑ i : Fin (n + 1), (if (i : ℕ) ≤ k then f i * c i else 0) =
      ∑ i ∈ range (k + 1), f i * coeffExt c i := by
  simp_rw [← coeffExt_apply_fin c]
  rw [Fin.sum_univ_eq_sum_range
    (fun i ↦ if i ≤ k then f i * coeffExt c i else 0) (n + 1)]
  rcases le_total (n + 1) (k + 1) with hnk | hkn
  · calc
      ∑ i ∈ range (n + 1), (if i ≤ k then f i * coeffExt c i else 0) =
          ∑ i ∈ range (n + 1), f i * coeffExt c i := by
            apply sum_congr rfl
            intro i hi
            have hin : i < n + 1 := mem_range.mp hi
            have hik : i ≤ k := by omega
            simp [hik]
      _ = ∑ i ∈ range (k + 1), f i * coeffExt c i := by
            apply sum_subset (range_mono hnk)
            intro i hik hin
            have hni : n + 1 ≤ i := by
              simpa [mem_range, Nat.not_lt] using hin
            simp [coeffExt_eq_zero_of_le c hni]
  · calc
      ∑ i ∈ range (n + 1), (if i ≤ k then f i * coeffExt c i else 0) =
          ∑ i ∈ range (k + 1), (if i ≤ k then f i * coeffExt c i else 0) := by
            symm
            apply sum_subset (range_mono hkn)
            intro i hin hik
            have hki : k < i := by
              simpa [mem_range, Nat.not_lt] using hik
            simp [Nat.not_le.mpr hki]
      _ = ∑ i ∈ range (k + 1), f i * coeffExt c i := by
            apply sum_congr rfl
            intro i hi
            have hik : i ≤ k := Nat.lt_succ_iff.mp (mem_range.mp hi)
            have hin : i < n + 1 := lt_of_lt_of_le (mem_range.mp hi) hkn
            simp [hik, coeffExt, hin]

/-- Finite convolution is symmetric over a commutative ring. -/
theorem convolution_comm (a b : ℕ → R) (k : ℕ) :
    ∑ i ∈ range (k + 1), a i * b (k - i) =
      ∑ j ∈ range (k + 1), b j * a (k - j) := by
  rw [← Finset.sum_range_reflect (fun j ↦ b j * a (k - j)) (k + 1)]
  apply sum_congr rfl
  intro i hi
  have hik : i ≤ k := Nat.lt_succ_iff.mp (mem_range.mp hi)
  simp [Nat.sub_sub_self hik, mul_comm]

/-- The Jacobian of coefficient multiplication, with the two input blocks kept
as a sum type. -/
def mulJacSum (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    Matrix (Fin (r + s + 1)) (Fin (r + 1) ⊕ Fin (s + 1)) R :=
  fun k col ↦ match col with
    | Sum.inl i => if (i : ℕ) ≤ (k : ℕ) then coeffExt b ((k : ℕ) - (i : ℕ)) else 0
    | Sum.inr j => if (j : ℕ) ≤ (k : ℕ) then coeffExt a ((k : ℕ) - (j : ℕ)) else 0

/-- Relative scaling of the two factors. -/
def kappaSum (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    Fin (r + 1) ⊕ Fin (s + 1) → R
  | Sum.inl i => a i
  | Sum.inr j => -b j

/-- The multiplication Jacobian kills relative scaling, in every commutative
ring and in all boundary degrees. -/
theorem mulJacSum_mulVec_kappaSum (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    mulJacSum r s a b *ᵥ kappaSum r s a b = 0 := by
  funext k
  simp only [Matrix.mulVec, dotProduct, Fintype.sum_sum_type, mulJacSum, kappaSum]
  simp_rw [ite_mul, zero_mul]
  rw [sum_fin_if_le_eq_range a (fun i ↦ coeffExt b ((k : ℕ) - i))]
  have hsecond :
      (∑ j : Fin (s + 1),
        (if (j : ℕ) ≤ (k : ℕ) then
          coeffExt a ((k : ℕ) - (j : ℕ)) * -b j else 0)) =
        -(∑ j ∈ range ((k : ℕ) + 1),
          coeffExt a ((k : ℕ) - j) * coeffExt b j) := by
    calc
      _ = ∑ j : Fin (s + 1),
          (if (j : ℕ) ≤ (k : ℕ) then
            (-coeffExt a ((k : ℕ) - (j : ℕ))) * b j else 0) := by
              apply Finset.sum_congr rfl
              intro j _
              split_ifs <;> ring
      _ = ∑ j ∈ range ((k : ℕ) + 1),
          (-coeffExt a ((k : ℕ) - j)) * coeffExt b j :=
            sum_fin_if_le_eq_range b
              (fun j ↦ -coeffExt a ((k : ℕ) - j))
      _ = -(∑ j ∈ range ((k : ℕ) + 1),
          coeffExt a ((k : ℕ) - j) * coeffExt b j) := by
            rw [← Finset.sum_neg_distrib]
            apply Finset.sum_congr rfl
            intro j _
            ring
  rw [hsecond]
  simp only [Pi.zero_apply]
  rw [← sub_eq_add_neg]
  apply sub_eq_zero.mpr
  simpa [mul_comm] using convolution_comm (coeffExt a) (coeffExt b) (k : ℕ)

/-- The order-preserving equivalence from the two coefficient blocks to the
single column order `a₀,…,aᵣ,b₀,…,bₛ`. -/
def coeffOrderEquiv (r s : ℕ) :
    Fin (r + 1) ⊕ Fin (s + 1) ≃ Fin (r + s + 2) :=
  finSumFinEquiv.trans (finCongr (by omega))

@[simp]
theorem coeffOrderEquiv_inl_val (r s : ℕ) (i : Fin (r + 1)) :
    ((coeffOrderEquiv r s) (Sum.inl i) : ℕ) = i := by
  simp [coeffOrderEquiv, finSumFinEquiv]

@[simp]
theorem coeffOrderEquiv_inr_val (r s : ℕ) (j : Fin (s + 1)) :
    ((coeffOrderEquiv r s) (Sum.inr j) : ℕ) = r + 1 + j := by
  simp [coeffOrderEquiv, finSumFinEquiv]

/-- The same Jacobian in the manuscript's single ordered finite index. -/
def mulJac (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    Matrix (Fin (r + s + 1)) (Fin (r + s + 2)) R :=
  fun k col ↦
    if (col : ℕ) ≤ r then
      if (col : ℕ) ≤ (k : ℕ) then coeffExt b ((k : ℕ) - (col : ℕ)) else 0
    else
      if (col : ℕ) - (r + 1) ≤ (k : ℕ) then
        coeffExt a ((k : ℕ) - ((col : ℕ) - (r + 1))) else 0

/-- The relative-scaling vector in the same ordered finite index. -/
def kappa (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    Fin (r + s + 2) → R :=
  fun col ↦
    if h : (col : ℕ) ≤ r then a ⟨col, by omega⟩
    else -b ⟨(col : ℕ) - (r + 1), by omega⟩

@[simp]
theorem mulJac_orderEquiv (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (k : Fin (r + s + 1))
    (col : Fin (r + 1) ⊕ Fin (s + 1)) :
    mulJac r s a b k (coeffOrderEquiv r s col) = mulJacSum r s a b k col := by
  cases col with
  | inl i =>
      have hir : (i : ℕ) ≤ r := Nat.le_of_lt_succ i.isLt
      simp [mulJac, mulJacSum, hir]
  | inr j =>
      have hrj : ¬(r + 1 + (j : ℕ) ≤ r) := by omega
      have hsub : r + 1 + (j : ℕ) - (r + 1) = (j : ℕ) := by omega
      simp [mulJac, mulJacSum, coeffOrderEquiv_inr_val, hrj, hsub]

@[simp]
theorem kappa_orderEquiv (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (col : Fin (r + 1) ⊕ Fin (s + 1)) :
    kappa r s a b (coeffOrderEquiv r s col) = kappaSum r s a b col := by
  cases col with
  | inl i =>
      have hir : (i : ℕ) ≤ r := Nat.le_of_lt_succ i.isLt
      simp [kappa, kappaSum, hir]
  | inr j =>
      have hrj : ¬(r + 1 + (j : ℕ) ≤ r) := by omega
      have hsub : r + 1 + (j : ℕ) - (r + 1) = (j : ℕ) := by omega
      simp [kappa, kappaSum, coeffOrderEquiv_inr_val, hrj, hsub]

/-- Ordered-index form of the universal relative-scaling kernel identity. -/
theorem mulJac_mulVec_kappa (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    mulJac r s a b *ᵥ kappa r s a b = 0 := by
  funext k
  change (∑ col : Fin (r + s + 2),
    mulJac r s a b k col * kappa r s a b col) = 0
  calc
    _ = ∑ col : Fin (r + 1) ⊕ Fin (s + 1),
        mulJac r s a b k (coeffOrderEquiv r s col) *
          kappa r s a b (coeffOrderEquiv r s col) :=
            (Equiv.sum_comp (coeffOrderEquiv r s)
              (fun col ↦ mulJac r s a b k col * kappa r s a b col)).symm
    _ = ∑ col : Fin (r + 1) ⊕ Fin (s + 1),
        mulJacSum r s a b k col * kappaSum r s a b col := by
          apply Finset.sum_congr rfl
          intro col _
          rw [mulJac_orderEquiv, kappa_orderEquiv]
    _ = 0 := by
      have h := congrFun (mulJacSum_mulVec_kappaSum r s a b) k
      simpa [Matrix.mulVec, dotProduct] using h

section Receipts

#print axioms sum_fin_if_le_eq_range
#print axioms convolution_comm
#print axioms mulJacSum_mulVec_kappaSum
#print axioms mulJac_mulVec_kappa

end Receipts

end BorderedJacobianUniversal
