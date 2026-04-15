import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const DATA_DIR   = "./data";
const LEDGER     = `${DATA_DIR}/ledger.log`;
const PRIV_PATH  = "./padi_private.pem";
const PUB_PATH   = "./padi_public.pem";

// Generate Ed25519 keypair
const { publicKey, privateKey } = crypto.generateKeyPairSync("ed25519", {
  publicKeyEncoding:  { type: "spki",  format: "pem" },
  privateKeyEncoding: { type: "pkcs8", format: "pem" },
});

// Write keys to disk
fs.writeFileSync(PRIV_PATH, privateKey, { mode: 0o600 });
fs.writeFileSync(PUB_PATH,  publicKey);

console.log("\n✔ Keys generated");
console.log(`  Private key → ${PRIV_PATH}  (keep secret, never commit)`);
console.log(`  Public key  → ${PUB_PATH}\n`);
console.log("══ PASTE THIS INTO padi.ttl :authorizedPublicKey ══════════════\n");
console.log(publicKey);
console.log("═══════════════════════════════════════════════════════════════\n");

// Create data directory and genesis block
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// Inline canonicalize and hash for setup — no package imports needed
function canonicalize(obj) {
  if (obj === null)           return "null";
  if (typeof obj === "boolean") return JSON.stringify(obj);
  if (typeof obj === "number")  return Number.isInteger(obj) ? obj.toString() : obj.toPrecision(15);
  if (typeof obj === "string")  return JSON.stringify(obj.normalize("NFC"));
  if (Array.isArray(obj))       return "[" + obj.map(canonicalize).join(",") + "]";
  const keys = Object.keys(obj).filter(k => k !== "signature" && k !== "hash").sort();
  return `{${keys.map(k => `"${k}":${canonicalize(obj[k])}`).join(",")}}`;
}

function hash(data) {
  return crypto
    .createHash("sha256")
    .update(Buffer.from("PADI_SOVEREIGN_V1.9.7" + data, "utf8"))
    .digest("hex");
}

const genesis = {
  t: 0, h: 0, p: [],
  d: { system: "PADI_GENESIS", v: "1.9.7" },
  s: "ROOT", e: 0,
};
genesis.hash = hash(canonicalize(genesis));

if (!fs.existsSync(LEDGER)) {
  fs.writeFileSync(LEDGER, JSON.stringify(genesis) + "\n");
  console.log("✔ Genesis block written");
  console.log(`  Hash → ${genesis.hash}\n`);
} else {
  console.log("✔ Ledger already exists — genesis skipped\n");
}

console.log("Next steps:");
console.log("  1. Copy the public key above into packages/schemas/definitions/padi.ttl");
console.log("  2. Run: pnpm --filter @samuelmuriithi/schemas build");
console.log("  3. Run: pnpm --filter api-server start\n");