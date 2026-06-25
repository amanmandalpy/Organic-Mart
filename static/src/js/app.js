/** Foundation behavior that remains optional to the core page experience. */
(() => {
    "use strict";

    const setupSpotlightCarousel = () => {
        const carousel = document.querySelector("#homepageSpotlightCarousel");
        if (!carousel) return;

        const interval = Number.parseInt(carousel.dataset.bsInterval || "3200", 10);

        if (window.bootstrap?.Carousel) {
            const bootstrapCarousel = window.bootstrap.Carousel.getOrCreateInstance(carousel, {
                interval,
                pause: false,
                ride: "carousel",
                touch: true,
                wrap: true,
            });
            bootstrapCarousel.cycle();
            return;
        }

        const items = [...carousel.querySelectorAll(".carousel-item")];
        const indicators = [...carousel.querySelectorAll("[data-bs-slide-to]")];
        const previousButton = carousel.querySelector("[data-bs-slide='prev']");
        const nextButton = carousel.querySelector("[data-bs-slide='next']");
        let activeIndex = Math.max(
            items.findIndex((item) => item.classList.contains("active")),
            0,
        );
        let timerId = null;

        if (items.length <= 1) return;

        const showSlide = (nextIndex) => {
            activeIndex = (nextIndex + items.length) % items.length;

            items.forEach((item, index) => {
                item.classList.toggle("active", index === activeIndex);
            });
            indicators.forEach((indicator, index) => {
                const isActive = index === activeIndex;
                indicator.classList.toggle("active", isActive);
                indicator.toggleAttribute("aria-current", isActive);
            });
        };

        const restartTimer = () => {
            if (timerId) window.clearInterval(timerId);
            timerId = window.setInterval(() => showSlide(activeIndex + 1), interval);
        };

        previousButton?.addEventListener("click", (event) => {
            event.preventDefault();
            showSlide(activeIndex - 1);
            restartTimer();
        });

        nextButton?.addEventListener("click", (event) => {
            event.preventDefault();
            showSlide(activeIndex + 1);
            restartTimer();
        });

        indicators.forEach((indicator, index) => {
            indicator.addEventListener("click", (event) => {
                event.preventDefault();
                showSlide(index);
                restartTimer();
            });
        });

        showSlide(activeIndex);
        restartTimer();
    };

    setupSpotlightCarousel();

    const header = document.querySelector("[data-site-header]");
    if (header) {
        const updateHeader = () => {
            header.classList.toggle("is-scrolled", window.scrollY > 8);
        };

        updateHeader();
        window.addEventListener("scroll", updateHeader, { passive: true });
    }

    const searchForm = document.querySelector("[data-live-search]");
    if (!searchForm) return;

    const input = searchForm.querySelector('input[name="q"]');
    const results = searchForm.querySelector("[data-live-search-results]");
    const suggestionsUrl = searchForm.dataset.suggestionsUrl;
    let activeController = null;

    const hideResults = () => {
        results.classList.remove("is-visible");
        results.innerHTML = "";
    };

    input.addEventListener("input", async () => {
        const query = input.value.trim();
        if (query.length < 2) {
            hideResults();
            return;
        }

        if (activeController) activeController.abort();
        activeController = new AbortController();

        try {
            const response = await fetch(`${suggestionsUrl}?q=${encodeURIComponent(query)}`, {
                headers: { "Accept": "application/json" },
                signal: activeController.signal,
            });
            const data = await response.json();

            if (!data.results.length) {
                hideResults();
                return;
            }

            results.innerHTML = data.results
                .map((item) => (
                    `<a href="${item.url}"><span>${item.emoji} ${item.name}</span><strong>₹${item.price}</strong></a>`
                ))
                .join("");
            results.classList.add("is-visible");
        } catch (error) {
            if (error.name !== "AbortError") hideResults();
        }
    });

    document.addEventListener("click", (event) => {
        if (!searchForm.contains(event.target)) hideResults();
    });
})();
