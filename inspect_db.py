"""
Quick diagnostic: decode the last N rows from RapidFire.db and pretty-print
the arrays so you can verify values look sane.
"""

import sqlite3
import numpy as np
import globals

CONT_NAMES   = {v: k for k, v in globals.CONTINUOUS_KNOB_ORDER.items()}
SWITCH_NAMES = {v: k for k, v in globals.SWITCH_ORDER.items()}
MODE_NAMES   = {v: k for k, v in {k: v['index'] for k, v in globals.MODES_ORDER_LENGTHS.items()}.items()}

N_CONT   = len(globals.CONTINUOUS_KNOB_ORDER)
N_SWITCH = len(globals.SWITCH_ORDER)
N_MODE   = len(globals.MODES_ORDER_LENGTHS)


def decode(blob, dtype, n):
    return np.frombuffer(blob, dtype=dtype)[:n]


def print_nonzero(label, arr, names):
    nonzero = [(names[i], arr[i]) for i in range(len(arr)) if arr[i] != 0]
    print(f"  {label}: {nonzero if nonzero else '(all zero)'}")


def inspect(row):
    (id_, description, emb, in_params, cont_targs, switch_targs, mode_targs,
     level, origin, request_type, desc_name, request_type_text,
     amask_c, amask_s, amask_m, pol_c, pol_s, level_c) = row

    print(f"\n{'='*60}")
    print(f"  ID: {id_}  |  type: {request_type_text}  |  origin: {origin}")
    print(f"  Description: {description}")

    in_p   = decode(in_params,    np.float32, N_CONT + N_SWITCH + N_MODE)
    c_t    = decode(cont_targs,   np.float32, N_CONT)
    s_t    = decode(switch_targs, np.float32, N_SWITCH)
    m_t    = decode(mode_targs,   np.int64,   N_MODE)
    ac     = decode(amask_c,      np.float32, N_CONT)
    as_    = decode(amask_s,      np.float32, N_SWITCH)
    am     = decode(amask_m,      np.float32, N_MODE)
    pc     = decode(pol_c,        np.float32, N_CONT)
    ps     = decode(pol_s,        np.float32, N_SWITCH)
    lc     = decode(level_c,      np.float32, N_CONT)

    emb_arr = np.frombuffer(emb, dtype=np.float32)
    print(f"  Embedding: shape={emb_arr.shape}, norm={np.linalg.norm(emb_arr):.4f} (should be ~1.0)")

    print("\n  --- Active continuous knobs ---")
    for i in range(N_CONT):
        if ac[i] != 0:
            print(f"    {CONT_NAMES[i]:30s}  target={c_t[i]:.4f}  polarity={int(pc[i]):+d}  level={lc[i]:.4f}")

    print("\n  --- Active switches ---")
    for i in range(N_SWITCH):
        if as_[i] != 0:
            print(f"    {SWITCH_NAMES[i]:30s}  target={s_t[i]:.1f}  polarity={int(ps[i]):+d}")

    print("\n  --- Active modes ---")
    for i in range(N_MODE):
        if am[i] != 0:
            mode_name = MODE_NAMES[i]
            options = globals.MODES_ORDER_LENGTHS[mode_name]['unormalized']
            idx = int(m_t[i])
            label = options[idx] if idx < len(options) else "OUT OF RANGE"
            print(f"    {mode_name:30s}  index={idx}  value={label}")


def main(n=5):
    conn = sqlite3.connect("RapidFire.db")
    cur  = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM training_data")
    total = cur.fetchone()[0]
    print(f"Total rows: {total}. Showing last {n}.")

    cur.execute("SELECT * FROM training_data ORDER BY id DESC LIMIT ?", (n,))
    rows = cur.fetchall()
    conn.close()

    for row in reversed(rows):
        inspect(row)

    print(f"\n{'='*60}")


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    main(n)
