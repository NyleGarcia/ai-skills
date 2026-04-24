#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * extracts "lessons learned" from the .gemini/antigravity/brain directory.
 * searches for resolved plan files and user hints.
 */

const GEMINI_DIR = path.join(os.homedir(), '.gemini');
const BRAIN_DIR = path.join(GEMINI_DIR, 'antigravity', 'brain');

if (!fs.existsSync(BRAIN_DIR)) {
    console.error("Failure: .gemini brain dir not found.");
    process.exit(1);
}

function findResolvedPlans(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const filePath = path.join(dir, file);
        if (fs.statSync(filePath).isDirectory()) {
            findResolvedPlans(filePath, fileList);
        } else if (file.endsWith('.resolved') || file.endsWith('.resolved.0')) {
            fileList.push(filePath);
        }
    });
    return fileList;
}

const plans = findResolvedPlans(BRAIN_DIR);
console.log(`Success: Found ${plans.length} resolved plans.`);

const lessons = [];

plans.slice(-10).forEach(planPath => {
    const content = fs.readFileSync(planPath, 'utf8');
    // Basic heuristic: look for "lesson", "preference", "mandate", "never", "always"
    const matches = content.match(/(always|never|prefer|mandate).{1,100}/gi);
    if (matches) {
        lessons.push(`--- From ${path.basename(planPath)} ---\n${matches.join('\n')}`);
    }
});

if (lessons.length > 0) {
    console.log("\n### Extracted Signals:\n");
    console.log(lessons.join('\n\n').substring(0, 2000));
} else {
    console.log("No explicit signals found in recent plans.");
}
