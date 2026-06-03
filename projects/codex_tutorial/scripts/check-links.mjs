import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const markdownFiles = [];

function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, name);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      walk(fullPath);
    } else if (name.endsWith(".md")) {
      markdownFiles.push(fullPath);
    }
  }
}

function stripFences(text) {
  return text.replace(/```[\s\S]*?```/g, "");
}

function isExternal(ref) {
  return ref.startsWith("http://") || ref.startsWith("https://") || ref.startsWith("mailto:") || ref.startsWith("#");
}

function assertLocalRef(fromFile, ref, failures) {
  if (!ref || isExternal(ref)) return;
  const target = ref.split("#")[0];
  if (!target) return;
  const resolved = path.resolve(path.dirname(fromFile), target);
  if (!fs.existsSync(resolved)) {
    failures.push(`${path.relative(root, fromFile)} -> ${ref}`);
  }
}

walk(root);

const failures = [];
const markdownLinkPattern = /!\[[^\]]*\]\(([^)]+)\)|(?<!!?)\[[^\]]+\]\(([^)]+)\)/g;

for (const file of markdownFiles) {
  const text = stripFences(fs.readFileSync(file, "utf8"));
  for (const match of text.matchAll(markdownLinkPattern)) {
    assertLocalRef(file, match[1] || match[2], failures);
  }
}

const htmlPath = path.join(root, "index.html");
const html = fs.readFileSync(htmlPath, "utf8");
for (const match of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
  assertLocalRef(htmlPath, match[1], failures);
}

if (failures.length > 0) {
  console.error("Broken local links:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Checked ${markdownFiles.length} markdown files and index.html. Local links/images OK.`);
