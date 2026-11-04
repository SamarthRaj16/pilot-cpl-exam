const CACHE_NAME = "cpl-practice-v2-cache";
const SAFE_STATIC_ASSETS = [
  "/",
  "/dashboard",
  "/manifest.json",
  "/cpl-exam-direct.html"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(SAFE_STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // NEVER cache sensitive exam API endpoints
  if (url.pathname.startsWith("/api/quiz/")) {
    return; // Pass through to live network
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).catch(() => {
        // Return offline fallback if network fails
        if (event.request.mode === "navigate") {
          return caches.match("/cpl-exam-direct.html");
        }
      });
    })
  );
});
