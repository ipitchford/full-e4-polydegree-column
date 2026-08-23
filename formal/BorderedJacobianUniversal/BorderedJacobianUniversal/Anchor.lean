/-
Copyright (c) 2026 HC4JC2 successor project. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: HC4JC2 successor project contributors
-/
import BorderedJacobianUniversal.Multiplication
import Mathlib.RingTheory.Polynomial.Resultant.Basic

/-!
# The anchored maximal minor and the Sylvester resultant

Deleting the leading `aᵣ` column leaves a square matrix whose last row has a
single nonzero entry.  The complementary top-left minor is Mathlib's Sylvester
matrix for `(A,B)`.  Resultant commutativity converts this to the manuscript's
convention `Res(B,A)` and accounts for the sign `(-1)^(r*s)`.
-/

namespace BorderedJacobianUniversal

open Finset Matrix Polynomial

variable {R : Type*} [CommRing R]

/-- A bounded coefficient vector as a polynomial. -/
noncomputable def polyOfCoeffs (n : ℕ) (c : Fin (n + 1) → R) : R[X] :=
  ∑ i : Fin (n + 1), Polynomial.monomial (i : ℕ) (c i)

@[simp]
theorem polyOfCoeffs_coeff (n k : ℕ) (c : Fin (n + 1) → R) :
    (polyOfCoeffs n c).coeff k = coeffExt c k := by
  classical
  by_cases hk : k < n + 1
  · rw [polyOfCoeffs]
    rw [Polynomial.finsetSum_coeff Finset.univ
      (fun i : Fin (n + 1) ↦ Polynomial.monomial (i : ℕ) (c i)) k]
    simp only [Polynomial.coeff_monomial]
    rw [Fintype.sum_eq_single ⟨k, hk⟩]
    · simp [coeffExt, hk]
    · intro i hi
      have hik : (i : ℕ) ≠ k := by
        intro hval
        apply hi
        exact Fin.ext hval
      simp [hik]
  · rw [polyOfCoeffs]
    rw [Polynomial.finsetSum_coeff Finset.univ
      (fun i : Fin (n + 1) ↦ Polynomial.monomial (i : ℕ) (c i)) k]
    simp only [Polynomial.coeff_monomial]
    rw [Fintype.sum_eq_zero]
    · simp [coeffExt, hk]
    · intro i
      have hik : (i : ℕ) ≠ k := by omega
      simp [hik]

/-- The paper's resultant convention: `Res(B,A)`. -/
noncomputable def resultantBA (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) : R :=
  Polynomial.resultant (polyOfCoeffs s b) (polyOfCoeffs r a) s r

/-- The column occupied by the leading coefficient `aᵣ`. -/
def aLeadCol (r s : ℕ) : Fin (r + s + 2) := ⟨r, by omega⟩

/-- Numerical action of the embedding that skips the `aᵣ` column. -/
@[simp]
theorem aLeadCol_succAbove_val (r s : ℕ) (j : Fin (r + s + 1)) :
    ((aLeadCol r s).succAbove j : ℕ) =
      if (j : ℕ) < r then (j : ℕ) else (j : ℕ) + 1 := by
  by_cases hjr : (j : ℕ) < r
  · have hlt : j.castSucc < aLeadCol r s := by
      apply Fin.mk_lt_mk.mpr
      simpa [aLeadCol] using hjr
    rw [Fin.succAbove_of_castSucc_lt _ _ hlt]
    simp [hjr]
  · have hle : aLeadCol r s ≤ j.castSucc := by
      apply Fin.mk_le_mk.mpr
      omega
    rw [Fin.succAbove_of_le_castSucc _ _ hle]
    simp [hjr]

/-- Delete the `aᵣ` column from the multiplication Jacobian. -/
def anchorMinor (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    Matrix (Fin (r + s + 1)) (Fin (r + s + 1)) R :=
  (mulJac r s a b).submatrix id (aLeadCol r s).succAbove

/-- Delete the last row and last column from the anchored minor. -/
def anchorCore (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    Matrix (Fin (r + s)) (Fin (r + s)) R :=
  (anchorMinor r s a b).submatrix (Fin.last (r + s)).succAbove
    (Fin.last (r + s)).succAbove

/-- The anchor core is exactly Mathlib's Sylvester matrix for `(A,B)`. -/
theorem anchorCore_eq_sylvester (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    anchorCore r s a b =
      Polynomial.sylvester (polyOfCoeffs r a) (polyOfCoeffs s b) r s := by
  ext i j
  induction j using Fin.addCases with
  | left j =>
      have hi : (i : ℕ) < r + s := i.isLt
      have hj : (j : ℕ) < r := j.isLt
      by_cases hji : (j : ℕ) ≤ (i : ℕ)
      · by_cases his : (i : ℕ) ≤ (j : ℕ) + s
        · simp [anchorCore, anchorMinor, mulJac, Polynomial.sylvester,
            aLeadCol_succAbove_val, Set.mem_Icc, hji, his, hj]
        · have hz : coeffExt b ((i : ℕ) - (j : ℕ)) = 0 :=
            coeffExt_eq_zero_of_le b (by omega)
          simp [anchorCore, anchorMinor, mulJac, Polynomial.sylvester,
            aLeadCol_succAbove_val, Set.mem_Icc, hji, his, hj, hz]
      · simp [anchorCore, anchorMinor, mulJac, Polynomial.sylvester,
          aLeadCol_succAbove_val, Set.mem_Icc, hji, hj]
  | right j =>
      have hi : (i : ℕ) < r + s := i.isLt
      have hj : (j : ℕ) < s := j.isLt
      by_cases hji : (j : ℕ) ≤ (i : ℕ)
      · by_cases hir : (i : ℕ) ≤ (j : ℕ) + r
        · simp [anchorCore, anchorMinor, mulJac, Polynomial.sylvester,
            aLeadCol_succAbove_val, Set.mem_Icc, hji, hir]
        · have hz : coeffExt a ((i : ℕ) - (j : ℕ)) = 0 :=
            coeffExt_eq_zero_of_le a (by omega)
          simp [anchorCore, anchorMinor, mulJac, Polynomial.sylvester,
            aLeadCol_succAbove_val, Set.mem_Icc, hji, hir, hz]
      · simp [anchorCore, anchorMinor, mulJac, Polynomial.sylvester,
          aLeadCol_succAbove_val, Set.mem_Icc, hji]

/-- Every nonfinal entry of the last anchor row is zero. -/
theorem anchorMinor_last_row_ne_last (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (j : Fin (r + s + 1))
    (hj : j ≠ Fin.last (r + s)) :
    anchorMinor r s a b (Fin.last (r + s)) j = 0 := by
  have hjlt : (j : ℕ) < r + s := by
    exact (Fin.lt_last_iff_ne_last.mpr hj)
  by_cases hjr : (j : ℕ) < r
  · have hz : coeffExt b (r + s - (j : ℕ)) = 0 :=
      coeffExt_eq_zero_of_le b (by omega)
    simp [anchorMinor, mulJac, aLeadCol_succAbove_val, hjr, hz]
    omega
  · simp only [anchorMinor, Matrix.submatrix_apply, mulJac,
      aLeadCol_succAbove_val, hjr, ↓reduceIte, Order.add_one_le_iff,
      Nat.reduceSubDiff, id_eq, Fin.val_last, tsub_le_iff_right,
      ite_eq_right_iff]
    intro _
    apply coeffExt_eq_zero_of_le
    omega

/-- The final entry of the last anchor row is `aᵣ`. -/
theorem anchorMinor_last_last (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    anchorMinor r s a b (Fin.last (r + s)) (Fin.last (r + s)) = a (Fin.last r) := by
  have hfin : (⟨r, by omega⟩ : Fin (r + 1)) = Fin.last r := Fin.ext rfl
  simpa [anchorMinor, mulJac, aLeadCol_succAbove_val, coeffExt] using congrArg a hfin

/-- Determinant of the anchored minor before swapping the resultant arguments. -/
theorem det_anchorMinor_eq_resultantAB_mul (r s : ℕ)
    (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    (anchorMinor r s a b).det =
      Polynomial.resultant (polyOfCoeffs r a) (polyOfCoeffs s b) r s * a (Fin.last r) := by
  rw [Matrix.det_succ_row (anchorMinor r s a b) (Fin.last (r + s))]
  rw [Fintype.sum_eq_single (Fin.last (r + s))]
  · rw [anchorMinor_last_last]
    have hsign :
        ((-1 : R) ^ ((r + s) + (r + s))) = 1 := by
      rw [show (r + s) + (r + s) = 2 * (r + s) by omega, pow_mul]
      simp
    simp only [Fin.val_last, hsign, one_mul]
    change a (Fin.last r) * (anchorCore r s a b).det =
      Polynomial.resultant (polyOfCoeffs r a) (polyOfCoeffs s b) r s * a (Fin.last r)
    rw [anchorCore_eq_sylvester]
    simp [Polynomial.resultant, mul_comm]
  · intro j hj
    simp [anchorMinor_last_row_ne_last r s a b j hj]

/-- The load-bearing anchor identity in the manuscript's `Res(B,A)` convention. -/
theorem det_anchorMinor (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    (anchorMinor r s a b).det =
      (-1) ^ (r * s) * resultantBA r s a b * a (Fin.last r) := by
  rw [det_anchorMinor_eq_resultantAB_mul]
  rw [Polynomial.resultant_comm]
  simp [resultantBA, mul_assoc]

section Receipts

#print axioms polyOfCoeffs_coeff
#print axioms anchorCore_eq_sylvester
#print axioms det_anchorMinor_eq_resultantAB_mul
#print axioms det_anchorMinor

end Receipts

end BorderedJacobianUniversal
