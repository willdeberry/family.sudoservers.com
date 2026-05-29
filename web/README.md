# web/

Astro + Tailwind site that visualizes the Guthrie family tree dataset.
Deployed at <https://family.sudoservers.com>.

## Architecture

```
web/
  scripts/
    transform-data.mjs   ← reads ../data/people.json, writes 3 JSON files
                          consumed by the client
  src/
    components/
      TopBar.astro        ← header with logo, search trigger, stats
      Tree.astro          ← family-chart instance + container
      PersonModal.astro   ← <dialog> that opens on card click
      SearchPalette.astro ← Cmd+K search palette
    layouts/Layout.astro
    pages/index.astro
    styles/global.css     ← Tailwind v4 import
  public/data/            ← generated, not committed:
                            tree.json, people-index.json, search.json
```

Data flow is one-way at build time:

```
../data/people.json  ─[transform-data.mjs]─→  web/public/data/*.json
                                                       │
                                                       ↓
                                                  fetch() in browser
```

## Local development

```bash
cd web
npm install        # one-time
npm run dev        # http://localhost:4321 (runs the transform first)
```

`predev` and `prebuild` hooks run `transform-data.mjs` automatically.
After editing `../parser/raw_entries.py`, run `python3 ../parser/build.py`
then restart `npm run dev` (or `npm run transform`).

## Production build

```bash
npm run build
# → web/dist/  (static files ready to serve)
```

## Deploy to sudoservers.com

The site is plain static files; any static-file webserver works. Example
with nginx:

### 1. Sync to the server

```bash
rsync -avz --delete web/dist/ user@sudoservers.com:/var/www/family.sudoservers.com/
```

### 2. nginx vhost

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name family.sudoservers.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name family.sudoservers.com;

    ssl_certificate     /etc/letsencrypt/live/family.sudoservers.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/family.sudoservers.com/privkey.pem;

    root /var/www/family.sudoservers.com;
    index index.html;

    # Data JSON files change on every rebuild. Short cache + revalidation.
    location /data/ {
        add_header Cache-Control "public, max-age=3600, must-revalidate";
    }

    # Fingerprinted assets can be cached forever
    location /_assets/ {
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # Gzip the JSON
    gzip on;
    gzip_types application/json text/css application/javascript image/svg+xml;
    gzip_min_length 1024;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 3. Update loop

After editing `../parser/raw_entries.py`:

```bash
python3 ../parser/build.py     # regenerates ../data/people.json
npm run build                   # regenerates web/dist/
rsync -avz --delete dist/ user@sudoservers.com:/var/www/family.sudoservers.com/
```

## Performance notes

- All 1351 people ship to the client as ~1.4MB of JSON (gzipped ~300KB).
  family-chart handles this size comfortably.
- Initial render shows ~900 cards centered on the founder. Users pan/zoom
  to explore.
- `people-index.json` and `search.json` load lazily on first modal open
  / first Cmd+K, so initial paint isn't blocked.

## Known limitations

- No write path yet — "Suggest an addition" is a mailto link. A real
  submission form would need a backend or a static-form service.
- Cards in the tree don't show a draft/verified badge yet (the modal does).
- Tree is purely descendant; no spouse-of-spouse traversal.
