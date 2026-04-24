---
name: web-quality
description: Optimize web projects for Performance, Core Web Vitals, Accessibility, and SEO based on Lighthouse.
---

# Web Quality

Lighthouse-driven optimization for any web framework. 

## Commands & Focus Areas
- `/web-quality-audit`: Full check. 50+ perf, 40+ a11y, 30+ SEO rules.
- `/performance`: Deep-dive speed. Critical render path, code split, image/font opt, caching.
- `/core-web-vitals`: Target Search ranking metrics.
  - LCP (Largest Contentful Paint) < 2.5s
  - INP (Interaction to Next Paint) < 200ms
  - CLS (Cumulative Layout Shift) < 0.1
- `/accessibility`: WCAG 2.2 compliance. Perceivable, Operable, Understandable, Robust. Contrast, keyboard nav, screen reader support.
- `/seo`: Tech SEO, meta tags, schema.org JSON-LD, crawlability.
- `/best-practices`: Security, modern APIs, code quality.

## Core Directives
1. Treat warnings as errors for Core Web Vitals.
2. Always verify keyboard navigation and ARIA roles.
3. Compress and lazy-load non-critical assets by default.
