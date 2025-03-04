# Custom Cable

If you want to make a custom USB-A 3.0 cable, you will need:

| Item | Amount | Link | Price (at time of writing) |Notes|
|---|---|---|---|----|
|USB-A 3.0 male ends|2|https://www.aliexpress.us/item/3256803918581184.html or https://www.aliexpress.us/item/2255801079732575.html or https://www.aliexpress.us/item/3256801764065903.html or https://www.aliexpress.us/item/3256805914053747.html or https://www.aliexpress.us/item/3256805068712110.html||Make sure you pick a USB 3.0 version! Also pay attention to shipping costs and lead times.|
|7+ strand wire |Your desired length|https://www.aliexpress.us/item/2255800380986172.html|$1.73 for 2 meters, 8 strands|For a proper USB 3 cable, you need at least 9 strands. The linked cable is 30AWG, which is very thin and unsuitable for USB 3 power transfer. If you wish to use the cable elsewhere, I suggest that you use at least 24AWG. For the linked cable, I recommend 8 strands as this puts the outer diameter at 3.5mm which is not *quite* as thick, but allows compatibility with commonly sized other parts. Note that a *proper* USB 3.0 cable would also include shielding and twisting of the pairs for signal reliability reasons, which is irrelevant for Apiaster.|


You will probably also want:

| Item | Amount | Link | Price (at time of writing) |Notes|
|---|---|---|---|----|
|Heat shrink|2|https://www.aliexpress.us/item/3256805506449553.html|$2.75 for 13mm, 1m, black|The *absolute minimum* inner diameter you can use is 9mm. You need more than a 2:1 shrink ratio. This is to cover up the cable ends.|
| Paracord | cable length|https://www.aliexpress.us/item/2255800708022724.html|$1.22 for 10 ft|Make sure the outer diameter is a bit larger than your cable. For example, for a 3.5mm cable outer diameter, 4mm paracord seems to be suitable.|
|PET expandable sleeving|cable length|https://www.aliexpress.us/item/3256801542457138.html|$0.96 per 5m| The outer diameter of this should be *smaller* than that of the paracord and cable, so that it expands around it to make a nice pattern. 3mm seems good for a 4mm paracord.|

I would then mostly follow [this video](https://www.youtube.com/watch?v=1WgCXG8qcVI), making adjustments for USB-A 3.0 instead of USB-C (and skipping the aviator connector).

## Wiring Diagram

![USB A 3.0 Cable Wiring Diagram](../images/usb3-cable-diagram.jpg)

Note that unlike USB 2.0, there are some internal wires exchanged. If you have only 7 wires, you can skip the connections marked in red and orange. If you have 8 wires, skip the orange.

# Chop Approach

What you could also always do is take two USB-A 3.0 to USB-C cables with designs that you like, chop them in half, and then reconnect the cables. Either with soldering and heat shrink, or with something fancier like a [9 pin GX16 connector](https://www.aliexpress.us/item/3256805937293382.html).