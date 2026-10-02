# Blender Jev Review

Review metadata for the objects you explicitly select, then jump back to the exact objects that triggered declared scene-hygiene criteria. Jev answers finite questions and selects existing object IDs; it never writes critique or edits the scene.

## Install

Zip the `blender_jev_review` directory, then use **Edit → Preferences → Add-ons → Install from Disk**. The panel appears under **3D View → Sidebar → Jev**. The TypeSafe API key is held in `WindowManager` with `SKIP_SAVE` and is not written into the `.blend` file.

The shipped alpha pack checks ambiguous naming, suspicious scale metadata, and unclear material naming. These are review hints—not geometry validation, accessibility certification, or a replacement for an art lead.

## Try the two-pass review offline

Run `python3 -m examples.two_pass_review`. A synthetic first answer raises an ambiguous-name issue; a second answer points to a selected object ID. The example also shows an invented object ID being rejected. No Blender installation, API key or network call is required, and this does not replace an in-host add-on test.

## Test

```bash
python3 -m unittest discover -s tests -v
ruff check .
python3 -m compileall -q blender_jev_review
```

No test contacts Jev. Blender was not installed in the build environment, so add-on registration and viewport focus still require an in-host smoke test.

MIT — see [LICENSE](LICENSE).

