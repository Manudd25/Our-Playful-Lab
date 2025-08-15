// static/scripts/petname.js - SUPER COOL & ATTENTION-GRABBING VERSION
(() => {
    const $ = (q) => document.querySelector(q);
    const cat = $("#category");
    const out = $("#name");
    const gen = $("#btn-generate");
    const copyBtn = $("#btn-copy");
    const meta = document.getElementById("meta");

    if (!cat || !out || !gen || !copyBtn) return;

    // COOL PARTICLE EFFECTS
    function createParticles(x, y, color) {
        for (let i = 0; i < 8; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                left: ${x}px;
                top: ${y}px;
                width: 4px;
                height: 4px;
                background: ${color};
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                animation: particleFloat 1s ease-out forwards;
            `;
            document.body.appendChild(particle);

            setTimeout(() => particle.remove(), 1000);
        }
    }

    // Add particle animation to CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleFloat {
            0% {
                transform: translate(0, 0) scale(1);
                opacity: 1;
            }
            100% {
                transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px) scale(0);
                opacity: 0;
            }
        }
        
        @keyframes nameReveal {
            0% {
                transform: scale(0.8) rotateY(90deg);
                opacity: 0;
            }
            100% {
                transform: scale(1) rotateY(0deg);
                opacity: 1;
            }
        }
        
        @keyframes buttonPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .generating {
            animation: buttonPulse 0.5s ease-in-out infinite !important;
        }
        
        .name-reveal {
            animation: nameReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
    `;
    document.head.appendChild(style);

    function updatePermalink(category, seed) {
        const url = new URL(window.location);
        category ? url.searchParams.set("category", category) : url.searchParams.delete("category");
        url.searchParams.set("seed", String(seed));
        history.replaceState(null, "", url);
    }

    // ENHANCED GENERATE FUNCTION WITH COOL EFFECTS
    async function generate() {
        try {
            // Visual feedback
            gen.disabled = true;
            gen.textContent = "✨ Generating... ✨";
            gen.classList.add('generating');

            // Add loading effect to output
            out.style.opacity = '0.5';
            out.textContent = "Summoning the perfect name...";

            // Create particles at button location
            const rect = gen.getBoundingClientRect();
            createParticles(rect.left + rect.width / 2, rect.top + rect.height / 2, '#ff0080');

            const qs = cat.value ? `?category=${encodeURIComponent(cat.value)}` : "";
            const res = await fetch(`/api/petname${qs}`, { cache: "no-store" });

            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();

            // Cool reveal effect
            out.style.opacity = '1';
            out.classList.add('name-reveal');
            out.textContent = data.name;

            // Create celebration particles
            const nameRect = out.getBoundingClientRect();
            createParticles(nameRect.left + nameRect.width / 2, nameRect.top + nameRect.height / 2, '#00ffff');

            if (meta) {
                meta.textContent = `✨ ${data.category} • seed: ${data.seed} ✨`;
                meta.style.animation = 'fadeInUp 0.5s ease-out';
            }

            updatePermalink(cat.value || "", data.seed);

            // Remove animation classes after animation completes
            setTimeout(() => {
                out.classList.remove('name-reveal');
            }, 600);

        } catch (err) {
            out.textContent = "Oops, couldn't generate a name. Try again.";
            out.style.color = '#ff6b6b';
            console.error(err);
        } finally {
            gen.disabled = false;
            gen.textContent = "Generate";
            gen.classList.remove('generating');
            out.style.color = '';
        }
    }

    // ENHANCED COPY FUNCTION
    copyBtn.addEventListener("click", async () => {
        const text = out.textContent.trim();
        if (!text || text === "Click \"Generate\" to get a name…" || text.includes("Oops")) return;

        try {
            await navigator.clipboard.writeText(text);

            // Cool copy feedback
            copyBtn.textContent = "✨ Copied! ✨";
            copyBtn.style.background = 'linear-gradient(135deg, #00ff80, #00ffff)';

            // Create success particles
            const rect = copyBtn.getBoundingClientRect();
            createParticles(rect.left + rect.width / 2, rect.top + rect.height / 2, '#00ff80');

            setTimeout(() => {
                copyBtn.textContent = "Copy";
                copyBtn.style.background = '';
            }, 1500);
        } catch (e) {
            console.error(e);
            copyBtn.textContent = "Failed";
            setTimeout(() => copyBtn.textContent = "Copy", 1000);
        }
    });

    // COOL HOVER EFFECTS
    gen.addEventListener('mouseenter', () => {
        if (!gen.disabled) {
            gen.style.transform = 'translateY(-2px) scale(1.02)';
        }
    });

    gen.addEventListener('mouseleave', () => {
        gen.style.transform = '';
    });

    // RANDOM COLOR CHANGES ON CATEGORY SELECT
    cat.addEventListener('change', () => {
        const colors = ['#ff0080', '#00ffff', '#8000ff', '#00ff80', '#ffff00', '#ff8000'];
        const randomColor = colors[Math.floor(Math.random() * colors.length)];

        // Subtle color flash effect
        out.style.transition = 'all 0.3s ease';
        out.style.borderColor = randomColor;
        out.style.boxShadow = `0 0 20px ${randomColor}40`;

        setTimeout(() => {
            out.style.borderColor = '';
            out.style.boxShadow = '';
        }, 300);
    });

    // COOL KEYBOARD SHORTCUTS
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !gen.disabled) {
            generate();
        }
        if (e.key === 'c' && (e.ctrlKey || e.metaKey)) {
            copyBtn.click();
        }
    });

    // AUTO-GENERATE WITH COOL INTRO
    setTimeout(() => {
        out.textContent = "Ready to create magic? ✨";
        setTimeout(generate, 1000);
    }, 500);

    // CLICK HANDLER
    gen.addEventListener("click", generate);

    // COOL MOUSE TRACKING EFFECT (optional)
    let mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Add subtle parallax effect to background
    document.addEventListener('mousemove', (e) => {
        const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
        const moveY = (e.clientY - window.innerHeight / 2) * 0.01;

        document.body.style.setProperty('--mouse-x', moveX + 'px');
        document.body.style.setProperty('--mouse-y', moveY + 'px');
    });

})();
