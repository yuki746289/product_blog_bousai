/* Created: 2026-09-02 / Updated: 2026-09-04 / common preview behavior */
(function () {
  var FONT_SIZE_STORAGE_KEY = "bousai-font-size";
  var MOBILE_NAV_MEDIA_QUERY = "(max-width: 720px)";
  var FONT_SIZE_LEVELS = {
    normal: { label: "普通", scale: "100%" },
    large: { label: "大", scale: "112.5%" },
    xlarge: { label: "特大", scale: "125%" }
  };

  function markImageError(img) {
    if (!img || img.dataset.fallbackHandled === "1") return;
    img.dataset.fallbackHandled = "1";

    /* Product cards already have a product-specific fallback. */
    if (img.closest(".product-recommendation__image")) return;

    var holder = img.closest(
      "figure, .official-link-visual, .card-thumb, .topic-card__thumb, .pickup-card__visual--image"
    );

    if (!holder) {
      img.hidden = true;
      return;
    }

    holder.classList.add("is-image-error");
    img.remove();

    if (!holder.querySelector(".image-error-note")) {
      var note = document.createElement("p");
      note.className = "image-error-note";
      note.textContent = "画像を読み込めません。本文・出典リンクの情報をご確認ください。";
      holder.appendChild(note);
    }
  }

  function ensureFontSizeStyles() {
    if (document.getElementById("bousai-font-size-styles")) return;

    var style = document.createElement("style");
    style.id = "bousai-font-size-styles";
    style.textContent = [
      'html[data-font-size="normal"] { font-size: 100%; }',
      'html[data-font-size="large"] { font-size: 112.5%; }',
      'html[data-font-size="xlarge"] { font-size: 125%; }',
      '.font-size-control { display: flex; align-items: center; gap: 6px; flex: 0 0 auto; font-size: 14px; line-height: 1.2; }',
      '.font-size-control__label { color: #52616a; font-size: 12px; font-weight: 700; white-space: nowrap; }',
      '.font-size-control__button { min-width: 42px; min-height: 36px; padding: 7px 9px; border: 1px solid #c8d2d7; border-radius: 8px; background: #fff; color: #243b53; font: inherit; font-weight: 700; cursor: pointer; }',
      '.font-size-control__button:hover { background: #f1f7f6; }',
      '.font-size-control__button[aria-pressed="true"] { border-color: #176b68; background: #e3f1f0; color: #104c4a; box-shadow: inset 0 0 0 1px #176b68; }',
      '.font-size-control__button:focus-visible { outline: 3px solid rgba(23, 107, 104, .28); outline-offset: 2px; }',
      '@media (max-width: 720px) { .header-top { flex-wrap: wrap; gap: 8px 14px; padding: 8px 0; } .font-size-control { margin-left: auto; } .font-size-control__label { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; } }'
    ].join("\n");
    document.head.appendChild(style);
  }

  function ensureMobileNavStyles() {
    if (document.getElementById("bousai-mobile-nav-styles")) return;

    var style = document.createElement("style");
    style.id = "bousai-mobile-nav-styles";
    style.textContent = [
      '.mobile-nav-toggle { display: none; }',
      '@media (max-width: 720px) {',
      '  .header-top { display: grid !important; grid-template-columns: minmax(0, 1fr) auto; align-items: center !important; gap: 8px 12px !important; padding: 8px 0 !important; }',
      '  .site-brand { min-width: 0; }',
      '  .font-size-control { grid-column: 1 / -1; grid-row: 2; justify-self: end; margin-left: 0 !important; }',
      '  .mobile-nav-toggle { grid-column: 2; grid-row: 1; display: inline-flex; align-items: center; justify-content: center; gap: 7px; min-width: 44px; min-height: 44px; padding: 8px 10px; border: 1px solid #c8d2d7; border-radius: 9px; background: #fff; color: #243b53; font: inherit; font-weight: 750; cursor: pointer; }',
      '  .mobile-nav-toggle:hover { background: #f1f7f6; }',
      '  .mobile-nav-toggle:focus-visible { outline: 3px solid rgba(23, 107, 104, .28); outline-offset: 2px; }',
      '  .mobile-nav-toggle[aria-expanded="true"] { border-color: #176b68; background: #e3f1f0; color: #104c4a; }',
      '  .mobile-nav-toggle__icon { display: inline-block; width: 1.2em; font-size: 1.35rem; line-height: 1; text-align: center; }',
      '  .mobile-nav-toggle__label { font-size: .82rem; line-height: 1.2; }',
      '  .site-nav.mobile-nav-enhanced { display: none; flex-direction: column; gap: 0; overflow: visible; padding: 4px 0 12px; border-top: 1px solid var(--line); white-space: normal; font-size: .96rem; }',
      '  .site-nav.mobile-nav-enhanced.is-open { display: flex; }',
      '  .site-nav.mobile-nav-enhanced a { display: block; padding: 12px 10px; border-bottom: 1px solid var(--line); }',
      '  .site-nav.mobile-nav-enhanced a[aria-current] { background: var(--primary-soft); color: var(--primary-dark); }',
      '}'
    ].join("\n");
    document.head.appendChild(style);
  }

  function normalizeFontSizeLevel(level) {
    return Object.prototype.hasOwnProperty.call(FONT_SIZE_LEVELS, level) ? level : "normal";
  }

  function readSavedFontSizeLevel() {
    try {
      return normalizeFontSizeLevel(window.localStorage.getItem(FONT_SIZE_STORAGE_KEY));
    } catch (error) {
      return "normal";
    }
  }

  function saveFontSizeLevel(level) {
    try {
      window.localStorage.setItem(FONT_SIZE_STORAGE_KEY, level);
    } catch (error) {
      /* Storage can be unavailable in privacy-restricted environments. */
    }
  }

  function applyFontSizeLevel(level) {
    var normalized = normalizeFontSizeLevel(level);
    document.documentElement.setAttribute("data-font-size", normalized);

    document.querySelectorAll(".font-size-control__button[data-font-size]").forEach(function (button) {
      var selected = button.getAttribute("data-font-size") === normalized;
      button.setAttribute("aria-pressed", selected ? "true" : "false");
    });

    return normalized;
  }

  function enhanceFontSizeControl() {
    ensureFontSizeStyles();
    var currentLevel = applyFontSizeLevel(readSavedFontSizeLevel());
    var headerTop = document.querySelector(".header-top");
    if (!headerTop || headerTop.querySelector(".font-size-control")) return;

    var group = document.createElement("div");
    group.className = "font-size-control";
    group.setAttribute("role", "group");
    group.setAttribute("aria-label", "文字サイズ");

    var label = document.createElement("span");
    label.className = "font-size-control__label";
    label.textContent = "文字サイズ";
    group.appendChild(label);

    Object.keys(FONT_SIZE_LEVELS).forEach(function (level) {
      var option = FONT_SIZE_LEVELS[level];
      var button = document.createElement("button");
      button.type = "button";
      button.className = "font-size-control__button";
      button.setAttribute("data-font-size", level);
      button.setAttribute("aria-pressed", level === currentLevel ? "true" : "false");
      button.setAttribute("title", "文字サイズを" + option.label + "にする");
      button.textContent = option.label;
      button.addEventListener("click", function () {
        var applied = applyFontSizeLevel(level);
        saveFontSizeLevel(applied);
      });
      group.appendChild(button);
    });

    headerTop.appendChild(group);
  }

  function setMobileNavState(nav, button, expanded) {
    var isExpanded = Boolean(expanded);
    nav.classList.toggle("is-open", isExpanded);
    button.setAttribute("aria-expanded", isExpanded ? "true" : "false");
    button.setAttribute("aria-label", isExpanded ? "メニューを閉じる" : "メニューを開く");

    var icon = button.querySelector(".mobile-nav-toggle__icon");
    var label = button.querySelector(".mobile-nav-toggle__label");
    if (icon) icon.textContent = isExpanded ? "×" : "☰";
    if (label) label.textContent = isExpanded ? "閉じる" : "メニュー";
  }

  function enhanceMobileNavigation() {
    var nav = document.querySelector(".site-nav");
    var headerTop = document.querySelector(".header-top");
    if (!nav || !headerTop || headerTop.querySelector(".mobile-nav-toggle")) return;

    ensureMobileNavStyles();

    if (!nav.id) nav.id = "site-main-nav";

    var button = document.createElement("button");
    button.type = "button";
    button.className = "mobile-nav-toggle";
    button.setAttribute("aria-controls", nav.id);
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-label", "メニューを開く");

    var icon = document.createElement("span");
    icon.className = "mobile-nav-toggle__icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = "☰";

    var label = document.createElement("span");
    label.className = "mobile-nav-toggle__label";
    label.textContent = "メニュー";

    button.appendChild(icon);
    button.appendChild(label);
    headerTop.appendChild(button);

    nav.classList.add("mobile-nav-enhanced");
    setMobileNavState(nav, button, false);

    var media = window.matchMedia(MOBILE_NAV_MEDIA_QUERY);

    button.addEventListener("click", function () {
      var expanded = button.getAttribute("aria-expanded") === "true";
      setMobileNavState(nav, button, !expanded);
    });

    nav.querySelectorAll("a[href]").forEach(function (link) {
      link.addEventListener("click", function () {
        if (media.matches) setMobileNavState(nav, button, false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape" || button.getAttribute("aria-expanded") !== "true") return;
      setMobileNavState(nav, button, false);
      button.focus();
    });

    document.addEventListener("click", function (event) {
      if (!media.matches || button.getAttribute("aria-expanded") !== "true") return;
      var header = button.closest(".site-header");
      if (header && !header.contains(event.target)) {
        setMobileNavState(nav, button, false);
      }
    });

    function handleViewportChange(event) {
      if (!event.matches) setMobileNavState(nav, button, false);
    }

    if (typeof media.addEventListener === "function") {
      media.addEventListener("change", handleViewportChange);
    } else if (typeof media.addListener === "function") {
      media.addListener(handleViewportChange);
    }
  }

  function enhanceAccessibility() {
    var main = document.querySelector("main");
    if (main) {
      if (!main.id) main.id = "main-content";
      if (!document.querySelector(".skip-link")) {
        var skip = document.createElement("a");
        skip.className = "skip-link";
        skip.href = "#" + main.id;
        skip.textContent = "本文へ移動";
        document.body.insertBefore(skip, document.body.firstChild);
      }
    }

    document.querySelectorAll(".breadcrumb").forEach(function (breadcrumb) {
      if (!breadcrumb.hasAttribute("aria-label")) {
        breadcrumb.setAttribute("aria-label", "パンくず");
      }
    });

    document.querySelectorAll(".table-wrap").forEach(function (wrapper) {
      if (!wrapper.hasAttribute("tabindex")) wrapper.setAttribute("tabindex", "0");
      if (!wrapper.hasAttribute("role")) wrapper.setAttribute("role", "region");

      if (!wrapper.hasAttribute("aria-label")) {
        var tableLabel = "表";
        var node = wrapper.previousElementSibling;
        while (node) {
          if (/^H[23]$/.test(node.tagName)) {
            tableLabel = (node.textContent || "").trim() + "の表";
            break;
          }
          node = node.previousElementSibling;
        }
        wrapper.setAttribute("aria-label", tableLabel);
      }
    });

    var currentFile = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
    var navLinks = Array.prototype.slice.call(document.querySelectorAll(".site-nav a[href]"));
    var currentMarked = false;

    navLinks.forEach(function (link) {
      var href = (link.getAttribute("href") || "").split("#")[0].split("?")[0].toLowerCase();
      if (href === currentFile) {
        link.setAttribute("aria-current", "page");
        currentMarked = true;
      }
    });

    if (!currentMarked) {
      var categoryCrumb = document.querySelector('.breadcrumb a[href^="category_"]');
      if (categoryCrumb) {
        var categoryHref = (categoryCrumb.getAttribute("href") || "").split("#")[0].split("?")[0].toLowerCase();
        navLinks.forEach(function (link) {
          var href = (link.getAttribute("href") || "").split("#")[0].split("?")[0].toLowerCase();
          if (href === categoryHref) {
            link.setAttribute("aria-current", "location");
          }
        });
      }
    }
  }

  function bindImageFallbacks() {
    document.querySelectorAll("img").forEach(function (img) {
      img.addEventListener("error", function () {
        markImageError(img);
      }, { once: true });

      if (img.complete && img.naturalWidth === 0) {
        markImageError(img);
      }
    });
  }

  function sendAnalyticsEvent(name, parameters) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, parameters);
  }

  function normalizedLinkText(link) {
    return (link.textContent || "").replace(/\s+/g, " ").trim().slice(0, 120);
  }

  function isAmazonHost(hostname) {
    var host = hostname.toLowerCase();
    return host === "amzn.to" || host === "amazon.co.jp" || host.endsWith(".amazon.co.jp");
  }

  function bindTrackedLinks() {
    document.addEventListener("click", function (event) {
      var target = event.target;
      if (!target || typeof target.closest !== "function") return;

      var link = target.closest("a[href]");
      if (!link) return;

      var url;
      try {
        url = new URL(link.href, window.location.href);
      } catch (error) {
        return;
      }

      var common = {
        link_url: url.href,
        link_text: normalizedLinkText(link),
        page_path: window.location.pathname,
        transport_type: "beacon"
      };

      if (isAmazonHost(url.hostname)) {
        sendAnalyticsEvent("amazon_click", common);
        return;
      }

      if (
        url.origin === window.location.origin &&
        /^\/goods\/.+\.html$/.test(url.pathname) &&
        !/\/goods\/index\.html$/.test(url.pathname) &&
        !/^\/goods\//.test(window.location.pathname)
      ) {
        sendAnalyticsEvent("product_guide_click", common);
      }
    }, { passive: true });
  }

  function init() {
    enhanceFontSizeControl();
    enhanceMobileNavigation();
    enhanceAccessibility();
    bindImageFallbacks();
    bindTrackedLinks();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}());
