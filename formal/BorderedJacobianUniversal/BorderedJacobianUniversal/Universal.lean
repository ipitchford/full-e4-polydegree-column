/-
Copyright (c) 2026 HC4JC2 successor project. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: HC4JC2 successor project contributors
-/
import BorderedJacobianUniversal.Anchor
import Mathlib.Algebra.MvPolynomial.NoZeroDivisors

/-!
# Universal maximal-minor identity

The universal coefficient ring is an integral domain.  The generic
proportionality theorem and the anchored minor therefore identify every signed
maximal minor after one explicit cancellation of the indeterminate `aᵣ`.
-/

namespace BorderedJacobianUniversal

open Finset Matrix Polynomial MvPolynomial

variable {R : Type*} [CommRing R]

/-- Signed anchor cofactor over an arbitrary commutative ring. -/
theorem cofactorVec_aLead (r s : ℕ) (a : Fin (r + 1) → R)
    (b : Fin (s + 1) → R) :
    cofactorVec (mulJac r s a b) (aLeadCol r s) =
      (-1) ^ (r * (s + 1)) * resultantBA r s a b * a (Fin.last r) := by
  rw [cofactorVec]
  change (-1) ^ r * (anchorMinor r s a b).det = _
  rw [det_anchorMinor]
  have hpow :
      (-1 : R) ^ r * (-1) ^ (r * s) = (-1) ^ (r * (s + 1)) := by
    calc
      (-1 : R) ^ r * (-1) ^ (r * s) = (-1) ^ (r + r * s) := by rw [pow_add]
      _ = (-1) ^ (r * (s + 1)) := by rw [Nat.mul_succ, add_comm]
  calc
    (-1) ^ r * (((-1) ^ (r * s) * resultantBA r s a b) * a (Fin.last r)) =
        (((-1) ^ r * (-1) ^ (r * s)) * resultantBA r s a b) * a (Fin.last r) := by
          ring
    _ = _ := by rw [hpow]

/-- Universal integer coefficient ring. -/
abbrev Univ (r s : ℕ) := MvPolynomial (Fin (r + s + 2)) ℤ

/-- Universal `a` coefficients. -/
noncomputable def univA (r s : ℕ) : Fin (r + 1) → Univ r s :=
  fun i ↦ X ⟨i, by omega⟩

/-- Universal `b` coefficients. -/
noncomputable def univB (r s : ℕ) : Fin (s + 1) → Univ r s :=
  fun j ↦ X ⟨r + 1 + j, by omega⟩

/-- The leading universal `a` coefficient is the variable at the anchor
column. -/
theorem univA_last_eq_X_aLead (r s : ℕ) :
    univA r s (Fin.last r) = X (aLeadCol r s) := by
  apply congrArg X
  apply Fin.ext
  simp [aLeadCol]

/-- The canonical kernel coordinate at the anchor is the same variable. -/
theorem kappa_univ_aLead (r s : ℕ) :
    kappa r s (univA r s) (univB r s) (aLeadCol r s) = X (aLeadCol r s) := by
  have hfin : (⟨r, by omega⟩ : Fin (r + 1)) = Fin.last r := Fin.ext rfl
  simp [kappa, aLeadCol, hfin, univA_last_eq_X_aLead]

/-- Universal signed-maximal-minor identity. -/
theorem universal_cofactorVec (r s : ℕ) (k : Fin (r + s + 2)) :
    cofactorVec (mulJac r s (univA r s) (univB r s)) k =
      (-1) ^ (r * (s + 1)) *
        resultantBA r s (univA r s) (univB r s) *
          kappa r s (univA r s) (univB r s) k := by
  let M := mulJac r s (univA r s) (univB r s)
  let κ := kappa r s (univA r s) (univB r s)
  have hker : M *ᵥ κ = 0 := mulJac_mulVec_kappa r s (univA r s) (univB r s)
  have hprop := kernel_cofactor_proportional M κ hker (aLeadCol r s) k
  have hanchor := cofactorVec_aLead r s (univA r s) (univB r s)
  rw [show κ (aLeadCol r s) = X (aLeadCol r s) by
    exact kappa_univ_aLead r s] at hprop
  rw [show cofactorVec M (aLeadCol r s) =
      (-1) ^ (r * (s + 1)) *
        resultantBA r s (univA r s) (univB r s) * X (aLeadCol r s) by
    simpa [M, univA_last_eq_X_aLead] using hanchor] at hprop
  apply mul_left_cancel₀ (MvPolynomial.X_ne_zero (R := ℤ) (aLeadCol r s))
  simpa [M, κ, mul_assoc, mul_comm, mul_left_comm] using hprop

section Receipts

#print axioms cofactorVec_aLead
#print axioms univA_last_eq_X_aLead
#print axioms kappa_univ_aLead
#print axioms universal_cofactorVec

end Receipts

end BorderedJacobianUniversal
