/**
 * Onion Techs - Frontend TypeScript Controller
 */

// Types & Interfaces
interface Testimonial {
    quote: string;
    author: string;
    role: string;
    rating: number;
}

class OnionApp {
    private mobileOpenBtn: HTMLElement | null = null;
    private mobileCloseBtn: HTMLElement | null = null;
    private mobileOverlay: HTMLElement | null = null;
    private mobileDrawer: HTMLElement | null = null;
    private navbar: HTMLElement | null = null;
    private typingElement: HTMLElement | null = null;
    private testimonialContainer: HTMLElement | null = null;
    private testimonials: Testimonial[] = [];
    private currentTestimonialIndex = 0;
    private testimonialInterval: number | null = null;

    constructor() {
        document.addEventListener("DOMContentLoaded", () => this.init());
    }

    private init(): void {
        console.log("OnionApp Initialized");
        this.cacheElements();
        this.setupMobileMenu();
        this.setupNavbarScroll();
        this.setupCounters();
        this.setupAOS();
        this.setupTypingEffect();
        this.setupTestimonialSlider();
        this.setupScrollAnimations();
    }

    private cacheElements(): void {
        this.mobileOpenBtn = document.getElementById("mobile-menu-open");
        this.mobileCloseBtn = document.getElementById("mobile-menu-close");
        this.mobileOverlay = document.getElementById("mobile-menu-overlay");
        this.mobileDrawer = document.getElementById("mobile-menu-drawer");
        this.navbar = document.querySelector("nav");
        this.typingElement = document.getElementById("typing-text");
        this.testimonialContainer = document.getElementById("testimonial-slider-container");
    }

    /**
     * Mobile Menu Slide-in Drawer Animations
     */
    private setupMobileMenu(): void {
        if (!this.mobileOpenBtn || !this.mobileDrawer || !this.mobileOverlay) return;

        const openMenu = () => {
            // Show Overlay
            this.mobileOverlay!.classList.remove("hidden");
            // Force layout reflow
            void this.mobileOverlay!.offsetWidth;
            this.mobileOverlay!.classList.remove("opacity-0");
            this.mobileOverlay!.classList.add("opacity-100");

            // Slide in Drawer
            this.mobileDrawer!.classList.remove("translate-x-full");
            this.mobileDrawer!.classList.add("translate-x-0");

            // Prevent body scroll
            document.body.style.overflow = "hidden";
        };

        const closeMenu = () => {
            // Hide Overlay
            this.mobileOverlay!.classList.remove("opacity-100");
            this.mobileOverlay!.classList.add("opacity-0");

            // Slide out Drawer
            this.mobileDrawer!.classList.remove("translate-x-0");
            this.mobileDrawer!.classList.add("translate-x-full");

            // Allow body scroll
            document.body.style.overflow = "";

            // Hide overlay element fully after transition
            setTimeout(() => {
                this.mobileOverlay!.classList.add("hidden");
            }, 300);
        };

        this.mobileOpenBtn.addEventListener("click", openMenu);
        
        if (this.mobileCloseBtn) {
            this.mobileCloseBtn.addEventListener("click", closeMenu);
        }

        // Close on clicking backdrop overlay
        this.mobileOverlay.addEventListener("click", closeMenu);

        // Close mobile menu on clicking any links inside it
        const links = this.mobileDrawer.querySelectorAll("a");
        links.forEach(link => {
            link.addEventListener("click", closeMenu);
        });
    }

    /**
     * Dynamic Navbar Styling on Scroll (reduces padding, adds backdrop accent)
     */
    private setupNavbarScroll(): void {
        if (!this.navbar) return;

        window.addEventListener("scroll", () => {
            if (window.scrollY > 50) {
                this.navbar!.classList.add("top-2", "w-[96%]", "shadow-2xl", "bg-[#070B34]/95", "border-purple-500/30");
                this.navbar!.classList.remove("top-4", "w-[92%]", "bg-[#070B34]/85", "border-purple-500/20");
            } else {
                this.navbar!.classList.add("top-4", "w-[92%]", "bg-[#070B34]/85", "border-purple-500/20");
                this.navbar!.classList.remove("top-2", "w-[96%]", "shadow-2xl", "bg-[#070B34]/95", "border-purple-500/30");
            }
        });
    }

    /**
     * Statistics Counter Count-up Animation using IntersectionObserver
     */
    private setupCounters(): void {
        const counters = document.querySelectorAll(".counter");
        if (counters.length === 0) return;

        const observerOptions = {
            threshold: 0.1,
            rootMargin: "0px"
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target as HTMLElement;
                    const target = Number(counter.dataset.target || 0);
                    let current = 0;
                    const duration = 2000; // 2 seconds animation duration
                    const startTime = performance.now();

                    const updateCounter = (currentTime: number) => {
                        const elapsedTime = currentTime - startTime;
                        const progress = Math.min(elapsedTime / duration, 1);
                        
                        // Ease-out quad function for smooth deceleration
                        const easeProgress = progress * (2 - progress);
                        counter.textContent = Math.floor(easeProgress * target).toString();

                        if (progress < 1) {
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.textContent = target.toString() + (target > 50 ? "+" : "");
                        }
                    };

                    requestAnimationFrame(updateCounter);
                    observer.unobserve(counter);
                }
            });
        }, observerOptions);

        counters.forEach(counter => observer.observe(counter));
    }

    /**
     * AOS Initializer
     */
    private setupAOS(): void {
        // @ts-ignore
        if (typeof AOS !== "undefined") {
            // @ts-ignore
            AOS.init({
                duration: 800,
                once: true,
                easing: "ease-out-quad"
            });
        }
    }

    /**
     * Typing animation effect for Hero section title
     */
    private setupTypingEffect(): void {
        if (!this.typingElement) return;

        const words: string[] = ["Technology", "Innovation", "Custom Software", "Expert Engineers", "AI Solutions"];
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;

        const type = () => {
            const currentWord = words[wordIndex];
            if (isDeleting) {
                charIndex--;
                typingSpeed = 50;
            } else {
                charIndex++;
                typingSpeed = 120;
            }

            this.typingElement!.textContent = currentWord.substring(0, charIndex);

            if (!isDeleting && charIndex === currentWord.length) {
                // Pause at complete word
                isDeleting = true;
                typingSpeed = 2000;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typingSpeed = 500;
            }

            setTimeout(type, typingSpeed);
        };

        type();
    }

    /**
     * Testimonial Carousel Auto-playing slider
     */
    private setupTestimonialSlider(): void {
        this.testimonials = [
            {
                quote: "Onion Techs delivered our custom telehealth platform connectdoc.ie on time. Their backend architecture with Django and billing integration was solid, scalable, and extremely secure.",
                author: "Dr. Adrian O'Connor",
                role: "Founder, ConnectDoc",
                rating: 5
            },
            {
                quote: "The web development team is outstanding. They restructured our Shopify and WooCommerce e-commerce platforms, optimizing page loading speed by 50% and doubling conversion rates.",
                author: "Sarah Jenkins",
                role: "Director of Operations, Glamour & Co",
                rating: 5
            },
            {
                quote: "Their AI chatbots and custom LLM integrations have automated our client onboarding. Onion Techs engineers are highly professional, agile, and technically superior.",
                author: "David Vance",
                role: "VP of Product, FinVerify",
                rating: 5
            },
            {
                quote: "We hired their dedicated developers for our mobile app project in React Native. The codebase is clean, well-tested, and their support is prompt. Highly recommended!",
                author: "Klaus Weber",
                role: "CTO, NextGen Logistics",
                rating: 5
            }
        ];

        if (!this.testimonialContainer) return;
        this.renderTestimonial();
        this.startTestimonialTimer();

        // Add swipe/button event listeners
        const prevBtn = document.getElementById("testimonial-prev");
        const nextBtn = document.getElementById("testimonial-next");

        if (prevBtn) {
            prevBtn.addEventListener("click", () => {
                this.stopTestimonialTimer();
                this.currentTestimonialIndex = (this.currentTestimonialIndex - 1 + this.testimonials.length) % this.testimonials.length;
                this.renderTestimonial();
                this.startTestimonialTimer();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener("click", () => {
                this.stopTestimonialTimer();
                this.currentTestimonialIndex = (this.currentTestimonialIndex + 1) % this.testimonials.length;
                this.renderTestimonial();
                this.startTestimonialTimer();
            });
        }
    }

    private renderTestimonial(): void {
        if (!this.testimonialContainer) return;
        const current = this.testimonials[this.currentTestimonialIndex];
        
        let starsHTML = "";
        for (let i = 0; i < current.rating; i++) {
            starsHTML += "⭐";
        }

        // Fade animation during transitions
        this.testimonialContainer.style.opacity = "0";
        this.testimonialContainer.style.transform = "translateY(10px)";
        
        setTimeout(() => {
            this.testimonialContainer!.innerHTML = `
                <div class="text-yellow-400 text-2xl mb-4">${starsHTML}</div>
                <p class="text-xl md:text-2xl text-gray-700 italic font-medium leading-relaxed">"${current.quote}"</p>
                <div class="mt-8">
                    <h4 class="font-bold text-lg text-[#070B34]">${current.author}</h4>
                    <p class="text-purple-600 text-sm font-semibold uppercase mt-1 tracking-wider">${current.role}</p>
                </div>
            `;
            this.testimonialContainer!.style.opacity = "1";
            this.testimonialContainer!.style.transform = "translateY(0)";
            this.testimonialContainer!.style.transition = "all 0.5s ease-out";
        }, 350);
    }

    private startTestimonialTimer(): void {
        this.testimonialInterval = window.setInterval(() => {
            this.currentTestimonialIndex = (this.currentTestimonialIndex + 1) % this.testimonials.length;
            this.renderTestimonial();
        }, 6000);
    }

    private stopTestimonialTimer(): void {
        if (this.testimonialInterval) {
            clearInterval(this.testimonialInterval);
        }
    }

    /**
     * Custom lightweight element reveal animations
     */
    private setupScrollAnimations(): void {
        const revealElements = document.querySelectorAll(".reveal");
        if (revealElements.length === 0) return;

        const revealOnScroll = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("active");
                    revealOnScroll.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealElements.forEach(el => revealOnScroll.observe(el));
    }
}

// Instantiate the application
new OnionApp();
