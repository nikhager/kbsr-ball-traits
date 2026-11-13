// Tests for site/js/app.js. Node's built-in runner, no dependencies.
// Run from the repo root: node --test tests/*.test.mjs
//
// app.js is a plain browser script, so each test loads it into a sandbox with
// a tiny fake DOM (just enough for el() and card()) and a fetch that never
// resolves, then calls its functions directly. app.js itself is not changed.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const ROOT = new URL("../", import.meta.url);
const APP = readFileSync(new URL("site/js/app.js", ROOT), "utf8");
const DATA = JSON.parse(readFileSync(new URL("site/data/traits.json", ROOT), "utf8"));

class FakeElement {
    constructor(tag) { this.tag = tag; this.attrs = {}; this.children = []; this.className = ""; }
    setAttribute(k, v) { this.attrs[k] = String(v); }
    append(...kids) { this.children.push(...kids); }
    get textContent() {
        return this.children.map(c => (typeof c === "string" ? c : c.textContent)).join("");
    }
    // Every text node in this element and its children, one string each.
    texts() {
        return this.children.flatMap(c => (typeof c === "string" ? [c] : c.texts()));
    }
    // Every attribute value in this element and its children.
    allAttrs() {
        const own = Object.values(this.attrs);
        return own.concat(...this.children.filter(c => typeof c !== "string").map(c => c.allAttrs()));
    }
    find(cls) {
        if (this.className.split(" ").includes(cls)) return this;
        for (const c of this.children) {
            const hit = typeof c === "string" ? null : c.find(cls);
            if (hit) return hit;
        }
        return null;
    }
}

function loadApp() {
    const sandbox = {
        document: { createElement: tag => new FakeElement(tag), getElementById: () => null },
        window: {},
        location: { hash: "", pathname: "/", search: "" },
        history: { replaceState() {} },
        fetch: () => new Promise(() => {}),
        setTimeout: () => 0,
    };
    vm.createContext(sandbox);
    vm.runInContext(APP + "\n;globalThis.__app = { cardTags, slugify, card, state, TAGS, SHOTS };", sandbox);
    return sandbox.__app;
}

const trait = (overrides = {}) => ({
    id: "sharp-drive",
    name: "Sharp Drive",
    category: "Handling",
    tags: ["Ankle Break"],
    effect: "Increases Ankle Breaker Chance.",
    effectSource: "Tier III",
    trainingCamp: "",
    tiers: {
        II: { value: "+1.2%", icon: "images/icons/sharp-drive-ii.webp", seenOn: "" },
        III: { value: "+1.5%", icon: "images/icons/sharp-drive-iii.webp", seenOn: "" },
    },
    collections: [{ name: "Akashi Collection" }, { name: "Nash" }],
    ...overrides,
});

test("slugify makes lowercase hyphenated slugs", () => {
    const { slugify } = loadApp();
    assert.equal(slugify("Ankle Break"), "ankle-break");
    assert.equal(slugify("LAST GAME Kise"), "last-game-kise");
    assert.equal(slugify("3PT"), "3pt");
});

test("cardTags collapses all five shot tags into one All shots chip", () => {
    const { cardTags, SHOTS } = loadApp();
    assert.deepEqual([...cardTags([...SHOTS, "Energy"])], ["All shots", "Energy"]);
    assert.deepEqual([...cardTags(["3PT", "Steal"])], ["3PT", "Steal"]);
});

test("a card shows the trait name and its tag chips", () => {
    const { card, SHOTS } = loadApp();
    assert.equal(card(trait()).find("name").textContent, "Sharp Drive");
    const chips = card(trait({ tags: [...SHOTS, "Energy"] })).find("tags").children.map(c => c.textContent);
    assert.deepEqual(chips, ["All shots", "Energy"]);
});

test("Found on lists collection names only", () => {
    const { card } = loadApp();
    const cols = card(trait()).find("cols");
    assert.equal(cols.textContent, "Found on: Akashi Collection · Nash");
});

test("Found on highlights the selected collection", () => {
    const app = loadApp();
    app.state.col = "Nash";
    const cols = app.card(trait()).find("cols");
    const marks = cols.children.filter(c => typeof c !== "string" && c.tag === "mark");
    assert.equal(marks.length, 1);
    assert.equal(marks[0].textContent, "Nash");
    assert.equal(cols.textContent, "Found on: Akashi Collection · Nash");
});

test("Found on says None logged yet with no collections", () => {
    const { card } = loadApp();
    assert.equal(card(trait({ collections: [] })).find("cols").textContent, "Found on: None logged yet");
});

test("tiers without numbers or icons show the right placeholder", () => {
    const { card } = loadApp();
    const t = trait({
        tiers: {
            II: { value: "", icon: "images/icons/sharp-drive-ii.webp", seenOn: "" },
            III: { value: "", icon: null, seenOn: "" },
        },
    });
    const text = card(t).textContent;
    assert.match(text, /Numbers not logged/);
    assert.match(text, /Not seen yet/);
});

test("a summary effect is labelled as not seen in game", () => {
    const { card } = loadApp();
    assert.match(card(trait({ effectSource: "" })).textContent, /Summary\. Not seen in game yet/);
    assert.match(card(trait()).textContent, /In-game text, Tier III/);
});

test("every real trait renders without undefined or null text", () => {
    // Catches the code and data drifting apart, like the "(undefined)" bug after #41.
    const { card } = loadApp();
    for (const t of DATA.traits) {
        const c = card(t);
        // Check each text node on its own: joined text like "Tier IIundefined"
        // has no word boundary before "undefined".
        const bad = /\bundefined\b|\bnull\b|\[object /;
        for (const s of c.texts()) assert.doesNotMatch(s, bad, `${t.id} text: ${s}`);
        for (const v of c.allAttrs()) assert.doesNotMatch(v, bad, `${t.id} attribute: ${v}`);
    }
});

test("app.js uses no HTML-string sinks blocked by Trusted Types", () => {
    const banned = /\.innerHTML|\.outerHTML|insertAdjacentHTML|document\.write|\beval\(|new Function\(|setTimeout\(\s*["'`]|srcdoc|createContextualFragment|DOMParser/;
    assert.doesNotMatch(APP, banned);
});
