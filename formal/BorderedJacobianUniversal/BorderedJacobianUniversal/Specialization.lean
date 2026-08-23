/-
Copyright (c) 2026 HC4JC2 successor project. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: HC4JC2 successor project contributors
-/
import BorderedJacobianUniversal.Universal

/-!
# Specialization to an arbitrary commutative ring

The universal identity is evaluated by a single ring homomorphism.  This file
proves that evaluation commutes with every definition used in the theorem and
then derives the maximal-minor and bordered-determinant formulas over an
arbitrary commutative ring, including rings with zero divisors.
-/

namespace BorderedJacobianUniversal

open Finset Matrix Polynomial MvPolynomial

variable {R : Type*}

/-- Assignment of the ordered universal variables to concrete coefficients. -/
def coeffAssign (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R) :
    Fin (r + s + 2) → R :=
  fun col ↦
    if h : (col : ℕ) ≤ r then a ⟨col, by omega⟩
    else b ⟨(col : ℕ) - (r + 1), by omega⟩

@[simp]
theorem coeffAssign_a (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R)
    (i : Fin (r + 1)) :
    coeffAssign r s a b ⟨i, by omega⟩ = a i := by
  have hi : (i : ℕ) ≤ r := Nat.le_of_lt_succ i.isLt
  simp [coeffAssign, hi]

@[simp]
theorem coeffAssign_b (r s : ℕ) (a : Fin (r + 1) → R) (b : Fin (s + 1) → R)
    (j : Fin (s + 1)) :
    coeffAssign r s a b ⟨r + 1 + j, by omega⟩ = b j := by
  have hrj : ¬(r + 1 + (j : ℕ) ≤ r) := by omega
  have hsub : r + 1 + (j : ℕ) - (r + 1) = (j : ℕ) := by omega
  simp [coeffAssign, hrj, hsub]

variable [CommRing R]

/-- Evaluation of the universal integer coefficient ring. -/
noncomputable def specialize (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) : Univ r s →+* R :=
  MvPolynomial.eval₂Hom (Int.castRingHom R) (coeffAssign r s a b)

@[simp]
theorem specialize_univA (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (i : Fin (r + 1)) :
    specialize r s a b (univA r s i) = a i := by
  simp [specialize, univA]

@[simp]
theorem specialize_univB (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (j : Fin (s + 1)) :
    specialize r s a b (univB r s j) = b j := by
  simp [specialize, univB]

@[simp]
theorem specialize_coeffExt_a (r s n : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    specialize r s a b (coeffExt (univA r s) n) = coeffExt a n := by
  by_cases hn : n < r + 1
  · simp [coeffExt, hn]
  · simp [coeffExt, hn]

@[simp]
theorem specialize_coeffExt_b (r s n : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    specialize r s a b (coeffExt (univB r s) n) = coeffExt b n := by
  by_cases hn : n < s + 1
  · simp [coeffExt, hn]
  · simp [coeffExt, hn]

/-- Entrywise specialization of the universal multiplication Jacobian. -/
theorem specialize_mulJac_entry (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (i : Fin (r + s + 1)) (j : Fin (r + s + 2)) :
    specialize r s a b (mulJac r s (univA r s) (univB r s) i j) =
      mulJac r s a b i j := by
  by_cases hjr : (j : ℕ) ≤ r
  · by_cases hji : (j : ℕ) ≤ (i : ℕ)
    · simp [mulJac, hjr, hji]
    · simp [mulJac, hjr, hji]
  · by_cases hji : (j : ℕ) - (r + 1) ≤ (i : ℕ)
    · simp [mulJac, hjr, hji]
    · simp [mulJac, hjr, hji]

/-- Specialization of the canonical kernel vector. -/
theorem specialize_kappa (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (j : Fin (r + s + 2)) :
    specialize r s a b (kappa r s (univA r s) (univB r s) j) =
      kappa r s a b j := by
  by_cases hjr : (j : ℕ) ≤ r
  · simp [kappa, hjr]
  · simp [kappa, hjr]

/-- Mapping a bounded coefficient polynomial maps each coefficient. -/
theorem map_polyOfCoeffs (n : ℕ) {S T : Type*} [CommRing S] [CommRing T]
    (f : S →+* T) (c : Fin (n + 1) → S) :
    (polyOfCoeffs n c).map f = polyOfCoeffs n (fun i ↦ f (c i)) := by
  ext k
  rw [Polynomial.coeff_map, polyOfCoeffs_coeff, polyOfCoeffs_coeff]
  by_cases hk : k < n + 1
  · simp [coeffExt, hk]
  · simp [coeffExt, hk]

@[simp]
theorem specialize_resultantBA (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    specialize r s a b (resultantBA r s (univA r s) (univB r s)) =
      resultantBA r s a b := by
  unfold resultantBA
  let f := specialize r s a b
  have hbmap : (polyOfCoeffs s (univB r s)).map f = polyOfCoeffs s b := by
    rw [map_polyOfCoeffs]
    congr 1
    funext j
    exact specialize_univB r s a b j
  have hamap : (polyOfCoeffs r (univA r s)).map f = polyOfCoeffs r a := by
    rw [map_polyOfCoeffs]
    congr 1
    funext i
    exact specialize_univA r s a b i
  rw [← Polynomial.resultant_map_map, hbmap, hamap]

/-- Specialization commutes with each signed maximal minor. -/
theorem specialize_cofactorVec (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (k : Fin (r + s + 2)) :
    specialize r s a b
        (cofactorVec (mulJac r s (univA r s) (univB r s)) k) =
      cofactorVec (mulJac r s a b) k := by
  have hmatrix :
      (specialize r s a b).mapMatrix
          ((mulJac r s (univA r s) (univB r s)).submatrix id k.succAbove) =
        (mulJac r s a b).submatrix id k.succAbove := by
    ext i j
    simp [RingHom.mapMatrix_apply, specialize_mulJac_entry]
  rw [cofactorVec, cofactorVec, map_mul, map_pow]
  simp only [map_neg, map_one]
  rw [RingHom.map_det, hmatrix]

/-- Arbitrary-ring signed-maximal-minor identity, obtained solely by evaluating
the universal polynomial identity. -/
theorem cofactorVec_mulJac (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (k : Fin (r + s + 2)) :
    cofactorVec (mulJac r s a b) k =
      (-1) ^ (r * (s + 1)) * resultantBA r s a b * kappa r s a b k := by
  have h := congrArg (specialize r s a b) (universal_cofactorVec r s k)
  simpa [specialize_cofactorVec, specialize_resultantBA, specialize_kappa] using h

/-- Equivalent maximal-minor statement in expanded form. -/
theorem det_mulJac_submatrix (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (k : Fin (r + s + 2)) :
    (-1) ^ (k : ℕ) * ((mulJac r s a b).submatrix id k.succAbove).det =
      (-1) ^ (r * (s + 1)) * resultantBA r s a b * kappa r s a b k := by
  exact cofactorVec_mulJac r s a b k

/-- Final bordered-Jacobian identity over every commutative ring. -/
theorem det_bordered (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) (v : Fin (r + s + 2) → R) :
    (border (mulJac r s a b) v).det =
      (-1) ^ (s * (r + 1) + 1) * resultantBA r s a b *
        ∑ i, v i * kappa r s a b i := by
  rw [det_border]
  simp_rw [cofactorVec_mulJac]
  have hsum :
      (∑ x, v x *
        ((-1) ^ (r * (s + 1)) * resultantBA r s a b * kappa r s a b x)) =
        ((-1) ^ (r * (s + 1)) * resultantBA r s a b) *
          ∑ x, v x * kappa r s a b x := by
    calc
      _ = ∑ x, ((-1) ^ (r * (s + 1)) * resultantBA r s a b) *
          (v x * kappa r s a b x) := by
            apply Finset.sum_congr rfl
            intro x _
            ring
      _ = _ := (Finset.mul_sum Finset.univ
        (fun x ↦ v x * kappa r s a b x)
        ((-1) ^ (r * (s + 1)) * resultantBA r s a b)).symm
  rw [hsum]
  have hsign :
      (-1 : R) ^ (r + s + 1) * (-1) ^ (r * (s + 1)) =
        (-1) ^ (s * (r + 1) + 1) := by
    rw [← pow_add]
    have hexp : r + s + 1 + r * (s + 1) = s * (r + 1) + 1 + 2 * r := by
      ring
    rw [hexp, pow_add, pow_mul]
    simp
  calc
    (-1) ^ (r + s + 1) *
        (((-1) ^ (r * (s + 1)) * resultantBA r s a b) *
          ∑ i, v i * kappa r s a b i) =
      (((-1) ^ (r + s + 1) * (-1) ^ (r * (s + 1))) *
        resultantBA r s a b) * ∑ i, v i * kappa r s a b i := by ring
    _ = _ := by rw [hsign]

section Receipts

#print axioms specialize_mulJac_entry
#print axioms specialize_resultantBA
#print axioms specialize_cofactorVec
#print axioms cofactorVec_mulJac
#print axioms det_mulJac_submatrix
#print axioms det_bordered

end Receipts

end BorderedJacobianUniversal
