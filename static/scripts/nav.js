// static/scripts/nav.js
(function () {
    const nav = document.querySelector("nav");
    const btn = document.getElementById("nav-toggle");
    const menu = document.getElementById("nav-menu");
    if (!nav || !btn || !menu) return;

    function setOpen(open) {
        nav.dataset.open = open ? "true" : "false";
        btn.setAttribute("aria-expanded", String(open));
        btn.classList.toggle("is-open", open);
    }
    function toggle() { setOpen(nav.dataset.open !== "true"); }
    function close() { setOpen(false); }

    btn.addEventListener("click", toggle);
    menu.addEventListener("click", (e) => { if (e.target.matches("a")) close(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
    document.addEventListener("click", (e) => { if (!nav.contains(e.target)) close(); });

    // optional: if the user resizes to desktop, ensure the panel is closed
    const mq = window.matchMedia("(min-width: 901px)");
    mq.addEventListener?.("change", () => { if (mq.matches) close(); });
})();
