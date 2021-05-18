# Drawing

이 프로젝트는 윈도우의 `그림판`과 같은 기능을 제공하는 리눅스 데스크톱 프로그램입니다.

기존 프로젝트에 헌글 번역을 추가하고 하모니카 OS (>=4.0) 에서 사용할 수 있도록 빌드한 버전입니다.

* upstream : https://github.com/maoschanz/drawing
* 한국어 번역 PR : https://github.com/maoschanz/drawing/pull/381

![drawing](./documentation/drawing.png)

## Install on HamoniKR
하모니카 사용자는 다음과 같이 설치할 수 있습니다.
```
sudo apt update 
sudo apt install drawing=0.8.1hamonikr2
```
## Install on Ubuntu(>=20.04)
우분투 사용자는 다음과 같이 설치할 수 있습니다.
```
wget -qO- https://pkg.hamonikr.org/add-hamonikr.apt | sudo -E bash -

sudo apt install drawing=0.8.1hamonikr2
```


## A simple drawing application for Linux.

This application is a basic image editor, similar to Microsoft Paint, but aiming
at the GNOME desktop.

PNG, JPEG and BMP files are supported.

[<img alt="" height="100" src="https://gitlab.gnome.org/Teams/Circle/-/raw/master/assets/button/circle-button-i.svg">](https://circle.gnome.org/)

Besides GNOME, some more traditional design layouts are available too, as well
as an [elementaryOS layout](./docs/screenshots/0.8/elementary_labels.png). It
should also be compatible with the *Pinephone* and *Librem 5*
[smartphones](./docs/screenshots/0.6/librem_menu.png).

## Screenshots

### Default user interface (for GNOME/Budgie)

![UI for GNOME and Budgie, here with the main menu opened](./docs/screenshots/0.8/gnome_menu.png)

[More screenshots](https://maoschanz.github.io/drawing/gallery.html)

----

## Installation

### Last stable version

>**Recommended**

You can install it from flathub.org using the instructions on
[this page](https://flathub.org/apps/details/com.github.maoschanz.drawing).

[<img alt="" height="100" src="https://flathub.org/assets/badges/flathub-badge-en.png">](https://flathub.org/apps/details/com.github.maoschanz.drawing).

### Other packages available

[![Packaging status](https://repology.org/badge/vertical-allrepos/drawing.svg)](https://repology.org/project/drawing/versions)

- Ubuntu 18.04, 20.10 and 21.04: [PPA](https://launchpad.net/~cartes/+archive/ubuntu/drawing/)
- [Gentoo package](https://gitlab.com/src_prepare/src_prepare-overlay/-/tree/master/media-gfx/drawing) from an external overlay
- ["Snap" package](https://snapcraft.io/drawing)

### Unstable/nightly version

[See here](./CONTRIBUTING.md#install-from-source-code) to install and test the
app from source code.

----

### Available languages

If your language is not here, or is incompletely translated, you can
[contribute](./CONTRIBUTING.md#translating) to the translations.

<!-- TODO just @ their account instead of writing full links myself? -->

| code | name         | complete*? | main translators                          |
|------|--------------|------------|-------------------------------------------|
| cs   | Czech        | 96%        | [Vojtěch Perník](https://github.com/pervoj)
| da   | Danish       | 92%        | [scootergrisen](https://github.com/scootergrisen)
| de   | German       | 99%        | [Onno Giesmann](https://github.com/Etamuk)
|      | English      | 100%       | help welcome **                           |
| es   | Castillan    | 100%       | [Adolfo Jayme-Barrientos](https://github.com/fitojb) and [Xoan Sampaiño](https://github.com/xoan)
| eu   | Basque       | 88%        | [alexgabi](https://github.com/alexgabi)
| fi   | Finnish      | 75%        | [MahtiAnkka](https://github.com/mahtiankka)
| fr   | French       | 100%       |                                           |
| he   | Hebrew       | **39%**    | [moriel5](https://github.com/moriel5) and [Shaked Ashkenazi](https://github.com/shaqash)
| hr   | Croatian     | 78%        | [Milo Ivir](https://github.com/milotype)  |
| hu   | Hungarian    | **62%**    | [Kálmán „KAMI” Szalai](https://github.com/kami911)
| id   | Indonesian   | 76%        | [Ghani Rafif](https://github.com/ekickx)  |
| it   | Italian      | 97%        | [Jimmy Scionti](https://github.com/amivaleo) and [Albano Battistella](https://github.com/albanobattistella)
| ja   | Japanese     | 100%       | [rlbxku1r](https://github.com/rlbxku1r)   |
| nl   | Dutch        | 100%       | [Heimen Stoffels](https://github.com/Vistaus)
| pl   | Polish       | **72%**    | [Piotr Komur](https://github.com/pkomur)  |
| pt_BR | Br. portuguese | 81%     | [Antonio Hauren](https://github.com/haurenburu) and [ArthurBacci64](https://github.com/ArthurBacci64)
| ru   | Russian      | 99%        | [Artem Polishchuk](https://github.com/tim77) and [Ser82-png](https://github.com/Ser82-png)
| sv   | Swedish      | 100%       | [Åke Engelbrektson](https://github.com/eson57)
| tr   | Turkish      | 100%       | [Serdar Sağlam](https://github.com/TeknoMobil) and [serkan-maker](https://github.com/serkan-maker)
| zh_CN | Chinese, simpl. | 80%    | [OverflowCat](https://github.com/OverflowCat)
| zh_TW | Chinese, tradi. | 81%    | [pan93412](https://github.com/pan93412), [OverflowCat](https://github.com/OverflowCat), [張修銘](https://github.com/cges30901)

\*Completion percentages correspond to **the next** major version, still in
development.

\**Concerning the "original version" in english: all the labels are here, but
i'm **not** a native english speaker, so there might be mistakes. If you find
incorrect english labels, please report an issue about it.

----

### Tools

(last update: **version 0.8.0**)

*Tools in italic can be disabled.*

#### Classic tools

General options for these tools: colors, use antialiasing, size, …

- Pencil (options: dashes, line shape, …)
- *Brushes (pressure sensitive)*:
	- *Simple round brush*
	- *Hairy brush*
	- *Airbrush*
	- *Calligraphic nibs*
- *Eraser* (options: blur, mosaic, transparency, solid color, …)
- *Highlighter* (options: highlight on dark background)
- Line (options: arrow, dashes, gradient, …)
- Curve (options: arrow, dashes, …)
- Insert text (options: font, shadow/outline, font size, …)
- *Insert points (options: shape of the points, include a number, …) to help captioning*
- Shape (options: filling style, outline style, gradient, …):
	- rectangle
	- rounded rectangle
	- circle
	- oval
	- polygon
	- free shape
- *Color picker*
- *Paint (options: remove a color, …)*

#### Selection tools

These tools allow you to define an area (rectangle or free), which you can move,
cut, copy, paste, edit with any transformation tool, export, open as a new
image, etc.

- Rectangle selection
- Free shape selection
- *Adjacent color selection*

#### Transformation tools

These tools can edit the whole image, or edit a selected part of it.

- Crop
- Scale (options: keep proportions or not)
- Rotate (rotate or flip)
- Filters:
	- Saturation (increase or decrease)<!-- - Veil -->
	- Transparency
	- Increase contrast
	- Blur (various types)
	- Pixelization
	- Invert colors
<!-- - Skew (horizontally or vertically) -->

----

### Settings

The settings are managed by the `Gio.Settings` abstraction, which will probably
corresponds to the `dconf` database once the app is installed as a native
package.

With flatpak however, the settings are stored in a key-value file, which can be
found (and edited) at `~/.var/app/com.github.maoschanz.drawing/config/glib-2.0/settings/keyfile`.

----

[Donations (paypal)](https://paypal.me/maoschannz)

[To contribute](./CONTRIBUTING.md)

the code is under GPL3, some tools icons are from [here](https://github.com/gnome-design-team/gnome-icons/tree/master/art-libre-symbolic) or from the Adwaita theme.

