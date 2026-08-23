/-
Copyright (c) 2026 HC4JC2 successor project. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: HC4JC2 successor project contributors
-/
import Mathlib.LinearAlgebra.Matrix.Adjugate

/-!
# Rectangular cofactor and bordered-determinant identities

This file isolates the matrix algebra used by the polynomial multiplication
Jacobian.  It works over every commutative ring and includes the zero-dimensional
case.  No domain, field, characteristic, or generic-rank hypothesis is used.
-/

namespace BorderedJacobianUniversal

open Finset Matrix

variable {R : Type*}

/-- Append a final row to an `n × (n+1)` matrix. -/
def border {n : ℕ} (M : Matrix (Fin n) (Fin (n + 1)) R)
    (v : Fin (n + 1) → R) : Matrix (Fin (n + 1)) (Fin (n + 1)) R :=
  Matrix.of (Fin.snoc M v)

/-- Deleting the appended row from a bordered matrix recovers the corresponding
maximal minor of the original rectangular matrix. -/
@[simp]
theorem border_submatrix_last {n : ℕ} (M : Matrix (Fin n) (Fin (n + 1)) R)
    (v : Fin (n + 1) → R) (k : Fin (n + 1)) :
    (border M v).submatrix (Fin.last n).succAbove k.succAbove =
      M.submatrix id k.succAbove := by
  ext i j
  simp [border]

variable [CommRing R]

/-- The signed maximal-minor vector of an `n × (n+1)` matrix. -/
def cofactorVec {n : ℕ} (M : Matrix (Fin n) (Fin (n + 1)) R) :
    Fin (n + 1) → R :=
  fun k ↦ (-1) ^ (k : ℕ) * (M.submatrix id k.succAbove).det

/-- Laplace expansion along the appended row, expressed through the signed
maximal-minor vector. -/
theorem det_border {n : ℕ} (M : Matrix (Fin n) (Fin (n + 1)) R)
    (v : Fin (n + 1) → R) :
    (border M v).det =
      (-1) ^ n * ∑ k, v k * cofactorVec M k := by
  rw [Matrix.det_succ_row (border M v) (Fin.last n)]
  simp_rw [border_submatrix_last]
  simp only [border, Matrix.of_apply, Fin.snoc_last, cofactorVec]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  simp only [Fin.val_last, pow_add]
  ring

/-- The signed maximal-minor vector lies in the right kernel of the rectangular
matrix. -/
theorem mulVec_cofactorVec {n : ℕ} (M : Matrix (Fin n) (Fin (n + 1)) R) :
    M *ᵥ cofactorVec M = 0 := by
  funext i
  have hrows : (border M (M i)) (Fin.castSucc i) =
      (border M (M i)) (Fin.last n) := by
    funext j
    simp [border]
  have hne : Fin.castSucc i ≠ Fin.last n := by
    exact Fin.castSucc_ne_last i
  have hdet : (border M (M i)).det = 0 :=
    Matrix.det_zero_of_row_eq hne hrows
  rw [det_border] at hdet
  have hunit : IsUnit ((-1 : R) ^ n) := isUnit_neg_one.pow n
  have hsum : ∑ k, M i k * cofactorVec M k = 0 := by
    exact (IsUnit.mul_right_eq_zero hunit).mp hdet
  simpa [Matrix.mulVec, dotProduct] using hsum

/-- A pointwise version of `mulVec_cofactorVec`. -/
theorem sum_mul_cofactorVec_eq_zero {n : ℕ}
    (M : Matrix (Fin n) (Fin (n + 1)) R) (i : Fin n) :
    ∑ k, M i k * cofactorVec M k = 0 := by
  have h := congrFun (mulVec_cofactorVec M) i
  simpa [Matrix.mulVec, dotProduct] using h

/-- Any right-kernel vector is determinantly proportional to the signed
maximal-minor vector.  No division and no regularity assumption are used:
`x p * C k = x k * C p` holds over every commutative ring. -/
theorem kernel_cofactor_proportional {n : ℕ}
    (M : Matrix (Fin n) (Fin (n + 1)) R) (x : Fin (n + 1) → R)
    (hx : M *ᵥ x = 0) (p k : Fin (n + 1)) :
    x p * cofactorVec M k = x k * cofactorVec M p := by
  let e : Fin (n + 1) → R := Pi.single p 1
  let B : Matrix (Fin (n + 1)) (Fin (n + 1)) R := border M e
  have hB : B *ᵥ x = Pi.single (Fin.last n) (x p) := by
    funext i
    refine Fin.lastCases ?_ (fun row ↦ ?_) i
    · simp only [B, border, e, Matrix.mulVec, dotProduct, Matrix.of_apply,
        Fin.snoc_last, Pi.single_eq_same]
      rw [Fintype.sum_eq_single p]
      · simp
      · intro j hj
        simp [Pi.single_eq_of_ne hj]
    · have hrow := congrFun hx row
      simpa [B, border, Matrix.mulVec, dotProduct] using hrow
  have hdet : B.det = (-1) ^ n * cofactorVec M p := by
    rw [show B = border M e by rfl, det_border]
    congr 1
    rw [Fintype.sum_eq_single p]
    · simp [e]
    · intro j hj
      simp [e, Pi.single_eq_of_ne hj]
  have hadj (i : Fin (n + 1)) :
      B.adjugate i (Fin.last n) = (-1) ^ n * cofactorVec M i := by
    rw [Matrix.adjugate_fin_succ_eq_det_submatrix]
    rw [show B = border M e by rfl, border_submatrix_last]
    simp only [Fin.val_last, cofactorVec, pow_add]
    ring
  have hsolve : B.det * x k = B.adjugate k (Fin.last n) * x p := by
    calc
      B.det * x k = ((B.det • (1 : Matrix (Fin (n + 1)) (Fin (n + 1)) R)) *ᵥ x) k := by
        rw [Matrix.smul_mulVec, Matrix.one_mulVec]
        rfl
      _ = ((B.adjugate * B) *ᵥ x) k := by rw [Matrix.adjugate_mul]
      _ = (B.adjugate *ᵥ (B *ᵥ x)) k := by rw [Matrix.mulVec_mulVec]
      _ = (B.adjugate *ᵥ Pi.single (Fin.last n) (x p)) k := by rw [hB]
      _ = B.adjugate k (Fin.last n) * x p := by
        simp only [Matrix.mulVec, dotProduct]
        rw [Fintype.sum_eq_single (Fin.last n)]
        · simp
        · intro j hj
          simp [Pi.single_eq_of_ne hj]
  rw [hdet, hadj] at hsolve
  have hunit : IsUnit ((-1 : R) ^ n) := isUnit_neg_one.pow n
  apply hunit.mul_left_cancel
  simpa [mul_assoc, mul_comm, mul_left_comm] using hsolve.symm

section Receipts

#print axioms border_submatrix_last
#print axioms det_border
#print axioms mulVec_cofactorVec
#print axioms sum_mul_cofactorVec_eq_zero
#print axioms kernel_cofactor_proportional

end Receipts

end BorderedJacobianUniversal
