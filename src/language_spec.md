# Restricted C Language Specification

## Purpose

This project uses a controlled subset of C to generate benchmark programs for
automated mutation-based compiler optimization.

The benchmark programs should look like normal C programs while remaining
simple enough for our compiler front end and TAC generator to process reliably.

---

## 1. Program Structure

Each benchmark contains exactly one function:

```c
int compute(int x, int y) {
    int a;
    int b;

    a = x + 5;
    b = a * 2;

    return b;
}