# MCU Upgrade Guide

To upgrade from RP2040-Zero to XIAOs, you'll need to purchase the following items:

## Mandatory Components

| Item | Amount | Link | Price (at time of writing)|Notes|
|---|---|---|---|----|
|XIAO nRF52840|1-3|[Singles](https://www.seeedstudio.com/Seeed-XIAO-BLE-nRF52840-p-5201.html) or  [3-pack](https://www.seeedstudio.com/Seeed-Studio-XIAO-nRF52840-3PCS-p-5921.html)|$9.90 each or $23.39 for 3.| As discussed [here](./mx-ordering-guide/mcu.md). A "sense" version is also sold, but *entirely* unnecessary and just increases the price.|

You will also need batteries. Your choice is between a coin cell battery, and a LiPo:

| Item | Amount | Link | Price (at time of writing)| Type | Notes|
|---|---|---|---|----|----|
|Coin Cell|2|https://www.amazon.de/-/en/LIR2032H-Rechargeable-Battery-Charger-Lithium/dp/B08HRY4QRL|€9.69 for 4|Coin Cell|The code is "LIR2032H", any product with that should be correct unless dubious.|
|LiPo Battery|2|https://www.aliexpress.us/item/2251832478677289.html|€3.93 each|LiPo|A somewhat trustworthy source on Aliexpress. Alleged capacity of 100mAh. Make sure you pick "JST PH 2.0MM" as a connector.|
|LiPo Battery|2|https://bihuade.com/products/37v-140mah-501522-liter-energy-battery-polymer-lithium-ion-li-ion-battery-for-smart-watchblue-toothgps-speaker|€3.93 each|LiPo|The biggest battery that fits in the designed case (fine-tuning may allow a bigger battery). Reliably sourced directly from the manufacturer, but beware the shipping costs. Make sure you pick "JST PH 2.0MM" as a connector.|
|Coin Cell holder|2|https://de.aliexpress.com/item/1005007339595580.html|$1.51 for 10|Coin Cell|Identical product can be found from multiple sources.|
|BMS 1S|2|https://www.aliexpress.com/item/1005007047240735.html|$1.11 for 10|Coin Cell|Needed to protect the coin cell from overcharge/overdischarge (LiPo should have this built in). Identical product can be found from multiple sources.|
|JST PH 2 pin|2|https://de.aliexpress.com/item/1005004955655144.html|$1.12 for 100|LiPo|Pick the right angle version. You can also pick a 3 pin version.|

A *lot* of LiPo battery sources, especially on Aliexpress, are dubious. They tend to claim battery capacities far beyond the actual capacity, often ship lacking proper protection, and there is no way to tell if they might not explode in the future. The shops I linked are ones that I have had good experiences with.

The main advantage of the coin cell is in its availability and reliability. The main advantage of LiPo is in its capacity. Use the [ZMK Power Profiler](https://zmk.dev/power-profiler) to estimate your battery life (LIR2032H has 70mAh):
 * The nice!nano is a decent approximation of the XIAO's battery consumption
 * If you use a cable between halves then do not enable the "split keyboard" toggle
 * If you use a dongle, then both your halves will have "peripheral" levels of power consumption, and the dongle will have "central" levels of power consumption (but should be connected via USB so that's irrelevant).

I recommend the [prospector](https://github.com/carrefinho/prospector) if you want a fancy dongle, but a bare XIAO with nothing attached to it also works.

I expect that you should have leftover pins and sockets from your previous build. If not, buy more of those.

A final, optional item is:

| Item | Amount | Link | Price (at time of writing) |Notes|
|---|---|---|---|----|
|Pogo Pins|2|https://www.aliexpress.us/item/3256805909678051.html|$2.62 for 10| Make sure the leg at the bottom is 0.8mm thick (or thinner), the overall height is at least 5mm, and the height when compressed is at most 4.5mm (assuming round hole sockets, heights may vary depending on your sockets). These are definitely optional, they are used for advanced socketing, but you can easily use a diode leg instead. Only recommended if you are using SMD diodes and don't have any spare wire.|

With all of your parts, you can essentially just remove your RP2040-Zero from your PCB by wedging it out, and then follow the relevant parts of the [build guide](./build-guide/pcb.md).