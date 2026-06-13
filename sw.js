/* Bushcraft Companion — Service Worker
   Simple cache-first strategy. Caches the app shell on install,
   serves from cache on fetch, falls back to network. */

const CACHE = 'bushcraft-v7';
const ASSETS = [
  './',
  './index.html',
  './sw.js',
  './manifest.json',
  './hero-bg.jpg',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './favicon-32.png'
];
// Bundled photos — best-effort precache (failure of any one must not abort install).
const IMG = [
  'ban-guides','ban-firstaid','ban-projects','ban-notes','ban-plants',
  'cat-fire','cat-shelter','cat-water','cat-food','cat-signalling','cat-psychology',
  'fa-snake-brown','fa-snake-tiger','fa-snake-taipan','fa-snake-rbb','fa-snake-deathadder',
  'fa-spider-funnelweb','fa-spider-redback','fa-spider-whitetail',
  'plant-quandong','plant-finger-lime','plant-macadamia','plant-bunya','plant-warrigal-greens',
  'plant-pigface','plant-lilly-pilly','plant-native-raspberry','plant-kakadu-plum',
  'plant-wattleseed','plant-river-mint','plant-bush-tomato'
].map((n) => './img/' + n + '.jpg').concat(['./img/credits.json']);

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then(async (cache) => {
      await cache.addAll(ASSETS);
      await Promise.allSettled(IMG.map((u) => cache.add(u)));
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
