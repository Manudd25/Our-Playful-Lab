(function () {
    // --- Nav (hamburger) ---
    const nav = document.querySelector("nav");
    const btn = document.getElementById("nav-toggle");
    const menu = document.getElementById("nav-menu");

    if (nav && btn && menu) {
        const setOpen = (open) => {
            nav.dataset.open = open ? "true" : "false";
            btn.setAttribute("aria-expanded", String(open));
            btn.classList.toggle("is-open", open);
        };
        const toggle = () => setOpen(nav.dataset.open !== "true");
        const close = () => setOpen(false);

        btn.addEventListener("click", toggle);
        menu.addEventListener("click", (e) => {
            if (e.target.closest("a")) close();           // <— more robust
        });
        document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
        document.addEventListener("click", (e) => { if (!nav.contains(e.target)) close(); });

        // Close the panel when resizing up to desktop
        const mq = window.matchMedia("(min-width: 901px)");
        if (mq.addEventListener) {
            mq.addEventListener("change", (e) => { if (e.matches) close(); });
        } else if (mq.addListener) {
            mq.addListener((e) => { if (e.matches) close(); }); // old Safari
        }
    }

    // --- Sparkles: back to top ---
    const deco = document.querySelector(".footer-decoration");
    if (deco) {
        // a11y: make it act like a button
        deco.setAttribute("role", "button");
        deco.setAttribute("aria-label", "Back to top");
        deco.tabIndex = 0;

        const toTop = () => window.scrollTo({ top: 0, behavior: "smooth" });
        deco.addEventListener("click", toTop);
        deco.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toTop(); }
        });
    }
})();

(function () {
    const modal = document.getElementById('hire-modal');
    const open = document.getElementById('open-hire');
    const close = document.getElementById('hire-close');
    const overlay = document.getElementById('hire-overlay');

    function show() { modal.setAttribute('aria-hidden', 'false'); }
    function hide() { modal.setAttribute('aria-hidden', 'true'); }

    open?.addEventListener('click', (e) => { e.preventDefault(); show(); });
    close?.addEventListener('click', hide);
    overlay?.addEventListener('click', hide);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') hide(); });
})();