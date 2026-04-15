import express from 'express';
import { PadiEngine } from '@samuelmuriithi/sovereign-node';

const app = express();
const port = 3000;
const engine = new PadiEngine();

async function startGateway() {
  console.log("\n--- [PADI Sovereign Bureau: API Gateway] ---");
  
  // Initialize the Sovereign Engine logic
  await engine.start();

  app.get('/', (req, res) => {
    res.json({ 
      status: "Operational", 
      identity: "Nairobi-01-Node",
      timestamp: new Date().toISOString() 
    });
  });

  app.listen(port, () => {
    console.log(`[API] Bureau Gateway active at http://localhost:${port}`);
    console.log("-------------------------------------------\n");
  });
}

startGateway().catch(err => {
  console.error("[API] Critical failure:", err);
  process.exit(1);
});