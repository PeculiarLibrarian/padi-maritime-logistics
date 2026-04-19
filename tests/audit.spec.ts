import { test, expect } from "@playwright/test";
import { runSteps } from "passmark";

test("PADI Bureau: Deterministic Logic Test", async ({ page }) => {
  // AI-driven steps require more time
  test.setTimeout(90_000);

  await runSteps({
    page,
    userFlow: "Audit the PADI N-1-NODE Validator",
    steps: [
      { description: "Navigate to https://padi-sovereign.streamlit.app/" },
      { description: "Type 'NB-01-NODE' into the Vessel ID field" },
      { description: "Click the Run Handshake button" },
    ],
    assertions: [
      { assertion: "The message 'HANDSHAKE SUCCESSFUL' is visible" },
      { assertion: "The JSON data for 'Nairobi Pioneer' is displayed" },
    ],
    test,
    expect,
  });
});
