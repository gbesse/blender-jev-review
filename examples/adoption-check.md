# blender-jev-review — contrôle d’adoption · adoption check · comprobación de adopción

## Français

Point de départ local, après la préparation indiquée dans le README :

```sh
python3 -m examples.two_pass_review
```

Deux objets peuvent avoir le même nom visible. Vérifiez que la seconde passe retient l’identifiant de l’objet sélectionné et rejette un identifiant inventé ; confirmez ensuite le comportement dans Blender.

## English

Local starting point, after the setup described in the README:

```sh
python3 -m examples.two_pass_review
```

Two objects can share a visible name. Check that the second pass keeps the selected object ID and rejects an invented ID; then confirm the behavior in Blender.

## Español

Punto de partida local, después de la preparación descrita en el README:

```sh
python3 -m examples.two_pass_review
```

Dos objetos pueden compartir el nombre visible. Compruebe que la segunda pasada conserva el ID del objeto seleccionado y rechaza uno inventado; confirme después el comportamiento en Blender.
## Variante synthétique · Synthetic variation · Variante sintética

```text
selected=[{name:"Cube",id:"object-1"},{name:"Cube",id:"object-2"}]; choice="object-2"
```

FR : adaptez une copie de la fixture locale à cette situation, puis vérifiez le comportement décrit ci-dessus. Les valeurs sont illustratives, pas des résultats Jev mesurés.

EN: adapt a copy of the local fixture to this situation, then check the behavior described above. Values are illustrative, not measured Jev output.

ES: adapte una copia de la fixture local a esta situación y compruebe el comportamiento descrito arriba. Los valores son ilustrativos, no resultados Jev medidos.
