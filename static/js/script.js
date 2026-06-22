/**
 * Onion Techs — Global Frontend Controller
 * Handles: AOS, navbar scroll shrink, counter animation, typing effect, scroll reveals
 */

document.addEventListener('DOMContentLoaded', () => {

    /* =====================================================
       1. AOS (Animate on Scroll) — initialize
    ===================================================== */
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 750,
            once: true,
            easing: 'ease-out-cubic',
            offset: 60
        });
    }

    /* =====================================================
       2. Navbar Scroll Shrink Effect
    ===================================================== */
    const navbar = document.querySelector('nav');
    if (navbar) {
        const handleNavScroll = () => {
            if (window.scrollY > 60) {
                navbar.classList.add('top-2', 'shadow-2xl', 'bg-[#070B34]/98', 'border-purple-500/30');
                navbar.classList.remove('top-4', 'bg-[#070B34]/85', 'border-purple-500/20');
            } else {
                navbar.classList.add('top-4', 'bg-[#070B34]/85', 'border-purple-500/20');
                navbar.classList.remove('top-2', 'shadow-2xl', 'bg-[#070B34]/98', 'border-purple-500/30');
            }
        };
        window.addEventListener('scroll', handleNavScroll, { passive: true });
    }

    /* =====================================================
       3. Counter Animate-up on Scroll
    ===================================================== */
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const el     = entry.target;
                const target = Number(el.dataset.target || 0);
                const suffix = el.dataset.suffix || (target >= 10 ? '+' : '');
                const start  = performance.now();
                const dur    = 2000;

                const tick = (now) => {
                    const prog = Math.min((now - start) / dur, 1);
                    const ease = 1 - Math.pow(1 - prog, 3); // ease-out cubic
                    el.textContent = Math.floor(ease * target) + (prog < 1 ? '' : suffix);
                    if (prog < 1) requestAnimationFrame(tick);
                };

                requestAnimationFrame(tick);
                observer.unobserve(el);
            });
        }, { threshold: 0.2 });

        counters.forEach(c => observer.observe(c));
    }

    /* =====================================================
       4. Hero Typing Effect (if element exists)
    ===================================================== */
    const typingEl = document.getElementById('typing-text');
    if (typingEl) {
        const words   = ['Technology', 'Innovation', 'AI Solutions', 'Custom Software', 'The Future'];
        let wIdx      = 0;
        let cIdx      = 0;
        let deleting  = false;
        let speed     = 110;

        const type = () => {
            const word = words[wIdx];
            if (deleting) {
                cIdx--;
                speed = 55;
            } else {
                cIdx++;
                speed = 120;
            }
            typingEl.textContent = word.substring(0, cIdx);

            if (!deleting && cIdx === word.length) {
                deleting = true;
                speed = 2200;
            } else if (deleting && cIdx === 0) {
                deleting = false;
                wIdx = (wIdx + 1) % words.length;
                speed = 500;
            }
            setTimeout(type, speed);
        };
        type();
    }

    /* =====================================================
       5. Generic .reveal scroll-in animation
    ===================================================== */
    const reveals = document.querySelectorAll('.reveal');
    if (reveals.length > 0) {
        const revealObs = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('active');
                    revealObs.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });
        reveals.forEach(el => revealObs.observe(el));
    }

});
