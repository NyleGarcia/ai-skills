---
name: playwright-e2e
description: Automates web app testing. Claude can test your UI flows end-to-end.
---

# Playwright E2E Testing

End-to-End browser testing agent. 

## Core Workflow
1. **Setup:** Ensure `playwright` is installed in project.
2. **Analysis:** Review DOM structure or user flow requirements.
3. **Scripting:** Generate resilient Playwright tests using `page.getByRole`, `page.getByText` (avoid fragile CSS selectors).
4. **Validation:** Run tests, intercept network if needed, capture trace/screenshots on failure.

## Directives
- ALWAYS prefer accessible locators (roles, alt text, ARIA labels).
- NEVER use fragile XPath or auto-generated CSS selectors unless unavoidable.
- Await state changes explicitly (e.g., `expect(locator).toBeVisible()`).
