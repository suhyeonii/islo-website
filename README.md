# Islo introduction website

A single-page, Korean/English introduction to the Islo iPhone cycling app.
The app is **in development and not yet publicly released**.

- Website: https://suhyeonii.github.io/islo-website/
- English introduction: https://suhyeonii.github.io/islo-website/?lang=en
- No app source code, API keys, ride archives, or conversation records belong here.
- No analytics, remote fonts, third-party scripts, or app downloads are included.
- `assets/` contains resized, profile-redacted screenshots. `img/` is private local input and must never be published or committed.
- Map and tourism credits embedded in screenshots are retained. Screenshots depict a development build; features and UI may change.
- Garmin rear-radar integration is explicitly identified as being considered, not implemented or approved.

## Preview and check

Run `python3 validate_site.py` for local validation.
To preview manually, run `python3 -m http.server 8080` in this folder, then visit http://localhost:8080.

## Publication boundary

This folder is maintained alongside the private app repository, but the public repository has a **new, independent Git history**.
Publish only the explicit allowlist in `validate_site.py` after validation. Never change the visibility of the app repository, copy its Git history, or push its parent directory.

The standalone public repository serves its root through GitHub Pages on the `main` branch. Website updates should go only to `suhyeonii/islo-website`.
