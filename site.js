"use strict";

// Keep translations local: no remote fonts, analytics, or translation services.
const translations = [...document.querySelectorAll("[data-en], [data-en-alt], [data-en-label]")].map(element => ({
  element,
  korean: element.hasAttribute("data-en") ? element.innerHTML : null,
  alt: element.getAttribute("alt"),
  label: element.getAttribute("aria-label")
}));
const languageButton = document.getElementById("language-toggle");
const description = document.querySelector('meta[name="description"]');
const koreanDescription = description.content;
function setLanguage(language) {
  const english = language === "en";
  document.documentElement.lang = english ? "en" : "ko";
  translations.forEach(({element, korean, alt, label}) => {
    if (korean !== null) {
      if (english) element.textContent = element.dataset.en;
      else element.innerHTML = korean; // Only restores trusted markup from this document.
    }
    if (element.hasAttribute("data-en-alt")) element.alt = english ? element.dataset.enAlt : alt;
    if (element.hasAttribute("data-en-label")) element.setAttribute("aria-label", english ? element.dataset.enLabel : label);
  });
  languageButton.replaceChildren(document.createTextNode(english ? "한국어 ↗" : "EN ↗"));
  languageButton.setAttribute("aria-label", english ? "한국어로 전환" : "Switch to English");
  description.content = english
    ? "Islo is an iPhone cycling navigation app in development. Discover routes, voice assistance, riding weather, ride recording and 3D replay. Not yet released."
    : koreanDescription;
  try { localStorage.setItem("islo.site.language", english ? "en" : "ko"); } catch { /* Storage is optional. */ }
}
languageButton.addEventListener("click", () => setLanguage(document.documentElement.lang === "en" ? "ko" : "en"));
let preferredLanguage = "ko";
try { preferredLanguage = localStorage.getItem("islo.site.language") === "en" ? "en" : "ko"; } catch { /* Keep Korean default. */ }
const requestedLanguage = new URLSearchParams(window.location.search).get("lang");
setLanguage(requestedLanguage === "en" || requestedLanguage === "ko" ? requestedLanguage : preferredLanguage);
