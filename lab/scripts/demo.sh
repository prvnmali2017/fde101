#!/usr/bin/env bash
set -euo pipefail

API="${API_URL:-http://localhost:8000}"

echo "==> RetailCo FDE Lab Demo"
echo "    API: $API"
echo ""

health=$(curl -sf "$API/health" 2>/dev/null) || {
  echo "ERROR: API not reachable at $API"
  echo "Start the server first: uvicorn src.api.main:app --reload --port 8000"
  exit 1
}
echo "Health: $health"
echo ""

questions=(
  "What is the return policy?"
  "How long does standard shipping take?"
  "What is the status of order ORD-1001?"
  "Can I return an opened item?"
)

for q in "${questions[@]}"; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Q: $q"
  echo ""
  response=$(curl -sf -X POST "$API/chat" \
    -H "Content-Type: application/json" \
    -d "$(QUESTION="$q" python3 -c "import json, os; print(json.dumps({'message': os.environ['QUESTION']}))")")
  echo "$response" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('A:', d['reply'][:500])
print('   Sources:', d.get('sources', []))
print('   Tools:', [t['tool'] for t in d.get('tool_calls', [])])
print('   Mode:', d.get('mode'))
"
  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Demo complete. Open $API for the web UI."
