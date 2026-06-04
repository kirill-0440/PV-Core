---
title: BC Lift Moduli in AWFS
author: Kirill Nikitin
date: 2026-06-04
status: research-note
---

# BC Lift Moduli in AWFS

## Abstract

We propose studying not merely the existence of a Beck–Chevalley lift in an algebraic weak factorisation system, but the fiber of possible L-map structures carried by the Beck–Chevalley comparison morphism.

## AWFS Structure

Let (L,R) be an algebraic weak factorisation system on a category C.

Define

L-Map := Coalg(L).

There is a forgetful functor

U_L : L-Map -> C^→.

## Space of L-Structures

For a morphism f in C^→ define

LStr(f) := (U_L)^(-1)(f).

Equivalently, LStr(f) is the fiber of the forgetful functor over f.

Objects are L-coalgebra structures on the underlying morphism f.

## Beck–Chevalley Comparison

Let β_BC be a Beck–Chevalley comparison morphism.

Define

M_BC(β_BC) := LStr(β_BC).

## Proposition

A Beck–Chevalley lift exists if and only if

M_BC(β_BC) ≠ ∅.

Proof.

By definition, points of the fiber of U_L over β_BC are precisely L-map structures whose underlying morphism is β_BC. ∎

## Interpretation

Ordinary liftability studies only non-emptiness.

The moduli viewpoint studies the entire fiber of possible structures.

## Open Problems

1. Determine whether M_BC admits a natural groupoid structure.
2. Extend to enriched AWFS.
3. Extend to monoidal AWFS.
4. Construct obstruction invariants.
5. Relate BC lift moduli to interface witness spaces.

## Status

Research note motivated by correspondence with John Bourke (2026).
