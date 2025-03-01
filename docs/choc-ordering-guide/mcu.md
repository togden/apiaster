# Choice #2: MCU

Your next choice is for the MCU of your keyboard, i.e. the brain that interprets key presses to identify what to send to the host device.

**Note that if you socket your MCU, as I recommend and demonstrate in this guide, you will be able to switch out the MCU with an "upgrade" at a later point in time.**

Here are your options:

|MCU|Price|Amount|Wireless|Notes|
|----|----|----|----|----|
|[RP2040-Zero](https://de.aliexpress.com/item/1005007650325892.html)|~$2-3 each|1| No | Both halves are connected with a USB A 3.0 cable, and the keyboard is connected to the host with a USB C cable.|
|[XIAO nRF52840](https://www.seeedstudio.com/Seeed-XIAO-BLE-nRF52840-p-5201.html)|~$10-12 each|1|Yes|Both halves are connected with a USB A 3.0 cable, the keyboard can be connected to the host via either Bluetooth or with a USB C cable.|
|[XIAO nRF52840](https://www.seeedstudio.com/Seeed-XIAO-BLE-nRF52840-p-5201.html)|~$10-12 each|2|Yes|The halves are connected via Bluetooth, the keyboard can be connected to the host via either Bluetooth or with a USB C cable going to a *prespecified* half.|
|[XIAO nRF52840 (different link)](https://www.seeedstudio.com/Seeed-Studio-XIAO-nRF52840-3PCS-p-5921.html)|$18-23|3|Yes| A set of 3 can be bought for \$23. Seeed currently offers a \$5 discount to first time signups to their newsletter. The third MCU is used as a dongle, significantly increasing the battery life when compared to having two XIAO controllers (but no difference when compared to only one with the halves connected via USB A 3.0)|

Even if you purchase and install multiple XIAOs, you can revert to using only one with little hassle.

Please click the links to doublecheck the prices for your region, as shipping and taxes may cause these to vary. If your choice involves a USB A 3.0 cable, you will also need to purchase (if you don't already have them) a USB A 3.0 cable and a set of USB 3.0 female connectors:

|Item|Amount|Notes|
|----|---- |----|
|[USB-A 3.0 Cable](https://de.aliexpress.com/item/1005001560424564.html)|1| A braided cable is recommended. Make sure you select a USB 3.0 cable, the linked store also sells USB 2.0 "color", which is useless.|
|[USB-A 3.0 Female Connectors](https://de.aliexpress.com/item/1005003729287891.html)|2|Sold in sets of 5. Pick the "90 degree warped mouth".|

If you're feeling *really* fancy, you could also make your own USB A 3.0 cable with a custom length & shaping using [these end pieces](https://www.aliexpress.com/item/4001266047327.html). An (untested) guide on this can be found [here](../custom-usb-cable.md).

[Continue with the RP2040-Zero.](./choc-zero.md)

[Continue with the XIAO nRF52840.](./choc-xiao.md)