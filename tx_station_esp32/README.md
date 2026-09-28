# Tx Base Station Firmware: ESP32 + CC1200 + SE2435L

Firmware controlling the high-power RF energy transmitter, enforcing strict WPC 2021 Table IV compliance.

## Hardware Interfaces
* **Host:** ESP32-WROOM-32
* **RF Synthesizer:** TI CC1200 Transceiver via HSPI
* **Front-End:** Skyworks SE2435L High-Power PA (`CSD`, `CTX` control lines)
* **Antenna:** +12 dBi Yagi (Mounted in **Vertical Polarization**)

## Technical Operation
1. **Continuous Wave (CW) Generation:** Drives the CC1200 to emit an unmodulated carrier centered at **866.3 MHz**.
2. **e.r.p. Power Regulation:** Conducted drive power is trimmed via CC1200 0.4 dB digital attenuation steps so total conducted power + antenna gain (+12 dBi) $-$ cable loss $\le +33\text{ dBm}$ (2W e.r.p.).
3. **Duty Cycling (WPC Table IV):** Uses high-resolution hardware timers to execute a cycle of **4.0 seconds Active TX**, followed by a **100 ms silent interval** (PA completely powered down via `CSD`).

## File Map
* `main.cpp`: Hardware timer ISR for the 4s-ON / 100ms-OFF cycle, PA bias control, and CLI power monitoring.
* `cc1200_tx.cpp` / `cc1200_tx.h`: CC1200 SPI register initialization, frequency calibration, and power-table attenuation routines.

## Build Requirements
* **Framework:** ESP-IDF v5.x or PlatformIO (Arduino-ESP32 framework)
* **SPI Clock:** 10 MHz