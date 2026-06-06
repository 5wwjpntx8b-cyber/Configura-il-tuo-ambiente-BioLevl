import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import BeecomsTracker from "./BeecomsTracker";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BeecomsTracker />
  </StrictMode>
);
