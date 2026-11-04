/**
 * LankaMedi AI — Service Worker (PWA)
 * Sri Lanka's Intelligent Medical Report Explainer
 */

const CACHE_NAME = 'lankamedi-pwa-v2.1';

const PRECACHE_ASSETS = [
    '/',
    '/static/css/main.css',
    '/static/js/app.js',
    '/static/js/i18n.js',
    '/static/manifest.json',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png',
    '/static/icons/icon-maskable-512x512.png',
    '/static/icons/apple-touch-icon.png',
    '/static/icons/favicon.ico',
    '/api/v1/reference-ranges'
];

// Offline HTML fallback for page navigations when completely offline and un-cached
const OFFLINE_FALLBACK_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LankaMedi AI — Offline</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 2rem 1.5rem;
            background: #f8fafc;
            color: #0f172a;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            box-sizing: border-box;
        }
        .offline-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1.25rem;
            max-width: 480px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
        }
        .offline-icon { font-size: 3.5rem; margin-bottom: 1rem; }
        h1 { font-size: 1.5rem; margin: 0 0 0.75rem; color: #0f766e; }
        p { color: #64748b; line-height: 1.6; margin: 0 0 1.5rem; }
        .emergency-box {
            background: #fef2f2;
            border: 1px solid #fee2e2;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
            text-align: left;
        }
        .emergency-box strong { color: #dc2626; display: block; margin-bottom: 0.25rem; }
        .emergency-box a { color: #dc2626; font-weight: 700; text-decoration: none; font-size: 1.2rem; }
        .btn-retry {
            display: inline-block;
            background: #0f766e;
            color: #ffffff;
            font-weight: 600;
            padding: 0.75rem 1.75rem;
            border-radius: 9999px;
            text-decoration: none;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="offline-card">
        <div class="offline-icon">📡</div>
        <h1>You are currently offline</h1>
        <p>LankaMedi AI could not connect to the network. Please verify your Wi-Fi or mobile data connection and try again.</p>
        <div class="emergency-box">
            <strong>🚨 Urgent Medical Emergency?</strong>
            <span>Do not wait for connectivity. Call Sri Lanka's free ambulance service:</span><br>
            <a href="tel:1990">📞 Call 1990 (Suwa Seriya)</a>
        </div>
        <button class="btn-retry" onclick="window.location.reload()">Retry Connection</button>
    </div>
</body>
</html>`;

// 1. Install Event: Pre-cache core shell
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(PRECACHE_ASSETS).catch((err) => {
                console.warn('[PWA] Pre-cache partial warning:', err);
            });
        })
    );
    self.skipWaiting();
});

// 2. Activate Event: Clean up outdated caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('[PWA] Removing obsolete cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// 3. Fetch Event: Routing & Caching Strategy
self.addEventListener('fetch', (event) => {
    const request = event.request;
    const url = new URL(request.url);

    // Non-GET requests (e.g. POST /api/v1/analyze)
    if (request.method !== 'GET') {
        if (url.pathname.includes('/analyze')) {
            event.respondWith(
                fetch(request).catch(() => {
                    return new Response(
                        JSON.stringify({
                            success: false,
                            offline: true,
                            error: 'Offline Mode: LankaMedi AI requires an active internet connection to synthesize clinical AI insights. Please check your data connection.',
                            emergency_contacts: {
                                "1990": "National Suwa Seriya Free Pre-Hospital Care Ambulance",
                                "National Hospital (NHSL)": "+94 11 269 1111",
                                "National Poisons Center": "+94 11 268 6143"
                            }
                        }),
                        {
                            status: 503,
                            headers: { 'Content-Type': 'application/json; charset=utf-8' }
                        }
                    );
                })
            );
        }
        return;
    }

    // A. Reference Ranges API: Stale-While-Revalidate (ensure offline lab ranges lookup)
    if (url.pathname === '/api/v1/reference-ranges') {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(request).then((cachedResponse) => {
                    const fetchPromise = fetch(request).then((networkResponse) => {
                        if (networkResponse && networkResponse.status === 200) {
                            cache.put(request, networkResponse.clone());
                        }
                        return networkResponse;
                    }).catch(() => cachedResponse);

                    return cachedResponse || fetchPromise;
                });
            })
        );
        return;
    }

    // B. Static Assets: CSS, JS, Images, Icons, Manifest
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(request).then((cachedResponse) => {
                if (cachedResponse) {
                    // Update cache in the background
                    fetch(request).then((networkResponse) => {
                        if (networkResponse && networkResponse.status === 200) {
                            caches.open(CACHE_NAME).then((cache) => cache.put(request, networkResponse));
                        }
                    }).catch(() => {});
                    return cachedResponse;
                }
                return fetch(request).then((networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        const responseClone = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
                    }
                    return networkResponse;
                });
            })
        );
        return;
    }

    // C. Navigation requests (HTML pages)
    if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
        event.respondWith(
            fetch(request).then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
                }
                return networkResponse;
            }).catch(() => {
                return caches.match(request).then((cachedResponse) => {
                    if (cachedResponse) {
                        return cachedResponse;
                    }
                    return caches.match('/').then((rootCached) => {
                        return rootCached || new Response(OFFLINE_FALLBACK_HTML, {
                            status: 200,
                            headers: { 'Content-Type': 'text/html; charset=utf-8' }
                        });
                    });
                });
            })
        );
        return;
    }

    // D. Default: Cache first with Network fallback
    event.respondWith(
        caches.match(request).then((cachedResponse) => {
            return cachedResponse || fetch(request).catch(() => {
                // Ignore failure for optional peripheral resources
            });
        })
    );
});

// 4. Message Event: Handle instant updates
self.addEventListener('message', (event) => {
    if (event.data && event.data.action === 'skipWaiting') {
        self.skipWaiting();
    }
});

