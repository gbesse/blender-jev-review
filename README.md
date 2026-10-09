# Blender Jev Review

Review metadata for the objects you explicitly select, then jump back to the exact objects that triggered declared scene-hygiene criteria. Jev answers finite questions and selects existing object IDs; it never writes critique or edits the scene.

## Install

Build or zip the `blender_jev_review` directory, which contains Blender's extension manifest, then use **Edit → Preferences → Add-ons → Install from Disk**. The panel appears under **3D View → Sidebar → Jev**. The TypeSafe API key is held in `WindowManager` with `SKIP_SAVE` and is not written into the `.blend` file.

The shipped alpha pack checks ambiguous naming, suspicious scale metadata, and unclear material naming. These are review hints—not geometry validation, accessibility certification, or a replacement for an art lead.

## Try the two-pass review offline

The synthetic example now selects two objects with the same visible name and locates the second one by its stable candidate ID. Run `python3 -m examples.two_pass_review`; the script also rejects an invented object ID. / L'exemple distingue deux objets de même nom par identifiant et rejette un identifiant inventé. / El ejemplo distingue dos objetos con el mismo nombre por identificador y rechaza uno inventado.

Run `python3 -m examples.two_pass_review`. A synthetic first answer raises an ambiguous-name issue; a second answer points to a selected object ID. The example also shows an invented object ID being rejected. No Blender installation, API key or network call is required, and this does not replace an in-host add-on test.

## Test

```bash
python3 -m unittest discover -s tests -v
ruff check .
python3 -m compileall -q blender_jev_review
```

No test contacts Jev. Blender was not installed in the build environment, so add-on registration and viewport focus still require an in-host smoke test.

MIT — see [LICENSE](LICENSE).

## October 2026 improvement · Amélioration d’octobre 2026 · Mejora de octubre de 2026

A selection above 255 objects now stops the review instead of silently dropping objects. Focus uses the reviewed object ID and reports a deleted object.

Une sélection de plus de 255 objets arrête désormais la revue au lieu d’omettre des objets sans avertissement. La focalisation utilise l’identifiant revu et signale un objet supprimé.

Una selección de más de 255 objetos detiene la revisión en vez de omitir objetos sin aviso. El enfoque usa el identificador revisado y avisa si se eliminó el objeto.

## Contrôle d’adoption · Adoption check · Comprobación de adopción

[Français : essayer un cas concret](examples/adoption-check.md) · [English: try a concrete case](examples/adoption-check.md) · [Español: pruebe un caso concreto](examples/adoption-check.md).
