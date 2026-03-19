const CACHE_NAME = 'civicengage-v2';
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  // API calls: network only, never cache
  if (
    url.hostname.includes('anthropic') ||
    url.hostname.includes('geoapify') ||
    url.hostname.includes('represent') ||
    url.hostname.includes('openparliament') ||
    url.hostname.includes('wikipedia') ||
    url.hostname.includes('workers.dev')
  ) {
    return;
  }
  // HTML pages: stale-while-revalidate so users always get fresh content
  if (event.request.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname === '/') {
    event.respondWith(
      caches.open(CACHE_NAME).then(cache =>
        cache.match(event.request).then(cached => {
          const fetchPromise = fetch(event.request).then(response => {
            if (response && response.status === 200) {
              cache.put(event.request, response.clone());
            }
            return response;
          }).catch(() => cached);
          return cached || fetchPromise;
        })
      )
    );
    return;
  }
  // Other assets: cache-first
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
