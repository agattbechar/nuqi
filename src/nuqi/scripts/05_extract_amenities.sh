#!/usr/bin/env bash
set -euo pipefail

INP="data/interim/nouakchott.osm.pbf"
OUT="data/interim/nouakchott_amenities.osm.pbf"

mkdir -p data/interim

# Keep only objects (n/w/r) where amenity is one of:
# health: hospital, clinic, doctors
# education: school
# markets: marketplace
osmium tags-filter -O "$INP" \
  nwr/amenity=hospital \
  nwr/amenity=clinic \
  nwr/amenity=doctors \
  nwr/amenity=school \
  nwr/amenity=marketplace \
  -o "$OUT"

echo "Wrote: $OUT"