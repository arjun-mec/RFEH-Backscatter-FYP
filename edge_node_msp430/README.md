# Edge Node Firmware: MSP430FR2433

Embedded C firmware for the ultra-low-power, batteryless backscatter sensor node.

## Hardware Interfaces
* **MCU:** TI MSP430FR2433 (FRAM-based)
* **Sensor:** Analog Devices ADXL362 MEMS Accelerometer (via eUSCI SPI)
* **Modulator:** Analog Devices ADG902 RF Switch (driven via Timer_A PWM pin)
* **PMIC Interface:** e-peas AEM30940 status lines

## Technical Operation
1. **Cold Boot & Power Gating:** The MCU initializes upon capacitor bank charge threshold. FRAM persistent variables restore network counter states across power-loss events.
2. **Deep Sleep:** The MCU enters `LPM3.5`/`LPM4`, consuming $<500\text{ nA}$. The ADXL362 autonomously monitors acceleration thresholds at 300 nA.
3. **Event & Modulate:** Motion triggers an external GPIO interrupt. The MCU reads $X, Y, Z$ data over SPI, constructs an OOK frame (Preamble + WaveMatch Sync + Payload + CRC), and keys **Timer_A** configured to an **85 kHz square wave** to shunt the ADG902 to ground.

## File Map
* `main.c`: Boot sequence, power-rail checks, LPM sleep entry, and interrupt service routines (ISRs).
* `adxl362.c` / `adxl362.h`: Integrated low-level SPI routines and motion threshold register configuration.
* `backscatter.c` / `backscatter.h`: Timer_A CCR register management, 85 kHz subcarrier generation, and bitstream OOK serialization.

## Build Requirements
* **Toolchain:** TI Code Composer Studio (CCS) v12+ or `msp430-elf-gcc`
* **Optimization:** `-O2` or `-Os` with Linker Dead Code Elimination enabled.