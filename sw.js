// Retirement worker for visitors who still have the previous Paperbox cached.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    await caches.delete('/sw.js');
    await self.registration.unregister();
    await self.clients.claim();
  })());
});
