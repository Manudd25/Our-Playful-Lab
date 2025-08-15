// Excuse Generator script (neon, resilient)

const $ = (q) => document.querySelector(q);
const categoryEl = $("#category");
const excuseEl = $("#excuse");
const metaEl = $("#meta");
const btnGen = $("#btn-generate");
const btnCopy = $("#btn-copy");
const btnSave = $("#btn-save");
const btnLink = $("#btn-link");
const btnShare = $("#btn-share");
const btnClear = $("#btn-clear");
const favList = $("#favorites");

// ---- CONFIG: adjust endpoints here ----
const API_EXCUSE = "/excuse";          // if your backend is '/api/excuse', change this to '/api/excuse'
//const API_CATS = null;               // set to '/api/categories' ONLY if you implement it
const API_CATS = "/api/categories";

const LS_KEY = "excuse_favorites_v1";
const MAX_FAVS = 20;

async function getJSON(url) {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

async function loadCategories() {
    if (!categoryEl || !API_CATS) return;           // keep existing options if no API
    try {
        const data = await getJSON(API_CATS);
        const list = data.categories || [];
        const have = new Set([...categoryEl.options].map(o => o.value));
        for (const c of list) {
            if (have.has(c)) continue;
            const opt = document.createElement("option");
            opt.value = c;
            opt.textContent = c[0].toUpperCase() + c.slice(1);
            categoryEl.appendChild(opt);
        }
    } catch (e) {
        console.warn("Categories API unavailable — keeping existing options.", e);
    }
}

function parseQuery() {
    const u = new URL(window.location);
    return { category: u.searchParams.get("category") || "", seed: u.searchParams.get("seed") };
}

function updatePermalink(category, seed) {
    const u = new URL(window.location);
    category ? u.searchParams.set("category", category) : u.searchParams.delete("category");
    u.searchParams.set("seed", String(seed));
    history.replaceState(null, "", u);
    return u.toString();
}

async function fetchExcuse({ category = "", seed = null } = {}) {
    const qs = new URLSearchParams();
    if (category) qs.set("category", category);
    if (seed !== null && seed !== undefined) qs.set("seed", String(seed));
    const url = `${API_EXCUSE}${qs.toString() ? "?" + qs.toString() : ""}`;
    const data = await getJSON(url);

    const text = data.excuse || data.text || "(no excuse)";
    const used = data.category || category || "";
    const usedSeed = data.seed || Date.now();

    excuseEl && (excuseEl.textContent = text);
    if (metaEl) {
        metaEl.textContent = `category: ${used || "random"} • seed: ${usedSeed}`;
        metaEl.style.display = "block";
    }
    updatePermalink(used, usedSeed);
}

async function onGenerate() {
    const cat = categoryEl?.value || "";
    await fetchExcuse({ category: cat || "" }); // server picks a seed
}

async function copyText(text) {
    try { await navigator.clipboard.writeText(text); return true; }
    catch {
        const ta = Object.assign(document.createElement("textarea"), { value: text });
        document.body.appendChild(ta); ta.select();
        const ok = document.execCommand("copy"); ta.remove(); return ok;
    }
}

// ---- Events (guarded) ----
btnGen?.addEventListener("click", onGenerate);

btnCopy?.addEventListener("click", async () => {
    const text = excuseEl?.textContent?.trim(); if (!text) return;
    if (await copyText(text)) { btnCopy.textContent = "Copied!"; setTimeout(() => btnCopy.textContent = "Copy", 900); }
});

btnLink?.addEventListener("click", async () => {
    const link = window.location.toString();
    if (await copyText(link)) { btnLink.textContent = "Link copied!"; setTimeout(() => btnLink.textContent = "Permalink", 900); }
});

btnShare?.addEventListener("click", async () => {
    const url = window.location.toString(), text = excuseEl?.textContent?.trim() || "";
    if (navigator.share) { try { await navigator.share({ title: "Excuse Generator", text, url }); } catch { } }
    else if (await copyText(url)) { btnShare.textContent = "URL copied!"; setTimeout(() => btnShare.textContent = "Share", 900); }
});

// ---- Favorites ----
function getFavs() { try { return JSON.parse(localStorage.getItem(LS_KEY)) || []; } catch { return []; } }
function setFavs(arr) { localStorage.setItem(LS_KEY, JSON.stringify(arr.slice(0, MAX_FAVS))); }
function renderFavs() {
    if (!favList) return;
    const favs = getFavs(); favList.innerHTML = "";
    if (!favs.length) {
        const li = document.createElement("li");
        li.className = "eg-note"; li.textContent = "No favorites yet."; favList.appendChild(li); return;
    }
    favs.forEach(f => {
        const li = document.createElement("li");
        li.className = "eg-fav-item";
        li.dataset.seed = String(f.seed);
        li.dataset.category = f.category || "";
        li.innerHTML = `
      <div class="eg-fav-row">
        <span class="eg-meta tiny">cat: ${f.category || "random"} • seed: ${f.seed}</span>
        <span class="eg-fav-actions">
          <button data-act="copy">Copy</button>
          <button data-act="open">Open</button>
          <button data-act="del">Delete</button>
        </span>
      </div>
      <div class="eg-fav-text">${f.text}</div>
    `;
        favList.appendChild(li);
    });
}

btnSave?.addEventListener("click", () => {
    const text = excuseEl?.textContent?.trim(); if (!text) return;
    const { category, seed } = parseQuery(); if (!seed) return;
    const favs = getFavs();
    if (!favs.some(f => String(f.seed) === String(seed) && (f.category || "") === (category || ""))) {
        favs.unshift({ text, category: category || "", seed }); setFavs(favs); renderFavs();
        btnSave.textContent = "Saved!"; setTimeout(() => btnSave.textContent = "Save", 900);
    }
});

favList?.addEventListener("click", async (e) => {
    const button = e.target.closest("button"); if (!button) return;
    const li = e.target.closest(".eg-fav-item");
    const seed = li?.dataset.seed; const category = li?.dataset.category || "";
    const act = button.dataset.act;
    if (act === "copy") { const t = li.querySelector(".eg-fav-text")?.textContent?.trim() || ""; await copyText(t); }
    if (act === "open") { await fetchExcuse({ category, seed }); window.scrollTo({ top: 0, behavior: "smooth" }); }
    if (act === "del") { const favs = getFavs().filter(f => !(String(f.seed) === String(seed) && (f.category || "") === category)); setFavs(favs); renderFavs(); }
});

btnClear?.addEventListener("click", () => { localStorage.removeItem(LS_KEY); renderFavs(); });

// ---- Init ----
(async function init() {
    await loadCategories();
    const { category, seed } = parseQuery();
    if (categoryEl && category) categoryEl.value = category;
    await fetchExcuse({ category: category || "", seed: seed || null });
    renderFavs();
})();
