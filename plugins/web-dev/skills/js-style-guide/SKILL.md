---
name: js-style-guide
description: Enforce comprehensive JavaScript/TypeScript coding standards based on the Airbnb JavaScript Style Guide. Use for all JS/TS code reviews, refactoring, or authoring.
---

# JavaScript Style Guide

Enforce clean, maintainable JS/TS. Apply these rules during code review, authoring, and refactoring.

## Core Rules

### 1. References & Variables
- **const/let:** Use `const` for all references; avoid `var`. Use `let` only for reassignment.
- **Grouping:** Group `const` declarations together, then group `let` declarations.
- **Naming:** `camelCase` for objects/functions/instances, `PascalCase` for classes/constructors, `UPPERCASE_SNAKE` for exported constants.

### 2. Objects & Arrays
- **Shorthand:** Use object method and property value shorthands.
- **Quoting:** Only quote properties that are invalid identifiers.
- **Copying:** Use spread operator `...` instead of `Object.assign` to shallow-copy objects.
- **Arrays:** Use array spreads `...` to copy arrays. Use `Array.from()` for converting iterables to arrays.
- **Trailing Commas:** Always use trailing commas in multiline object/array literals.

### 3. Destructuring
- **Objects:** Prefer object destructuring for accessing multiple properties.
- **Arrays:** Use array destructuring.
- **Returns:** Return objects, not arrays, for multiple return values to avoid positional destructuring bugs.

### 4. Strings
- **Quotes:** Use single quotes `''` for strings.
- **Templates:** Use template literals `\`` for programmatic string building. Never use string concatenation `+`.

### 5. Functions & Arrow Functions
- **Declarations:** Use named function expressions instead of function declarations.
- **Parameters:** Use default parameter syntax rather than mutating arguments.
- **Arguments:** Never use `arguments`, use rest syntax `...args` instead.
- **Arrow Functions:** Use arrow functions for anonymous callbacks. Use implicit return when the body is a single expression.
- **Binding:** Arrow functions bind `this` lexically.

### 6. Modules
- **Syntax:** Always use ES6 modules (`import`/`export`). Do not use CommonJS `require`/`module.exports`.
- **Wildcards:** Do not use wildcard imports (`import * as foo`).
- **Default Exports:** Prefer default exports for files containing a single export, named exports for utility files.

### 7. Classes
- **Usage:** Always use `class`. Avoid direct prototype manipulation.
- **Inheritance:** Use `extends` for inheritance.
- **Methods:** Methods can return `this` to help with method chaining. Custom `toString()` must be safe and have no side effects.

### 8. Iterators & Control Flow
- **Loops:** Avoid `for...in` and `for...of`. Use higher-order functions like `map()`, `filter()`, `reduce()`, `some()`, `every()`.
- **Equality:** Always use `===` and `!==`. Never use `==` or `!=`.
- **Booleans:** Use shortcuts for booleans (e.g., `if (name)` instead of `if (name !== '')`).
- **Early Return:** Prefer early returns to avoid deep nesting of `if` statements.

## Execution Workflows

### Authoring Code
1. Verify no `var` is used.
2. Destructure parameters early in function signatures.
3. Validate module import/export structure.
4. Ensure naming conventions align with the guide.

### Code Review (Refactoring)
1. **Lints:** Identify and correct implicit type coercion, `==` comparisons, and missing curly braces on blocks.
2. **Modernization:** Convert `function() {}` to `() => {}`, `Object.assign` to spreads, and concatenated strings to template literals.
3. **Complexity:** Recommend array iteration methods to replace explicit `for` loops. Look for early return opportunities.

For edge cases, fall back to the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
