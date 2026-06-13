/* Bushcraft Companion — Service Worker
   Simple cache-first strategy. Caches the app shell on install,
   serves from cache on fetch, falls back to network. */

const CACHE = 'bushcraft-v8';
const ASSETS = [
  './',
  './index.html',
  './sw.js',
  './manifest.json',
  './hero-bg.jpg',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './favicon-32.png',
  './img/credits.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then(async (cache) => {
      await cache.addAll(ASSETS);
      // Data-driven photo precache: every key in credits.json maps to ./img/<key>.jpg.
      try {
        const cr = await (await fetch('./img/credits.json')).json();
        const imgs = Object.keys(cr).map((k) => './img/' + k + '.jpg');
        await Promise.allSettled(imgs.map((u) => cache.add(u)));
      } catch (e) { /* offline / first-load race — runtime caching will fill gaps */ }
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req)
        .then((res) => {
          // Cache same-origin successful responses for offline reuse.
          if (res && res.status === 200 && res.type === 'basic') {
            const clone = res.clone();
            caches.open(CACHE).then((cache) => cache.put(req, clone));
          }
          return res;
        })
        .catch(() => {
          // Offline fallback: serve the app shell for navigations.
          if (req.mode === 'navigate') return caches.match('./index.html');
        });
    })
  );
});
