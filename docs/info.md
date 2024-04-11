<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

If `r` is high, then a counter wil becaome 0.(`out = 0000_0000`).
If `r` is low, the output pins are shifted to right hand side and reversed (`out = {~out[size],out[0:size-1]}`).

## How to test

Set `r` high and observe that the counter is output on the output pins ( `out`) .

Set `r` low and observe that the output pins are shifted to right hand side and reversed( `out = {~out[size],out[0:size-1]}`).

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
