import { useState, useEffect } from "react";

interface Category {
  label: string;
  color: string;
  icon: string;
}

interface Entry {
  id: number;
  date: string;
  category: string;
  activity: string;
  output: string;
  notes: string;
}

type View = "list" | "add" | "stats";

const CATEGORIES: Category[] = [
  { label: "Commerciale", color: "#f59e0b", icon: "◆" },
  { label: "Tecnico", color: "#3b82f6", icon: "◉" },
  { label: "Marketing", color: "#10b981", icon: "▲" },
  { label: "Admin", color: "#8b5cf6", icon: "■" },
  { label: "Altro", color: "#6b7280", icon: "●" },
];

const OUTPUTS: string[] = [
  "Cliente contattato",
  "Demo effettuata",
  "Preventivo inviato",
  "Incontro organizzato",
  "Problema risolto",
  "Materiale creato",
  "Installazione seguita",
  "Altro",
];

const formatDate = (iso: string): string => {
  const d = new Date(iso);
  return d.toLocaleDateString("it-IT", { day: "2-digit", month: "short", year: "numeric" });
};

export default function BeecomsTracker() {
  const [entries, setEntries] = useState<Entry[]>(() => {
    try {
      return JSON.parse(localStorage.getItem("beecoms_entries") || "[]") as Entry[];
    } catch {
      return [];
    }
  });

  const [form, setForm] = useState({
    date: new Date().toISOString().split("T")[0],
    category: "Commerciale",
    activity: "",
    output: "Cliente contattato",
    notes: "",
  });

  const [view, setView] = useState<View>("list");

  useEffect(() => {
    localStorage.setItem("beecoms_entries", JSON.stringify(entries));
  }, [entries]);

  const handleAdd = () => {
    if (!form.activity.trim()) return;
    const entry: Entry = { ...form, id: Date.now() };
    setEntries([entry, ...entries]);
    setForm({ ...form, activity: "", notes: "" });
    setView("list");
  };

  const handleDelete = (id: number) => {
    setEntries(entries.filter((e) => e.id !== id));
  };

  const getCategoryColor = (label: string) =>
    CATEGORIES.find((c) => c.label === label)?.color ?? "#6b7280";
  const getCategoryIcon = (label: string) =>
    CATEGORIES.find((c) => c.label === label)?.icon ?? "●";

  const stats = CATEGORIES.map((cat) => ({
    ...cat,
    count: entries.filter((e) => e.category === cat.label).length,
  })).filter((c) => c.count > 0);

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0a",
      color: "#f5f5f5",
      fontFamily: "'DM Mono', 'Courier New', monospace",
      maxWidth: 480,
      margin: "0 auto",
      position: "relative",
    }}>
      {/* Header */}
      <div style={{
        padding: "28px 20px 16px",
        borderBottom: "1px solid #1f1f1f",
        position: "sticky",
        top: 0,
        background: "#0a0a0a",
        zIndex: 10,
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <div style={{ fontSize: 10, letterSpacing: 4, color: "#f59e0b", marginBottom: 4, textTransform: "uppercase" }}>
              BeeComs
            </div>
            <div style={{ fontSize: 22, fontWeight: 700, letterSpacing: -1 }}>
              Attività
            </div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 10, color: "#555", letterSpacing: 2, textTransform: "uppercase" }}>Totale</div>
            <div style={{ fontSize: 28, fontWeight: 700, color: "#f59e0b" }}>{entries.length}</div>
          </div>
        </div>

        {/* Nav */}
        <div style={{ display: "flex", gap: 8, marginTop: 16 }}>
          {(["list", "add", "stats"] as View[]).map((v) => (
            <button key={v} onClick={() => setView(v)} style={{
              flex: 1,
              padding: "8px 0",
              background: view === v ? "#f59e0b" : "#111",
              color: view === v ? "#0a0a0a" : "#888",
              border: "1px solid " + (view === v ? "#f59e0b" : "#222"),
              borderRadius: 6,
              fontSize: 11,
              letterSpacing: 2,
              textTransform: "uppercase",
              cursor: "pointer",
              fontFamily: "inherit",
              fontWeight: view === v ? 700 : 400,
              transition: "all 0.15s",
            }}>
              {v === "list" ? "Lista" : v === "add" ? "+ Aggiungi" : "Stats"}
            </button>
          ))}
        </div>
      </div>

      {/* LIST VIEW */}
      {view === "list" && (
        <div style={{ padding: "12px 20px" }}>
          {entries.length === 0 ? (
            <div style={{ textAlign: "center", padding: "60px 20px", color: "#333" }}>
              <div style={{ fontSize: 32, marginBottom: 12 }}>◉</div>
              <div style={{ fontSize: 13, letterSpacing: 1 }}>Nessuna attività ancora</div>
              <div style={{ fontSize: 11, color: "#2a2a2a", marginTop: 8 }}>Premi + Aggiungi per iniziare</div>
            </div>
          ) : entries.map((e) => (
            <div key={e.id} style={{
              marginBottom: 10,
              padding: "14px 16px",
              background: "#111",
              borderRadius: 10,
              borderLeft: `3px solid ${getCategoryColor(e.category)}`,
              position: "relative",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 6 }}>
                    <span style={{ fontSize: 10, color: getCategoryColor(e.category), letterSpacing: 1, textTransform: "uppercase" }}>
                      {getCategoryIcon(e.category)} {e.category}
                    </span>
                    <span style={{ fontSize: 10, color: "#444" }}>·</span>
                    <span style={{ fontSize: 10, color: "#444" }}>{formatDate(e.date)}</span>
                  </div>
                  <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4, lineHeight: 1.3 }}>{e.activity}</div>
                  <div style={{
                    display: "inline-block",
                    fontSize: 10,
                    color: "#888",
                    background: "#1a1a1a",
                    padding: "2px 8px",
                    borderRadius: 20,
                    letterSpacing: 0.5,
                  }}>{e.output}</div>
                  {e.notes && (
                    <div style={{ fontSize: 12, color: "#555", marginTop: 6, fontStyle: "italic" }}>{e.notes}</div>
                  )}
                </div>
                <button onClick={() => handleDelete(e.id)} style={{
                  background: "none",
                  border: "none",
                  color: "#333",
                  cursor: "pointer",
                  fontSize: 16,
                  padding: "0 0 0 12px",
                  lineHeight: 1,
                }}>×</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ADD VIEW */}
      {view === "add" && (
        <div style={{ padding: "20px" }}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 10, letterSpacing: 2, color: "#555", textTransform: "uppercase", display: "block", marginBottom: 6 }}>
              Data
            </label>
            <input
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              style={{
                width: "100%",
                background: "#111",
                border: "1px solid #222",
                borderRadius: 8,
                padding: "12px 14px",
                color: "#f5f5f5",
                fontFamily: "inherit",
                fontSize: 14,
                boxSizing: "border-box",
              }}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 10, letterSpacing: 2, color: "#555", textTransform: "uppercase", display: "block", marginBottom: 6 }}>
              Categoria
            </label>
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
              {CATEGORIES.map((cat) => (
                <button key={cat.label} onClick={() => setForm({ ...form, category: cat.label })} style={{
                  padding: "8px 14px",
                  background: form.category === cat.label ? cat.color : "#111",
                  color: form.category === cat.label ? "#0a0a0a" : "#666",
                  border: "1px solid " + (form.category === cat.label ? cat.color : "#222"),
                  borderRadius: 20,
                  fontSize: 11,
                  cursor: "pointer",
                  fontFamily: "inherit",
                  fontWeight: form.category === cat.label ? 700 : 400,
                  transition: "all 0.15s",
                }}>
                  {cat.icon} {cat.label}
                </button>
              ))}
            </div>
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 10, letterSpacing: 2, color: "#555", textTransform: "uppercase", display: "block", marginBottom: 6 }}>
              Attività *
            </label>
            <input
              type="text"
              placeholder="Es: Demo con Logistica Rossi SpA"
              value={form.activity}
              onChange={(e) => setForm({ ...form, activity: e.target.value })}
              style={{
                width: "100%",
                background: "#111",
                border: "1px solid #222",
                borderRadius: 8,
                padding: "12px 14px",
                color: "#f5f5f5",
                fontFamily: "inherit",
                fontSize: 14,
                boxSizing: "border-box",
              }}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 10, letterSpacing: 2, color: "#555", textTransform: "uppercase", display: "block", marginBottom: 6 }}>
              Output
            </label>
            <select
              value={form.output}
              onChange={(e) => setForm({ ...form, output: e.target.value })}
              style={{
                width: "100%",
                background: "#111",
                border: "1px solid #222",
                borderRadius: 8,
                padding: "12px 14px",
                color: "#f5f5f5",
                fontFamily: "inherit",
                fontSize: 14,
                boxSizing: "border-box",
                appearance: "none",
              }}
            >
              {OUTPUTS.map((o) => <option key={o} value={o}>{o}</option>)}
            </select>
          </div>

          <div style={{ marginBottom: 24 }}>
            <label style={{ fontSize: 10, letterSpacing: 2, color: "#555", textTransform: "uppercase", display: "block", marginBottom: 6 }}>
              Note (opzionale)
            </label>
            <textarea
              placeholder="Contesto, followup, dettagli..."
              value={form.notes}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
              rows={3}
              style={{
                width: "100%",
                background: "#111",
                border: "1px solid #222",
                borderRadius: 8,
                padding: "12px 14px",
                color: "#f5f5f5",
                fontFamily: "inherit",
                fontSize: 14,
                boxSizing: "border-box",
                resize: "none",
              }}
            />
          </div>

          <button onClick={handleAdd} style={{
            width: "100%",
            padding: "16px",
            background: form.activity.trim() ? "#f59e0b" : "#1a1a1a",
            color: form.activity.trim() ? "#0a0a0a" : "#333",
            border: "none",
            borderRadius: 10,
            fontSize: 13,
            fontWeight: 700,
            letterSpacing: 2,
            textTransform: "uppercase",
            cursor: form.activity.trim() ? "pointer" : "default",
            fontFamily: "inherit",
            transition: "all 0.15s",
          }}>
            Salva Attività
          </button>
        </div>
      )}

      {/* STATS VIEW */}
      {view === "stats" && (
        <div style={{ padding: "20px" }}>
          {entries.length === 0 ? (
            <div style={{ textAlign: "center", padding: "60px 20px", color: "#333", fontSize: 13 }}>
              Nessun dato ancora
            </div>
          ) : (
            <>
              <div style={{ marginBottom: 24 }}>
                <div style={{ fontSize: 10, letterSpacing: 3, color: "#555", textTransform: "uppercase", marginBottom: 14 }}>
                  Per categoria
                </div>
                {stats.map((cat) => (
                  <div key={cat.label} style={{ marginBottom: 12 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                      <span style={{ fontSize: 12, color: cat.color }}>{cat.icon} {cat.label}</span>
                      <span style={{ fontSize: 12, color: "#888" }}>{cat.count} attività</span>
                    </div>
                    <div style={{ height: 4, background: "#111", borderRadius: 2 }}>
                      <div style={{
                        height: "100%",
                        width: `${(cat.count / entries.length) * 100}%`,
                        background: cat.color,
                        borderRadius: 2,
                        transition: "width 0.4s",
                      }} />
                    </div>
                  </div>
                ))}
              </div>

              <div style={{ marginBottom: 24 }}>
                <div style={{ fontSize: 10, letterSpacing: 3, color: "#555", textTransform: "uppercase", marginBottom: 14 }}>
                  Per output
                </div>
                {OUTPUTS.map((o) => {
                  const count = entries.filter((e) => e.output === o).length;
                  if (!count) return null;
                  return (
                    <div key={o} style={{
                      display: "flex",
                      justifyContent: "space-between",
                      padding: "10px 0",
                      borderBottom: "1px solid #151515",
                      fontSize: 13,
                    }}>
                      <span style={{ color: "#888" }}>{o}</span>
                      <span style={{ color: "#f59e0b", fontWeight: 700 }}>{count}</span>
                    </div>
                  );
                })}
              </div>

              <div style={{
                padding: "16px",
                background: "#111",
                borderRadius: 10,
                border: "1px solid #1f1f1f",
              }}>
                <div style={{ fontSize: 10, letterSpacing: 2, color: "#555", textTransform: "uppercase", marginBottom: 10 }}>
                  Prima attività registrata
                </div>
                <div style={{ fontSize: 13, color: "#888" }}>
                  {entries.length > 0 ? formatDate(entries[entries.length - 1].date) : "—"}
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
