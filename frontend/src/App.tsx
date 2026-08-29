function App() {
  return (
    <main className="app-shell">
      <section className="hero-card">
        <p className="eyebrow">School Website</p>
        <h1>Welcome to the future school portal</h1>
        <p className="subtitle">
          This is the initial scaffold for a public-facing school website.
          Business features and authentication are intentionally not implemented yet.
        </p>
        <div className="status-grid">
          <div>
            <span>Frontend</span>
            <strong>React + TypeScript + Vite</strong>
          </div>
          <div>
            <span>Backend</span>
            <strong>FastAPI + PostgreSQL</strong>
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;
