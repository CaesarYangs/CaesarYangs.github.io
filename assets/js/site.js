// The site is readable without JavaScript. Retire the previous offline cache.
'use strict';

const year = document.querySelector('#year');
if (year) year.textContent = String(new Date().getFullYear());

// Retire only Paperbox's old root worker, never another app's registration.
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then(registrations => Promise.all(
    registrations.filter(registration => {
      const worker = registration.active || registration.waiting || registration.installing;
      if (!worker) return false;
      const url = new URL(worker.scriptURL);
      return url.origin === location.origin && url.pathname === '/sw.js';
    }).map(registration => registration.unregister())
  )).then(() => {
    if ('caches' in window) return caches.delete('/sw.js');
  }).catch(() => { /* Static navigation does not depend on cache APIs. */ });
}
