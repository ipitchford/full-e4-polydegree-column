/-
Copyright (c) 2026 HC4JC2 successor project. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: HC4JC2 successor project contributors
-/
import BorderedJacobianUniversal.Specialization
import Mathlib.Data.ZMod.Basic

/-!
# Boundary and negative-control tests

These theorems exercise the same definitions as the general result.  They are
not substitutes for the proof; they are indexing and specialization tripwires.
-/

namespace BorderedJacobianUniversal

open Matrix

variable {R : Type*} [CommRing R]

/-- At bidegree `(0,0)`, the bordered determinant is the expected `2 × 2`
determinant. -/
theorem det_bordered_zero_zero (a₀ b₀ v₀ v₁ : R) :
    (border (mulJac 0 0 ![a₀] ![b₀]) ![v₀, v₁]).det = b₀ * v₁ - a₀ * v₀ := by
  have hmatrix :
      border (mulJac 0 0 ![a₀] ![b₀]) ![v₀, v₁] = !![b₀, a₀; v₀, v₁] := by
    ext i j
    fin_cases i <;> fin_cases j <;> rfl
  rw [hmatrix, Matrix.det_fin_two]
  change b₀ * v₁ - a₀ * v₀ = b₀ * v₁ - a₀ * v₀
  rfl

/-- Concrete zero-divisor-ring control.  The chosen `(1,1)` instance over
`ZMod 6` has determinant `2`, so this also catches accidental field-only
specialization. -/
theorem zmod_six_one_one_control :
    (border
      (mulJac 1 1
        ![(1 : ZMod 6), (2 : ZMod 6)]
        ![(3 : ZMod 6), (4 : ZMod 6)])
      ![(1 : ZMod 6), (2 : ZMod 6), (3 : ZMod 6), (4 : ZMod 6)]).det = 2 := by
  decide

section Receipts

#print axioms det_bordered_zero_zero
#print axioms zmod_six_one_one_control

end Receipts

end BorderedJacobianUniversal
