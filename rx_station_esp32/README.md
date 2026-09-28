# Rx Base Station Firmware: ESP32 + CC1200

Firmware for the weak-signal backscatter receiver, optimized for rejection of the 866.3 MHz carrier and extraction of the 85 kHz subcarrier sideband.

## Hardware Interfaces
* **Host:** ESP32-WROOM-32
* **RF Receiver:** TI CC1200 Transceiver via VSPI
* **Interrupt Pin:** CC1200 `GPIO0`/`GPIO2` connected to ESP32 external interrupt pin
* **Antenna:** +12 dBi Yagi (Mounted in **Horizontal Polarization**)

## Technical Operation
1. **Tuning & Filtering:** Synthesizes an RX center frequency of **866.385 MHz** (866.3 MHz Tx carrier + 85 kHz subcarrier offset). Narrow channel filtering rejects direct residual Tx interference.
2. **Demodulation:** Configured for On-Off Keying (OOK) reception with CC1200 WaveMatch hardware sync detection.
3. **Telemetry Pipeline:** Packet reception triggers a hardware ISR. Payload is read from the RX FIFO, CRC is validated, and acceleration vectors along with RSSI values are output over USB-UART as formatted JSON/CSV strings.

## File Map
* `main.cpp`: FreeRTOS reception task, sync interrupt handling, and serial telemetry streamer.
* `cc1200_rx.cpp` / `cc1200_rx.h`: SPI abstraction, CC1200 OOK register configuration, FIFO burst extraction, and CRC-16 validation.

## Build Requirements
* **Framework:** ESP-IDF v5.x or PlatformIO (Arduino-ESP32 framework)
* **Baud Rate:** 115200 bps (UART0 for host logging)