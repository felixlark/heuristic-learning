#!/usr/bin/env node

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const rootDir = path.resolve(__dirname, '..')
const docsDir = path.join(rootDir, 'docs')
const publicDir = path.join(docsDir, 'public')
const siteUrl = (
  process.env.SITE_URL || 'https://longbiaochen.github.io/heuristic-learning'
).replace(/\/+$/, '')
const skipWrite = process.env.SITEMAP_NO_WRITE === '1'

function scanMarkdown(dir, prefix = '') {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
  const files = []

  for (const entry of entries) {
    if (entry.name === '.vitepress' || entry.name === 'public') continue
    const fullPath = path.join(dir, entry.name)
    const relative = path.join(prefix, entry.name)

    if (entry.isDirectory()) {
      files.push(...scanMarkdown(fullPath, relative))
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(relative)
    }
  }

  return files
}

function toUrl(file) {
  let route = file.replace(/\.md$/, '')
  if (route === 'index') route = ''
  if (route.endsWith('/index')) route = route.slice(0, -'/index'.length)
  return `${siteUrl}/${route}`.replace(/\/+$/, '') || siteUrl
}

function escapeXml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}

const files = scanMarkdown(docsDir)
const urls = files.map((file) => {
  const fullPath = path.join(docsDir, file)
  return {
    loc: toUrl(file),
    lastmod: fs.statSync(fullPath).mtime.toISOString()
  }
})

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (url) => `  <url>
    <loc>${escapeXml(url.loc)}</loc>
    <lastmod>${url.lastmod}</lastmod>
    <changefreq>weekly</changefreq>
  </url>`
  )
  .join('\n')}
</urlset>
`

if (skipWrite) {
  console.log(`SITEMAP_NO_WRITE=1: scanned ${urls.length} pages`)
} else {
  fs.mkdirSync(publicDir, { recursive: true })
  fs.writeFileSync(path.join(publicDir, 'sitemap.xml'), xml)
  console.log(`Generated sitemap for ${urls.length} pages`)
}
