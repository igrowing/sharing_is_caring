# Replacing Tuya Firmware with OpenBeken on a CB3S / T1-3S Wi-Fi Switch

This guide turns a Tuya "1ch Wi-Fi switch module" into a fully local device that talks to Home Assistant over MQTT. No Tuya app and no cloud.

**Time needed:** 1–2 hours the first time.
**Difficulty:** Easy soldering (5 wires on small pads).

---

## ⚠️ Safety first — read this

- **Never work on the switch while it is connected to mains (230V).** Unplug it completely. Mains voltage can kill.
- Leave the device unplugged for a few minutes before opening it, so capacitors can discharge.
- During flashing, the module is powered **only** by the low-voltage 3.3V supply described below.
- Never connect **5V** to any pin of the module. It needs **3.3V** only.

---

## Step 0 — Identify which module you have

### Prepare the hardware

### Hardware

| Item | Why / notes |
|---|---|
| **USB-to-TTL serial adapter** (CH340, CP2102 or FT232) | Talks to the chip. Must support **3.3V logic**. If it has a 5V/3.3V jumper, set it to **3.3V**. |
| **3.3V power supply, at least 300 mA** | (Optional, can be supplied from USB) An **AMS1117-3.3 regulator board** powered from a USB charger or USB port is cheap and reliable. The 3.3V pin on most USB adapters is too weak and causes random failures. |
| Soldering iron with a **fine tip** | 300–350 °C is fine. |
| Thin solder and **flux** | Flux makes soldering small pads much easier. |
| Thin wires (~30 AWG, or cut Dupont jumper wires) | Keep them **short** (5–15 cm). Long wires cause flashing errors. |
| A multimeter | (Optional) To double-check GND and 3.3V pads. |
| A spare jumper wire or tweezers | For briefly touching CEN to GND (optional, see Step 6). |
| Isopropyl alcohol + old toothbrush | To clean flux afterwards. |

### Prepare the software

**📥 Downloads (quick links)**

| What | Link | Which file to download |
|---|---|---|
| **ltchiptool** (flashing tool, Windows) | <https://github.com/libretiny-eu/ltchiptool/releases/latest> | The `.exe` file under **Assets** |
| **OpenBeken firmware** | <https://github.com/openshwprojects/OpenBK7231T_App/releases> | Open the newest release, then under **Assets**: CB3S → `OpenBK7231N_QIO_<version>.bin`; T1-3S → `OpenBK7238_QIO_<version>.bin` |


Open the switch and look at the metal shield or the printed label on the Wi-Fi module.

| Label on module | Chip inside | Chip type to select in tools | Firmware file |
|---|---|---|---|
| **CB3S** | BK7231N | `BK7231N` | `OpenBK7231N_QIO_<version>.bin` |
| **T1-3S** | BK7238 | `BK7238` | `OpenBK7238_QIO_<version>.bin` |

Both modules have **exactly the same pins in the same places**, so the wiring below is identical. Only the chip type and firmware file differ.

> The pinout drawing used for this guide is labeled **T1-3S**. It is identical to CB3S module too.

Write down which one you have. You will need it in Steps 5 and 6.

### Open the switch and find the pads

1. Make sure the switch is **unplugged from mains**.
2. Open the case (usually clips or small screws).
3. Find the small Wi-Fi module with the metal shield and a zig-zag antenna printed at one end.

#### Where the pins are

Look at the module **from above** (the side with the metal shield), with the **antenna at the top**. The pins are the little half-holes along the edges:

```
              ANTENNA (top)
        ┌────────────────────┐
        │   ~~~~~~~~~~~~~~   │
  pin 1 ○│                  │○ pin 16  TX1   ◄── solder
  pin 2 ○│                  │○ pin 15  RX1   ◄── solder
  pin 3 ○│ CEN              │○ pin 14
  pin 4 ○│                  │○ pin 13
  pin 5 ○│                  │○ pin 12
  pin 6 ○│ TX2              │○ pin 11
  pin 7 ○│                  │○ pin 10
  pin 8 ○│ 3V3              │○ pin 9   GND   ◄── solder
         └──────────────────┘
          3V3 ◄── solder
```

| Pin | Name | Where (top view, antenna up) | Solder a wire? |
|---|---|---|---|
| 16 | **TX1** | Right side, **top** pad | ✅ Yes |
| 15 | **RX1** | Right side, **2nd** from top | ✅ Yes |
| 9 | **GND** | Right side, **bottom** pad | ✅ Yes |
| 8 | **3V3** (power) | Left side, **bottom** pad | ✅ Yes |
| 3 | **CEN** (reset) | Left side, **3rd** from top | Optional (see Step 6) |

> Compare with your pinout drawing before soldering. Note that the drawing's **bottom view** is mirrored compared to what you see from above.

> N.B.! You can use the +5V directly from UART converter. It takes the power from USB port of your computer. It is enough for flashing the switch. Identify the input pin of LDO which supplied the RF module. Instead of soldering the positive +3.3V wire, solder the positive +5V wire.

### Double-check with a multimeter (recommended)

- Set the multimeter to **continuity (beep)** mode.
- **GND pad** should beep against the board's ground (for example, the negative side of a large capacitor near the power supply section).
- The **3V3 pad** usually connects to the output of a small 3-pin regulator chip on the board.

If the checks match, you have the right pads.

---

## Step 1 — Solder the wires

1. Put a small amount of **flux** on the 4 pads: TX1, RX1, GND, 3V3 after the LDO or 5V before the LDO.
2. **Tin** the tip of each wire (put a little solder on the bare end).
3. Touch the wire to the pad and heat it briefly (1–2 seconds). The solder flows and the wire sticks.
4. Gently tug each wire to make sure it holds.
5. Check that **no solder bridges** connect neighboring pads. Use a magnifier or phone camera zoom.
6. Optional: tape the wires to the board with Kapton or electrical tape so they don't rip off the pads.

**Optional CEN wire:** Solder a 5th wire to CEN if you want. You can also just touch it briefly with a jumper wire later, or skip it and use the power-cycle method in Step 6.

---

## Step 2 — Connect everything

⚠️ **Mains still unplugged!**

Make these connections:

| Module pad | Connect to |
|---|---|
| **TX1** | USB adapter **RX** |
| **RX1** | USB adapter **TX** |
| **GND** | USB adapter **GND** *and* 3.3V supply **GND** |
| **3V3** | 3.3V supply **output (3.3V / VOUT)** |

Key points:

- **TX goes to RX, and RX goes to TX** — they cross over. This is the most common mistake.
- **All grounds must be connected together**: module, USB adapter, and 3.3V supply.
- **Do not** connect the USB adapter's 3.3V or 5V pin to anything.
- Leave the 3.3V supply **unpowered** for now (unplugged from USB).

Plug the **USB adapter** into your PC. In Windows **Device Manager → Ports (COM & LPT)**, note which **COM port** appeared (e.g., COM5).

---

## Step 3 — Make a backup of the original firmware (do not skip!)

The backup is your only way to restore the original Tuya firmware later. It can also be used to recover the original pin settings.

1. Start **ltchiptool**.
2. Choose **Read flash**.
3. Select the **chip family**:
   - CB3S → **BK7231N**
   - T1-3S → **BK7238**
4. Select your **COM port**.
5. Choose where to save the file (e.g., `backup_original.bin`).
6. Keep the default length (full flash, usually 2 MB).
7. Click **Start**. The log will say it is trying to connect.
8. **Now power on the module**: plug in the 3.3V supply. If the ltchiptool does not pick the module, turn the module off and on again. See Step 4 for how to trigger the connection if nothing happens.
9. Wait until reading finishes (1–3 minutes).
10. **Copy the backup file somewhere safe**, like cloud storage or a USB stick.

---

## Step 4 — How to "wake up" the chip for flashing

The chip only listens to the flasher for a short moment right after it starts up. So when ltchiptool says it's trying to connect, you need to **restart the module**. Choose one way:

**Method A — Power cycle (easiest):**
While ltchiptool is waiting, **unplug and re-plug the 3.3V supply** (or pull and reinsert its 3.3V wire). Repeat if it doesn't catch the first time.

**Method B — CEN reset:**
While ltchiptool is waiting, **briefly touch the CEN pad to GND** with a jumper wire or tweezers for about half a second, then release.

When it works, the log shows the chip was detected and reading or writing starts.

---

## Step 5 — Flash OpenBeken

1. In ltchiptool choose **Write flash**.
2. Click **Browse** and select the OpenBeken file you downloaded:
   - CB3S → `OpenBK7231N_QIO_<version>.bin`
   - T1-3S → `OpenBK7238_QIO_<version>.bin`
3. ltchiptool should detect the file and chip type automatically. Leave **"Auto-detect advanced parameters"** checked.
4. Select your COM port and click **Start**.
5. Restart the chip as in **Step 6** when it waits for connection.
6. Wait until it says flashing is **done**.

**If ltchiptool says the file is "Unrecognized":** Use BK7231GUIFlashTool instead. Select the chip type (BK7231N or BK7238) and the COM port, click the button to download the latest firmware, then flash. It also restarts the same way (Step 4).

---

## Step 6 — First start: connect the switch to your home Wi-Fi

After flashing, the switch doesn't know your Wi-Fi yet. So it creates **its own small Wi-Fi network** that you connect to with your phone or laptop, and it shows a setup web page. This is called the **setup portal**.

### 6.1 — Start the module

1. Unplug the 3.3V supply, wait 2 seconds, and plug it back in. The module now runs OpenBeken.
2. Wait about **30 seconds**.

### 6.2 — Connect your phone or laptop to the switch's network

1. On your phone, open **Settings → Wi-Fi** (on a laptop, click the Wi-Fi icon near the clock).
2. In the list of networks, look for a new one named like:
   - `OpenBK7231N_XXXXXXXX` (CB3S), or
   - `OpenBK7238_XXXXXXXX` (T1-3S)

   (The X's are random letters and numbers.)
3. Tap it to connect. It has **no password**.
4. Your phone will probably warn **"No internet connection"** or **"Internet may not be available"**. This is normal, because the switch is not connected to the internet.
   - **Android:** if asked *"Stay connected?"* or *"Keep Wi-Fi connection?"*, choose **Yes / Keep**.
   - **iPhone:** if a window pops up, tap **Cancel → Use Without Internet**.
5. **Turn off mobile data** on your phone for now. Otherwise the phone may quietly use mobile data instead, and the setup page won't open.

**Don't see the network?** Wait another minute and refresh the Wi-Fi list. Move the phone close to the switch. Check that the 3.3V supply is on.

### 6.3 — Open the setup page

The setup page usually does **not** open by itself. You have to open it:

1. Open a web browser (Chrome, Safari, Edge, Firefox).
2. Tap the **address bar at the very top** (where website addresses like `www.google.com` go), **not** a search box in the middle of the page.
3. Type `http://192.168.4.1` <- It is all numbers and dots, with no spaces.
4. Press **Enter / Go**.

You should see the **OpenBeken** page with buttons such as **Config**, **Restart**, and a toggle.

**Page doesn't open?**
- Wait a little, it takes time to Beken...
- Try a different browser.

### 6.4 — Enter your home Wi-Fi details

1. Tap **Config**.
2. Tap **Configure WiFi**.
3. Fill in:
   - **SSID:** the **name** of your home Wi-Fi network, written exactly as it appears on your phone, including capital letters and spaces.
   - **Password:** your home Wi-Fi password. Capital letters matter here too.
4. Tap **Submit / Save**.

> ⚠️ The switch works **only with 2.4 GHz Wi-Fi**. If your router has separate networks such as `MyHome` and `MyHome_5G`, choose the one **without** "5G". If you're not sure, it's usually the one without "5G" or "5GHz" in its name.

The switch restarts and joins your home network. Its own `OpenBK...` network **disappears** — that's a good sign.

5. Reconnect your phone to your **home Wi-Fi** and turn mobile data back on.

### 6.5 — Find the switch's new address (IP address)

Your router gives the switch a new address, like `192.168.1.57`. You need it to open the switch's page again. Ways to find it:

- **Router app or page:** open your router's app or admin page and look at the list of connected devices. Find one named `OpenBK7231N_...` or `OpenBK7238_...` and note its IP address.
- **Free phone app:** apps like **SimplyNet** (Android/iPhone) scan your network and list all devices with their IP addresses.

Type that address in your browser the same way as before, e.g., `http://192.168.1.57`, and the OpenBeken page opens again, now through your home Wi-Fi.

> **Tip:** In your router settings, you can "reserve" this IP address for the switch (often called *DHCP reservation* or *static lease*). Then it never changes, which makes Home Assistant setup more reliable.

**Write the IP address down.** You will use it in Steps 7, 8 and 9.

### 6.6 — If something went wrong

- **The switch doesn't appear on your home network, and the `OpenBK...` network is gone:** the Wi-Fi name or password was probably mistyped. Power the switch off and on again and wait a minute. If the `OpenBK...` network comes back, repeat 6.2–6.4. On most OpenBeken versions, switching power off and on **5 times quickly** (about 1 second on, 1 second off) forces the setup network to reappear.
- **Weak signal:** during setup the module runs from the bench supply, so keep it close to your router.

---

## Step 7 — Set up the pins (relay, button, LED)

OpenBeken needs to know which chip pin drives the relay, which one reads the button, and which one lights the LED. Each chip pin has a name like **P6** or **P26**.

### 9.1 — Where to enter pin settings

1. Open the switch's web page (`http://<its IP address>`, see Step 6.5).
2. Click **Config → Configure Module**.
3. You'll see a list of pins (P0, P1, … P26). Next to each pin there is:
   - a **dropdown** to choose the pin's **role** (what it does), and
   - a small **box** for the **channel** number (which on/off "switch" it belongs to).
4. After changing anything, click **Save** at the bottom, then go back to the main page and click **Restart**.

### 9.2 — Find out which pins your device uses

Choose one of these ways, easiest first:

**Option A — Ready-made template:**
Search your device name in the OpenBeken device list at <https://openbekeniot.github.io/webapp/devicesList.html>. If you find it, import the template through the device's web page (**Web App → Import**).

**Option B — Try the most common CB3S layout:**
Many CB3S relay switches use these pins. A wrong guess does no harm, so it's fine to try:

| Pin | Role | Channel |
|---|---|---|
| **P6** | `Rel` (relay) | `1` |
| **P26** | `Btn` (button) | `1` |
| **P9** | `LED` (shows relay state) | `1` |

**Option C — Find them by testing:**
Open **GPIO Doctor** (under **Config**). It lets you switch each pin on and off and listen for the relay **click**, and it shows live input states so you can press the physical button and see which pin changes. **Don't touch P10 and P11** — those are the serial pins.

### 7.3 — Test the relay and button

1. On the main page, click the **toggle**. Listen for the relay **click**.
   - If it turns on when it should be off, change the role from `Rel` to **`Rel_n`**.
2. Press the **physical button** on the switch. The toggle on the web page should change.
   - If it reacts on release instead of press, or behaves strangely, try **`Btn_n`** instead of `Btn`.

> With only the 3.3V bench supply, the relay may not click, because relays usually need the board's own power. That's normal. You'll test it properly after reassembly (Step 10).

### 7.4 — Test the LED

**Important:** if you pick the `WifiLED` role, the LED shows **Wi-Fi status**, not the relay state. It blinks while connecting and then stays steadily **on** (or steadily **off**) once connected. A LED that doesn't blink after connecting may be working correctly.

To be sure the LED pin is right, make the LED follow the relay for a moment:

1. In **Configure Module**, set the LED pin (e.g., **P9**) to role **`LED`**, channel **`1`**. Save and restart.
2. Click the toggle on the main page a few times.
   - **LED turns on and off with the relay:** ✅ correct pin.
   - **LED does the opposite** (on when relay is off): ✅ correct pin, just inverted. Use **`LED_n`** instead.
   - **Nothing happens:** it's the wrong pin. Set P9 back to *None*, then try the same test on other free pins, e.g., **P8, P7, P24, P14, P23**, one at a time. Or use **GPIO Doctor** to switch pins on and off and watch the LED.
3. Once you've found the LED pin, choose what you want it to show.

   ✅ **Tested and recommended for this switch: role `LED`, channel `1`.** The LED is then on while the relay is on.

   Other options:

| You want the LED to… | Role | Channel |
|---|---|---|
| Show the **relay state** (on = relay on) | `LED` | `1` |
| Same, but inverted | `LED_n` | `1` |
| Show **Wi-Fi status** (blink = connecting) | `WifiLED` | `0` |
| Wi-Fi status, inverted | `WifiLED_n` | `0` |

Save and restart after the final choice.

---

## Step 8 — Reassemble

1. **Unplug** the 3.3V supply and USB adapter.
2. **Desolder the wires** from the module pads.
3. Clean flux residue with isopropyl alcohol and a toothbrush, then let it dry fully.
4. Check again for solder bridges.
5. Close the case completely.
6. Only now connect the switch back to mains.
7. Wait about 30 seconds, then open the device's web page again (same IP address as before) and click the toggle. The relay should now **click**.

Future firmware updates can be done **over Wi-Fi** from the OpenBeken web page (**OTA**), so you won't need to open the switch again.

---

## Step 9 — Pair with Home Assistant (MQTT)

Do this with the switch reassembled and powered from mains.

### In Home Assistant

Assuming you already have MQTT broker up and running. Recall its username and password.

### In OpenBeken (device web page)

1. Go to **Config → Configure MQTT**.
2. Fill in:
   - **Host:** your Home Assistant IP address (do not use FQDN.)
   - **Port:** `1883`
   - **Client topic:** a unique name, e.g., `switch_kitchen`
   - **User / Password:** the user you just recalled
3. Save. The main page should show **MQTT connected** after a few seconds.
4. Go to **Config → Home Assistant Configuration** and click **Start Home Assistant Discovery**.

### Back in Home Assistant

Go to **Settings → Devices & Services → MQTT**. Your switch should appear as a new device. Toggle it from Home Assistant to confirm it works. 🎉

---

## Step 10 (optional) — Make it a "push button" (0.3-second pulse)

Use this if the switch should act like a **doorbell or gate button**: one command closes the relay for **0.3 seconds** and opens it again automatically.

The switch does this **by itself**. Home Assistant only sends a normal "ON". This is safer than timing it from Home Assistant: if Wi-Fi drops right after "ON", the switch still opens the relay after 0.3 seconds and never stays closed.

### 10.1 — Create the two script files

OpenBeken runs a startup file called `autoexec.bat` (similar to "rules" in Tasmota). We add two small files:

1. Open the switch's web page (`http://<its IP address>`).
2. Click **Config**, then **Web App** (Web Application). A new page opens.
3. Go to the **Filesystem** tab.
4. Create a new file named exactly **`pulse.bat`** with this content:

   ```
   delay_ms 300
   setChannel 1 0
   ```

   This means: wait 300 milliseconds (0.3 s), then switch the relay off.

5. Create a second file named exactly **`autoexec.bat`** with this content:

   ```
   addChangeHandler Channel1 == 1 startScript pulse.bat *
   ```

   This means: every time the relay turns on, run `pulse.bat`.

6. **Save** both files.
7. Go back to the main page and click **Restart**.

> 💡 To change the pulse length, change `300` in `pulse.bat` (for example `500` = half a second, `1000` = one second).

### 10.2 — Make the relay always start off

So a power cut never leaves the relay closed when power returns:

1. Go to **Config → Configure Startup**.
2. Set channel **1** to start **off** (`0`).
3. Save.

### 10.3 — Test it

1. On the main page, click the toggle. The relay should **click twice quickly** (on, then off), and the toggle should jump back to off by itself.
2. Press the switch's own **physical button**. Same effect: a short 0.3-second pulse.

   Nothing extra is needed for the button. It is still set as `Btn` on channel `1` (Step 9), so it switches the relay on, and the script switches it off again 0.3 s later. Pressing it again within those 0.3 seconds just ends the pulse slightly early, which doesn't matter in practice.

3. The LED (role `LED`, channel `1`) flashes briefly with each pulse.

**If it doesn't work:** open the log on the device's web page (or the serial log on TX2). If you see *"unknown command"* for `delay_ms` or `startScript`, your OpenBeken version uses different command names. Update the firmware (Config → OTA) or check the OpenBeken command list for your version.

### 10.4 — Use it from Home Assistant

**Simplest way:** use the switch entity created in Step 9. Turn it **on** (from a dashboard, automation or script) and the device pulses and reports itself off again.

**Nicer way — a real "button" in Home Assistant:**
Add this to Home Assistant's `configuration.yaml` (for example with the *File editor* or *Studio Code Server* add-on), replacing `switch_kitchen` with the **Client topic** you set in Step 9:

```yaml
mqtt:
  button:
    - name: "Push button pulse"
      command_topic: "cmnd/switch_kitchen/POWER"
      payload_press: "ON"
```

Then go to **Developer tools → YAML → Check configuration**, and if it's OK, **Restart** Home Assistant. A new button entity "Push button pulse" appears. Each press sends one pulse.

> If your `configuration.yaml` already has an `mqtt:` section, add the `button:` part under the existing `mqtt:` line instead of creating a second one.

---

## Troubleshooting

| Problem | Try this |
|---|---|
| ltchiptool never connects | Swap TX and RX wires. Check all grounds are connected. Restart the chip (Step 4) several times while it waits. |
| Connects, then fails midway | Shorten the wires. Use a stronger 3.3V supply. Try a lower baud rate. |
| Wrong chip type error | Recheck the module label (Step 0). T1-3S needs **BK7238**, CB3S needs **BK7231N**. |
| No `OpenBK...` Wi-Fi network after flashing | Power cycle the module. Make sure you flashed the correct `_QIO_` file for your chip. |
| Communication garbled or impossible | Some boards have a second chip wired to TX1/RX1. In that case the module may need to be removed from the board for flashing (ask for help first). |
| Device doesn't appear in Home Assistant | Check MQTT is "connected" on the device page. Check the user/password. Click **Start Home Assistant Discovery** again. |
| Want to go back to Tuya | Use **Write flash** with your `backup_original.bin`. |
