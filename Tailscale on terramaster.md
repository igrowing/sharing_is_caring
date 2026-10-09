# How to run Tailscale on Terra Master NAS

Abbreviations:
- TNAS - Terra Master NAS
- VPN  - Virtual private network

## Problem

Tailscale is one of VPNs which allows to connect different devices in different locations in one network. Like many other VPN. If you use ZeroTier, it is one of "known apps" on TNAS. However, if your netowrk runs on TailScale... Here is the trouble.

1. Tailscale is not among "known apps" on TNAS.
2. [Terramaster community](https://forum.terra-master.com/en/viewtopic.php?t=4168) points to [unofficial app builds](https://tmnascommunity.eu/download/tailscale/). New and old builds are failing with "404 Not found" error.

## Solution

Run Tailscale as docker not from custom installed app but from command line. It is recoverable one-time setup. Shoot and forget.

1. Open your browser and go to the Tailscale admin console: login.tailscale.com/admin/settings/keys
2. Click Generate auth key.
3. Check the box for Reusable (this prevents the key from expiring if the NAS reboots multiple times).
4. Click Generate key and copy the resulting string (it will start with `tskey-auth-`).
5. Connect to the NAS over SSH or open terminal in WebUI.
6. Replace the `xxxxxx` with your key you copied in previous step and type:
```
docker run -d \
  --name=tailscale \
  --restart=unless-stopped \
  --network=host \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -e TS_AUTHKEY="tskey-auth-xxxxxx" \
  -e TS_EXTRA_ARGS="--accept-dns=false" \
  -e TS_STATE_DIR="/var/lib/tailscale" \
  -v /Volume1/docker/tailscale/state:/var/lib/tailscale \
  -v /dev/net/tun:/dev/net/tun \
  tailscale/tailscale
```

7. Find the TNAS in your [Tailscale admin console](https://console.tailscale.com/admin/machines) --> 3-dot menu --> Disable key expire

To prove this worked without waiting for a full NAS reboot, you can run `docker restart tailscale` and then check your [Tailscale admin console](https://console.tailscale.com/admin/machines). The NAS will remain connected.