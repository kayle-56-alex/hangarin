// This is the "Offline Copy" code [cite: 55-70]
self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('projectsite-cache-v1').then(function(cache) {
            return cache.addAll([
                '/static/css/bootstrap.min.css',
                '/static/js/main.js',
            ]);
        })
    );
});

self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});