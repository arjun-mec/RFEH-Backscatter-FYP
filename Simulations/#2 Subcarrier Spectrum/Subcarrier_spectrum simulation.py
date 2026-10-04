"""
Simulation 2 — WPC Regulatory Subcarrier Spectrum & Bandwidth Compliance
==========================================================================
Proves that the 85 kHz OOK-modulated backscatter signal (USB @ +85 kHz,
LSB @ -85 kHz, plus square-wave harmonics) stays inside the WPC 200 kHz
channel mask (+-100 kHz) with >=15 kHz guard band, and that sideband
power drops below the -36 dBm reference before hitting the mask edge.
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 1. PARAMETERS (from the proposal spec)
# ----------------------------------------------------------------------
FS          = 2_000_000        # sampling rate, Sa/s  (>= 2 MSa/s required)
DURATION    = 50e-3            # seconds  (>= 50 ms required)
F_SUB       = 85_000           # Hz, subcarrier square-wave frequency
DATA_RATE   = 1200             # bits/s   (1.2 kbps)
F_CARRIER   = 0                # Hz, baseband-equivalent centre (866.3 MHz downconverted to 0)

MASK_HALF_BW   = 100_000       # Hz, WPC 200 kHz channel -> +-100 kHz
GUARD_TARGET   = 15_000        # Hz, required guard band
MASK_FLOOR_DBM = -36           # dBm, level sidebands must fall below at the mask edge

PRX_DBM_AT_D = -60.0   # <-- replace with your Sim-1 result, e.g. Prx(10 m)

# ----------------------------------------------------------------------
# 2. SIGNAL MODELLING
# ----------------------------------------------------------------------
t = np.arange(0, DURATION, 1 / FS)
n_samples = len(t)

Ac = 1.0
c_t = Ac * np.cos(2 * np.pi * F_CARRIER * t)

s_t = signal.square(2 * np.pi * F_SUB * t)

bits_needed = int(np.ceil(DURATION * DATA_RATE)) + 2
rng = np.random.default_rng(42)
prbs_bits = rng.integers(0, 2, size=bits_needed)

samples_per_bit = int(FS / DATA_RATE)
d_t = np.repeat(prbs_bits, samples_per_bit)[:n_samples]
if len(d_t) < n_samples:
    d_t = np.pad(d_t, (0, n_samples - len(d_t)), mode="edge")

m_t = d_t * s_t
x_backscatter = c_t * (1 + m_t)

# ----------------------------------------------------------------------
# 3. POWER SPECTRAL DENSITY (Welch, Hann window, 50% overlap)
# ----------------------------------------------------------------------
nperseg = 8192
freqs, psd = signal.welch(
    x_backscatter, fs=FS, window="hann",
    nperseg=nperseg, noverlap=nperseg // 2,
    scaling="density", return_onesided=False,
)

freqs = np.fft.fftshift(freqs)
psd = np.fft.fftshift(psd)
mask_window = (freqs >= -200e3) & (freqs <= 200e3)
freqs = freqs[mask_window]
psd = psd[mask_window]

psd_db_rel = 10 * np.log10(psd + 1e-20)
psd_db_rel -= psd_db_rel.max()

if PRX_DBM_AT_D is not None:
    psd_dbm = psd_db_rel + PRX_DBM_AT_D
    ylabel = "PSD (dBm, calibrated to Sim-1 Prx)"
else:
    psd_dbm = psd_db_rel
    ylabel = "PSD (dB, relative to carrier peak)"

# ----------------------------------------------------------------------
# 4. MASK VERIFICATION
# ----------------------------------------------------------------------
def power_near(freq_target, tol=2_000):
    idx = (np.abs(freqs - freq_target) <= tol)
    return psd_dbm[idx].max()

usb_peak = power_near(F_SUB)
lsb_peak = power_near(-F_SUB)
edge_pos = power_near(MASK_HALF_BW, tol=1_000)
edge_neg = power_near(-MASK_HALF_BW, tol=1_000)
guard_band = MASK_HALF_BW - F_SUB

print(f"USB peak (@ +{F_SUB/1e3:.0f} kHz): {usb_peak:6.2f}  (reference)")
print(f"LSB peak (@ -{F_SUB/1e3:.0f} kHz): {lsb_peak:6.2f}")
print(f"Level at +{MASK_HALF_BW/1e3:.0f} kHz mask edge: {edge_pos:6.2f}")
print(f"Level at -{MASK_HALF_BW/1e3:.0f} kHz mask edge: {edge_neg:6.2f}")
print(f"Guard band available: {guard_band/1e3:.1f} kHz "
      f"(required >= {GUARD_TARGET/1e3:.0f} kHz -> "
      f"{'PASS' if guard_band >= GUARD_TARGET else 'FAIL'})")
if PRX_DBM_AT_D is not None:
    edge_ok = max(edge_pos, edge_neg) < MASK_FLOOR_DBM
    print(f"Sidebands below {MASK_FLOOR_DBM} dBm at mask edge: "
          f"{'PASS' if edge_ok else 'FAIL'}")

# ----------------------------------------------------------------------
# 5. PLOT — PSD with regulatory overlay
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(freqs / 1e3, psd_dbm, color="tab:blue", lw=1)

ax.axvline(-MASK_HALF_BW / 1e3, color="red", ls="--", lw=1.2, label="WPC 200 kHz mask edge")
ax.axvline(MASK_HALF_BW / 1e3, color="red", ls="--", lw=1.2)

ax.axvline(0, color="gray", ls=":", lw=1, label="Carrier (0 kHz)")
ax.axvline(F_SUB / 1e3, color="green", ls=":", lw=1, label=f"USB (+{F_SUB/1e3:.0f} kHz)")
ax.axvline(-F_SUB / 1e3, color="green", ls=":", lw=1)

if PRX_DBM_AT_D is not None:
    ax.axhline(MASK_FLOOR_DBM, color="orange", ls="-.", lw=1, label=f"{MASK_FLOOR_DBM} dBm floor")

ax.set_xlim(-200, 200)
ax.set_xlabel("Frequency offset from carrier (kHz)")
ax.set_ylabel(ylabel)
ax.set_title("Backscatter Subcarrier PSD vs WPC 200 kHz Channel Mask")
ax.legend(loc="upper right", fontsize=8)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("sim2_psd_plot.png", dpi=150)
print("\nSaved plot to sim2_psd_plot.png")