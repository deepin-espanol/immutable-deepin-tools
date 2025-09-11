#!/bin/bash
# update_translations.sh

# Usar pyside6-lupdate para generar archivos de traduccion .ts
pyside6-lupdate main.py resources/admin.py resources/snapshots.py -ts resources/langs/immutable-deepin-tools_es.ts
pyside6-lupdate main.py resources/admin.py resources/snapshots.py -ts resources/langs/immutable-deepin-tools_en.ts
pyside6-lupdate main.py resources/admin.py resources/snapshots.py -ts resources/langs/immutable-deepin-tools_pt.ts
pyside6-lupdate main.py resources/admin.py resources/snapshots.py -ts resources/langs/immutable-deepin-tools_zh_CN.ts

echo "Archivos .ts generados. Abre Qt Linguist para traducir:"
echo "linguist resources/langs/immutable-deepin-tools_es.ts"

# Compilar a .qm después de traducir
# pyside6-lrelease resources/langs/immutable-deepin-tools_es.ts