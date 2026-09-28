\# Bistatic Batteryless IoT Sensor Network

> Unidirectional RF Energy Harvesting \& Subcarrier Cross-Polarized Backscatter



A fully batteryless, event-driven sensing system operating in India's 865–867 MHz unlicensed UHF band. The network replaces active RF transmitters on edge devices with passive subcarrier backscatter modulation powered by beamed RF energy, completely eliminating battery maintenance.



\---



\## System Overview \& Core Innovations



1\. \*\*Bistatic Cross-Polarization Isolation\*\*

&#x20;  \* \*\*Problem:\*\* Direct Tx-to-Rx self-jamming blinds the receiver to microwatt backscatter reflections.

&#x20;  \* \*\*Solution:\*\* The Tx Base Station beams a \*\*Vertically Polarized\*\* wave. The Rx Base Station uses a \*\*Horizontally Polarized\*\* Yagi, achieving high passive cross-polarization isolation. The sensor node's dipole is tilted at \*\*45°\*\*, capturing vertical energy for harvesting while reflecting a mixed wave with horizontal components for the Rx.



2\. \*\*Cold-Start Deadlock Resolution (Shunt Topology)\*\*

&#x20;  \* \*\*Problem:\*\* Series RF switches block incoming RF when storage capacitors are completely drained (0V).

&#x20;  \* \*\*Solution:\*\* An Analog Devices ADG902 RF switch is placed in \*\*parallel (shunt)\*\* between the antenna trace and ground. At 0V, the switch defaults to High-Impedance (open), routing 100% of incoming RF directly to the e-peas AEM30940 PMIC. To transmit, the MCU drives the switch closed, shorting the antenna to ground ($\\Gamma = -1$) to generate backscatter contrast without breaking the cold-start charging path.



3\. \*\*Subcarrier Backscatter (85 kHz Offset)\*\*

&#x20;  \* To prevent baseband noise interference from the Tx carrier, the edge node modulates incoming 866.3 MHz energy using an \*\*85 kHz square wave\*\*.

&#x20;  \* This creates an upper sideband at \*\*866.385 MHz\*\*, completely isolated from the primary carrier while remaining within regulatory spectrum limits.



4\. \*\*WPC 2021 Regulatory Compliance (India)\*\*

&#x20;  \* \*\*Tx Base Station (Table IV - RFID Applications):\*\* Emits at 866.3 MHz. Duty cycle is hardware-limited to \*\*4.0 s ON, 100 ms OFF\*\*. Conducted power is digitally attenuated to match the +12 dBi Yagi gain, capping effective radiated power strictly at \*\*2 Watts e.r.p. (+33 dBm)\*\*.

&#x20;  \* \*\*Sensor Node (Table II - Tracking and Data Acquisition):\*\* The 85 kHz sideband operates strictly within the allowed 200 kHz channel boundary ($866.3 \\pm 0.1\\text{ MHz}$), leaving a 15 kHz guard band.



\---



\## Repository Structure



```text

.

├── edge\_node\_msp430/         # Batteryless Edge Node Firmware

│   ├── main.c                # Cold-start state machine \& power-mode coordination

│   ├── adxl362.c / .h        # SPI driver \& 300 nA wake-up configuration

│   ├── backscatter.c / .h    # Timer\_A 85 kHz PWM subcarrier \& OOK modulator

│   └── README.md

│

├── tx\_station\_esp32/         # Power Transmitter Base Station Firmware

│   ├── main.cpp              # 4s-ON/100ms-OFF duty-cycle state machine \& PA control

│   ├── cc1200\_tx.cpp / .h    # 866.3 MHz CW generation \& power attenuation routines

│   └── README.md

│

├── rx\_station\_esp32/         # Data Receiver Base Station Firmware

│   ├── main.cpp              # Packet reception ISR \& USB serial telemetry

│   ├── cc1200\_rx.cpp / .h    # 866.385 MHz OOK reception \& WaveMatch sync

│   └── README.md

│

└── README.md                 # Root documentation

