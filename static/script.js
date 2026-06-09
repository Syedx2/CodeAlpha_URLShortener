/**
 * Sniplink — URL Shortener Frontend Logic (Production)
 * Handles form submission, result display, clipboard copy, and recent links.
 */

(function () {
    "use strict";

    // --- DOM References ---
    const form = document.getElementById("shorten-form");
    const urlInput = document.getElementById("url-input");
    const btnShorten = document.getElementById("btn-shorten");
    const errorMessage = document.getElementById("error-message");
    const resultSection = document.getElementById("result-section");
    const resultUrl = document.getElementById("result-url");
    const resultOriginal = document.getElementById("result-original");
    const btnCopy = document.getElementById("btn-copy");
    const recentList = document.getElementById("recent-list");
    const recentEmpty = document.getElementById("recent-empty");

    // --- Constants ---
    const API_SHORTEN = "/api/shorten";
    const API_RECENT = "/api/recent";
    const STORAGE_KEY = "sniplink_recent";

    // --- State ---
    let currentShortUrl = "";

    // --- Initialization ---
    init();

    function init() {
        form.addEventListener("submit", handleSubmit);
        btnCopy.addEventListener("click", handleCopy);
        loadRecentLinks();
    }

    // --- Form Submit ---
    async function handleSubmit(e) {
        e.preventDefault();

        const url = urlInput.value.trim();
        if (!url) return;

        // Reset UI
        hideError();
        hideResult();
        setLoading(true);

        try {
            const response = await fetch(API_SHORTEN, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.error || "Something went wrong. Please try again.");
                return;
            }

            // Show result
            currentShortUrl = data.short_url;
            showResult(data.short_url, data.original_url);

            // Save to local storage & refresh list
            saveToLocal(data);
            loadRecentLinks();

            // Clear input
            urlInput.value = "";

        } catch (err) {
            showError("Network error. Is the server running?");
            console.error("Shorten error:", err);
        } finally {
            setLoading(false);
        }
    }

    // --- Copy to Clipboard ---
    async function handleCopy() {
        if (!currentShortUrl) return;

        try {
            await navigator.clipboard.writeText(currentShortUrl);
            showCopiedState();
        } catch (err) {
            // Fallback for older browsers / non-HTTPS contexts
            const textArea = document.createElement("textarea");
            textArea.value = currentShortUrl;
            textArea.style.cssText = "position:fixed;opacity:0;left:-9999px";
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand("copy");
                showCopiedState();
            } catch (copyErr) {
                console.error("Copy failed:", copyErr);
            }
            document.body.removeChild(textArea);
        }
    }

    function showCopiedState() {
        btnCopy.classList.add("copied");
        const copyText = btnCopy.querySelector(".copy-text");
        const copyIcon = btnCopy.querySelector(".copy-icon-svg");

        copyText.textContent = "Copied!";

        // Change icon to checkmark
        if (copyIcon) {
            copyIcon.innerHTML = '<polyline points="20 6 9 17 4 12"/>';
        }

        setTimeout(() => {
            btnCopy.classList.remove("copied");
            copyText.textContent = "Copy";
            if (copyIcon) {
                copyIcon.innerHTML = '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>';
            }
        }, 2000);
    }

    // --- UI Helpers ---
    function setLoading(loading) {
        btnShorten.disabled = loading;
        btnShorten.classList.toggle("loading", loading);
    }

    function showResult(shortUrl, originalUrl) {
        resultUrl.innerHTML = '<a href="' + escapeHtml(shortUrl) + '" target="_blank" rel="noopener">' + escapeHtml(shortUrl) + '</a>';
        resultOriginal.textContent = "\u2192 " + originalUrl;
        resultSection.classList.add("visible");
    }

    function hideResult() {
        resultSection.classList.remove("visible");
        currentShortUrl = "";
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.add("visible");
    }

    function hideError() {
        errorMessage.classList.remove("visible");
    }

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    // --- Recent Links (Local Storage + Server) ---
    function saveToLocal(data) {
        let recent = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
        recent.unshift({
            short_code: data.short_code,
            short_url: data.short_url,
            original_url: data.original_url,
            created_at: new Date().toISOString(),
            click_count: 0,
        });
        // Keep only the last 10
        recent = recent.slice(0, 10);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(recent));
    }

    function loadRecentLinks() {
        var items = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
        renderRecentLinks(items);
    }

    function renderRecentLinks(items) {
        // Remove old items
        const existingItems = recentList.querySelectorAll(".recent-item");
        existingItems.forEach(function (el) { el.remove(); });

        if (!items || items.length === 0) {
            recentEmpty.style.display = "block";
            return;
        }

        recentEmpty.style.display = "none";
        const baseUrl = window.location.origin;

        items.forEach(function (item, index) {
            var el = document.createElement("div");
            el.classList.add("recent-item");
            el.style.animation = "fade-up 0.4s ease both " + (index * 0.05) + "s";

            var shortUrl = item.short_url || (baseUrl + "/" + item.short_code);

            el.innerHTML =
                '<span class="recent-item__code">' +
                    '<a href="' + escapeHtml(shortUrl) + '" target="_blank" rel="noopener">' + escapeHtml(item.short_code) + '</a>' +
                '</span>' +
                '<span class="recent-item__url" title="' + escapeHtml(item.original_url) + '">' + escapeHtml(item.original_url) + '</span>' +
                '<span class="recent-item__clicks">' +
                    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5"/></svg> ' +
                    (item.click_count || 0) + ' clicks' +
                '</span>';

            recentList.appendChild(el);
        });
    }

    // --- Focus input on load ---
    urlInput.focus();

})();
