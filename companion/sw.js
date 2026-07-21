const CACHE = "kvassistent-live-v9";
const ASSETS = ["./","index.html","styles.css","engine.js","preferences.js","app.js","manifest.webmanifest","icon.svg","icon-192.png","icon-512.png"];
self.addEventListener("install", event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting())));
self.addEventListener("activate", event => event.waitUntil(Promise.all([
  caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith("kvassistent-live-") && key !== CACHE).map(key => caches.delete(key)))),
  self.clients.claim(),
])));
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request).then(response => {
      const copy = response.clone(); caches.open(CACHE).then(cache => cache.put("./", copy)); return response;
    }).catch(() => caches.match("./")));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => {
    const network = fetch(event.request).then(response => {
      if (response.ok) caches.open(CACHE).then(cache => cache.put(event.request, response.clone()));
      return response;
    });
    return cached || network;
  }));
});
