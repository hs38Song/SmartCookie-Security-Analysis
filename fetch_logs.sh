DEST="$HOME/experiment_logs"
LOGS=(
  /tmp/client_h1.log
  /tmp/server_h2.log
  /tmp/attacker_h3.log
  /tmp/bloom_defender.log
  /tmp/accurate_attacker_h4.log
)

mkdir -p "$DEST"

echo "Retrieving logs into $DEST …"
for src in "${LOGS[@]}"; do
  if [ -f "$src" ]; then
    sudo cp "$src" "$DEST/"
    # fix ownership so you can read them without sudo
    sudo chown "$(id -u):$(id -g)" "$DEST/$(basename "$src")"
    echo "  ✓ $(basename "$src")"
  else
    echo "  ⨯ missing $(basename "$src")"
  fi
done

echo "Done."
