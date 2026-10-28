# Vesktop Liquid Glass

Two themes for [Vesktop](https://github.com/Vencord/Vesktop) (Discord): iOS-style "liquid glass" with frosted
floating panels, pill-shaped account and server lists, springy hover and appear animations, a green speaking ring
that grows out of the avatar, and an **autumn** variant (warm amber/rust gradients, leaf and jack-o'-lantern
channel icons, leaf fall when you join a voice channel, light rain over the chat).

| file | what |
|---|---|
| `liquid-glass.theme.css` | the base theme: near-black, neutral glass |
| `liquid-glass-autumn.theme.css` | the autumn variant (generated from the base by `make-autumn.py`) |

Use **one** of them at a time.

## Install

**A. Online theme (updates itself).** Vesktop -> Settings -> Themes -> *Online Themes*, paste one URL:

```
https://raw.githubusercontent.com/ImGreaterThanOne/vesktop-liquid-glass/main/liquid-glass.theme.css
https://raw.githubusercontent.com/ImGreaterThanOne/vesktop-liquid-glass/main/liquid-glass-autumn.theme.css
```

**B. Files.** Run `python3 install.py` (it finds Vesktop's themes folder on Linux, macOS and Windows), or copy the
`.theme.css` files into that folder yourself, then enable the theme in Settings -> Themes.

## Notes

* **Font:** the themes use [Inter](https://rsms.me/inter/) (a stand-in for SF Pro). Install it for the intended look;
  otherwise Discord falls back to another font.
* **Sharp avatar (optional):** Discord loads your avatar in the account panel at 24 px. To show a sharp one, add this to
  *QuickCSS* with your own avatar URL (any size up to 256): `:root { --lg-avatar: url("https://cdn.discordapp.com/avatars/<id>/<hash>.webp?size=256"); }`.
  Without it everything works; you just get Discord's own small avatar. The avatar *glow* needs nothing.
* **Autumn channel icons** are picked by the channel type in the link's `aria-label`, so they work for Russian and
  English Discord. Private channels and live voice channels keep their original icons on purpose.
* **Rain off / softer:** `:root { --lg-rain-opacity: 0; }` in QuickCSS (autumn theme).
* **Class names** come from Discord's current build (`guilds__5e434`-style hashes). When Discord ships a UI update some
  rules may stop matching until the names are refreshed.
* Rebuild the autumn theme after editing the base: `python3 make-autumn.py`.

Client themes are not endorsed by Discord and technically go against its terms. Use at your own risk. Not affiliated
with Discord or Vencord.
