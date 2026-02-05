# -*- coding: utf-8 -*-

import streamlit as st

st.set_page_config(
    page_title="Shenker App – Functional Voice Leading MVP",
    layout="centered"
)

st.title("🎼 Shenker App – Functional Voice Leading MVP")

# =========================
# DATOS MUSICALES
# =========================

NOTE_NAMES = ["C", "C#", "D", "Eb", "E", "F",
              "F#", "G", "Ab", "A", "Bb", "B"]

CHORD_QUALITIES = {
    "maj7":   {1: 0, 3: 4, 5: 7, 7: 11},
    "7":      {1: 0, 3: 4, 5: 7, 7: 10},
    "m7":     {1: 0, 3: 3, 5: 7, 7: 10},
    "mMaj7":  {1: 0, 3: 3, 5: 7, 7: 11},
    "m7b5":   {1: 0, 3: 3, 5: 6, 7: 10},
    "°7":     {1: 0, 3: 3, 5: 6, 7: 9},
    "maj7#5": {1: 0, 3: 4, 5: 8, 7: 11},
}

def note_name(pc):
    return NOTE_NAMES[pc % 12]

def build_chord(root_pc, quality):
    intervals = CHORD_QUALITIES[quality]
    return {f: (root_pc + i) % 12 for f, i in intervals.items()}

def apply_functional_permutation(current_order, permutation):
    return [permutation[f] for f in current_order]

# =========================
# INPUT USUARIO
# =========================

st.header("1️⃣ Voicing inicial")

initial_voicing = st.text_input(
    "Funciones iniciales (ej: 7 3 5 1)",
    value="7 3 5 1"
)

try:
    initial_voicing = [int(x) for x in initial_voicing.strip().split()]
except ValueError:
    st.error("Ingresá solo números separados por espacios.")
    st.stop()

st.header("2️⃣ Permutación funcional")

permutation_input = st.text_input(
    "Permutación (ej: 5 7 1 3)",
    value="5 7 1 3"
)

try:
    perm_list = [int(x) for x in permutation_input.strip().split()]
except ValueError:
    st.error("Ingresá solo números separados por espacios.")
    st.stop()

if len(perm_list) != len(initial_voicing):
    st.error("La permutación debe tener la misma longitud que el voicing.")
    st.stop()

permutation = {
    initial_voicing[i]: perm_list[i]
    for i in range(len(initial_voicing))
}

# =========================
# PROGRESIÓN ARMÓNICA (8 ACORDES)
# =========================

st.header("3️⃣ Progresión armónica (8 acordes)")

chord_roots = []
chord_qualities = []

for i in range(8):
    st.subheader(f"Acorde {i + 1}")

    root = st.selectbox(
        f"Tónica {i + 1}",
        NOTE_NAMES,
        index=9,
        key=f"root_{i}"
    )
    quality = st.selectbox(
        f"Especie {i + 1}",
        list(CHORD_QUALITIES.keys()),
        index=2,
        key=f"quality_{i}"
    )

    chord_roots.append(root)
    chord_qualities.append(quality)

# =========================
# PROCESO
# =========================

st.header("🎯 Resultado – Voice Leading Funcional")

current_order = initial_voicing.copy()

for i in range(8):
    root_pc = NOTE_NAMES.index(chord_roots[i])
    chord = build_chord(root_pc, chord_qualities[i])

    notes = [note_name(chord[f]) for f in current_order]

    st.markdown(f"**Acorde {i + 1}: {chord_roots[i]} {chord_qualities[i]}**")
    st.code(
        f"Funciones: {current_order}\n"
        f"Notas:     {notes}"
    )

    if i < 7:
        current_order = apply_functional_permutation(
            current_order,
            permutation
        )
