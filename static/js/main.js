const $ = (q) => document.querySelector(q);
const categoryEl = $("#category");
const excuseEl = $("#excuse");
const metaEl = $("#meta");
const btnGenerate = $("#btn-generate");
const btnCopy = $("#btn-copy");
const btnSave = $("#btn-save");
const btnLink = $("#btn-link");
const btnShare = $("#btn-share");
const btnClear = $("#btn-clear");
const favList = $("#favorites");

const LS_KEY = "excuse_favorites_v1";
const MAX_FAVS = 20;

async function getJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

async function loadCategories() {
    try {
        const data = await getJSON("/api/categories");
        for (const c of data.categories) {
            const opt = document.createElement("option");
            opt.value = c;
            opt.textContent = c[0].toUpperCase() + c.slice(1);
            categoryEl.appendChild(opt);
        }
    } catch (e) {
        console.error("Failed to load categories:", e);
    }
}

function parseQuery() {
    const u = new URL(window.location);
    return {
        category: u.searchParams.get("category") || "",
        seed: u.searchParams.get("seed"),
    };
}

function updatePermalink(category, seed) {
    const u = new URL(window.location);
    u.searchParams.set("category", category || "");
    u.searchParams.set("seed", String(seed));
    history.replaceState(null, "", u);
    return u.toString();
}

async function fetchExcuse({ category = "", seed = null } = {}) {
    const qs = new URLSearchParams();
    if (category) qs.set("category", category);
    if (seed !== null && seed !== undefined) qs.set("seed", String(seed));
    const { excuse, category: used, seed: usedSeed } = await getJSON(`/api/excuse?${qs.toString()}`);
    excuseEl.textContent = excuse;
    const link = updatePermalink(used, usedSeed);
    metaEl.textContent = `category: ${used} • `;
    return link;
}

async function onGenerate() {
    const cat = categoryEl.value;
    await fetchExcuse({ category: cat || "" }); // server creates a fresh seed
}

async function copyText(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch {
        const ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        const ok = document.execCommand("copy");
        ta.remove();
        return ok;
    }
}

btnGenerate.addEventListener("click", onGenerate);

btnCopy.addEventListener("click", async () => {
    const text = excuseEl.textContent.trim();
    if (!text) return;
    if (await copyText(text)) {
        btnCopy.textContent = "Copied!";
        setTimeout(() => (btnCopy.textContent = "Copy"), 900);
    }
});

btnLink.addEventListener("click", async () => {
    const link = window.location.toString();
    if (await copyText(link)) {
        btnLink.textContent = "Link copied!";
        setTimeout(() => (btnLink.textContent = "Permalink"), 900);
    }
});

btnShare.addEventListener("click", async () => {
    const url = window.location.toString();
    const text = excuseEl.textContent.trim();
    if (navigator.share) {
        try {
            await navigator.share({ title: "Excuse Generator", text, url });
        } catch { /* user cancelled */ }
    } else {
        if (await copyText(url)) {
            btnShare.textContent = "URL copied!";
            setTimeout(() => (btnShare.textContent = "Share"), 900);
        }
    }
});

function getFavs() {
    try { return JSON.parse(localStorage.getItem(LS_KEY)) || []; }
    catch { return []; }
}
function setFavs(arr) { localStorage.setItem(LS_KEY, JSON.stringify(arr.slice(0, MAX_FAVS))); }

function renderFavs() {
    const favs = getFavs();
    favList.innerHTML = "";
    if (!favs.length) {
        const li = document.createElement("li");
        li.className = "muted tiny";
        li.textContent = "No favorites yet.";
        favList.appendChild(li);
        return;
    }
    for (const f of favs) {
        const li = document.createElement("li");
        li.className = "fav-item";
        li.innerHTML = `
      <div class="fav-row">
        <span class="tiny muted">cat: ${f.category} • </span>
        <span class="fav-actions-inline">
          <button data-act="copy">Copy</button>
          <button data-act="open">Open</button>
          <button data-act="del">Delete</button>
        </span>
      </div>
      <div class="tiny" style="margin-top:.4rem">${f.text}</div>
    `;
        li.dataset.seed = String(f.seed);
        li.dataset.category = f.category;
        favList.appendChild(li);
    }
}

btnSave.addEventListener("click", () => {
    const text = excuseEl.textContent.trim();
    if (!text) return;
    const { category, seed } = parseQuery();
    if (!seed) return; // only save if we have a permalink seed
    const favs = getFavs();
    // de-dupe by seed+category
    if (!favs.some(f => String(f.seed) === String(seed) && f.category === category)) {
        favs.unshift({ text, category, seed });
        setFavs(favs);
        renderFavs();
        btnSave.textContent = "Saved!";
        setTimeout(() => (btnSave.textContent = "Save"), 900);
    }
});

favList.addEventListener("click", async (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    const li = e.target.closest(".fav-item");
    const seed = li?.dataset.seed;
    const category = li?.dataset.category || "";
    const act = btn.dataset.act;

    if (act === "copy") {
        const text = li.querySelector("div.tiny:nth-of-type(2)")?.textContent?.trim() || "";
        await copyText(text);
    }
    if (act === "open") {
        await fetchExcuse({ category, seed });
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (act === "del") {
        const favs = getFavs().filter(f => !(String(f.seed) === String(seed) && f.category === category));
        setFavs(favs);
        renderFavs();
    }
});

btnClear.addEventListener("click", () => {
    localStorage.removeItem(LS_KEY);
    renderFavs();
});

// init
(async function init() {
    await loadCategories();
    const { category, seed } = parseQuery();
    if (category) categoryEl.value = category;
    if (seed) {
        await fetchExcuse({ category, seed });
    }
    renderFavs();
})();

metaEl.textContent = ""; 
