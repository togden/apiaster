# Selecting The Case

Rather than modelling the case directly using CAD software, I used build123d (a Python package) to generate the case. I took advantage of this to make the case highly customisable by passing in various build flags:

|Command|Options|Default|Description|
|---|---|---|---|
|`--side`| {left,right} |both|   Which sides of the keyboard to build the case for. Note that your halves may differ e.g. in the choice of MCU.|
|`--export-stl`  |true/false|false|        Save case to file|
|`--no-show` |true/false|false|           Skip rendering case using ocp_vscode|
|`--low-case`  |true/false|false|          If enabled, this will lower the height of the tray and frame such that they stop at the switch snap-on point. (You may need to expose some components)|
|`--switch`| {mx,choc} |choc|   What type of switches are used|
|`--mcu`|{xiao,rp2040-zero,either}|either| MCU used. Will error if rp2040-zero is tried to be put on the RHS. 'either' will expose the MCU, similar to '--expose'. If you wish to be flexible between the two *and* cover the MCU, it is recommended that you print the frame with 'either', and print the tray with the MCU you're currently using. The "either" option is mostly for people who are ordering the case from somewhere, not for those printing it themselves.|
|`--smd-mcu`  |true/false|false|          Set this flag if MCU is mounted SMD|
|`--mcu-socket-height`| any number| 4.7| The height of the sockets in millimeters above the PCB. Default is 4.7mm (height of round pin sockets)|
|`--battery` |{none,coin,lipo}|none| Will error if 'xiao' or 'either' is selected as mcu and this is 'none'. |
|`--no-usb-a`  |true/false|false|Set this flag if you're using a xiao and there will be no usb-A 3.0 port.|
|`--block-usb` |true/false|false|Set this flag if you're using a xiao and there is a soldered usb-A 3.0 port that you wish to cover up.|
|`--tenting`| {none,magsafe,puck} | none|  Integrated tenting options. A magsafe sticker (inner diameter 46mm, outer diameter 56mm, thickness 0.7mm or less) or the SplitKB tenting puck. Default: 'none'|
|`--smd-diodes`  |true/false|false| Set this flag if you are using SMD diodes. Will slightly reduce the height of the case. | 
|`--expose` |[{mcu,battery,usb} ...]| none of them| Select components which shouldn't be covered up by the tray. Note that 'battery' only has an effect if 'coin' is selected.|
|`--outer-keys`| {all,upper-1.5u,upper-1u,lower,none}| all|Which outer pinky keys should be enabled. All sets the upper key to 1.5u.|
|`--inner-index`| {all,reduced,flex}|flex|Adjust the number and position of the inner index keys for better comfort. Flex allows either configuration to be used. I recommend the frame to be printed in flex, with the tray printed in whichever configuration you desire.|
|`--remove-num-row`   |true/false|false|   Removes the num row keys by covering them up with the tray.|
|`--thumb-type`| {ripple,all-1u,classic,flex}|flex|Select what thumb cluster type should be used. Classic is 1u-1u-1.5u. Flex allows for any of the three options, but may be less stable. I recommend the frame to be printed in flex, with the tray printed in your desired configuration.|
|`--thumbs` |[{reachy,tucky,middle} ...]| all of them| Select which thumbs to use. |
|`--thumb-adjustment` |three numbers x,y,r|0,0,0| Move the thumb cluster. --thumb-adjustment x,y,r where x is the number of mm that the cluster should be moved inwards, y is the number of mm that the cluster should be moved downwards, and r is the clockwise rotation in degrees around the outermost down-most corner of the cluster. Be aware that negative values are not permitted, as these will cause collision with the PCB.|
|`--pinkies` |[{upper,home,lower} ...]|all of them| Select which pinky keys to use. Default all.|

There are also some options related to rendering and export names. Use `-h` to see the help menu.

To make your life easier, I have pre-generated a number of cases for you. These can be found [here](../case/stl). If you are 3D printing it yourself and are running XIAOs, also print two copies of `apiaster-xiao-button.stl`. If you're ordering the case from a big company it's not worth purchasing these as they're so tiny, but an individual Etsy printer fellow might be helpful.

Once you have the case of your choice, follow the [case assembly guide](./build-guide/case.md).

## Running The Case Generator

To *run* this generator, my suggested way of doing so is with VSCode. Follow [this guide](https://github.com/bernhard-42/vscode-ocp-cad-viewer?tab=readme-ov-file#installation) to get it all set up, then run [this file](../case/make_case.py). You will need to add some command line flags, as the base without any command line flags (intentionally) will not run.