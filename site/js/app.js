const SHOTS = ["3PT","Mid-Range","Close-Range","Layup","Dunk"];
const TAGS = [...SHOTS,"Steal","Block","Contest","Rebound","Handling","Passing","Speed","Energy"];
// On cards, a trait that boosts every shot type shows one "All shots" chip instead of five.
const cardTags = tags => SHOTS.every(s => tags.includes(s)) ? ["All shots", ...tags.filter(t => !SHOTS.includes(t))] : tags;
const state = { tag: "", col: "", q: "" };
let DATA = null;
const $ = id => document.getElementById(id);
const slugify = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
// Counts filter use as GoatCounter events on the public page; does nothing where the counter isn't loaded.
function track(name, tries = 0) {
  const gc = window.goatcounter;
  if (gc && typeof gc.count === 'function') gc.count({ path: name, title: name, event: true });
  else if (tries < 10) setTimeout(() => track(name, tries + 1), 500);
}
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function readHash() {
  const h = decodeURIComponent(location.hash.slice(1));
  const t = TAGS.find(x => x.toLowerCase().replace(/[^a-z0-9]+/g,'-') === h);
  state.tag = t || "";
}

function buildControls() {
  const tagEl = $("tags");
  ["All", ...TAGS].forEach(t => {
    const b = document.createElement("button");
    b.className = "chip"; b.type = "button"; b.dataset.tag = t === "All" ? "" : t;
    b.innerHTML = `${esc(t)} <span class="n"></span>`;
    b.addEventListener("click", () => {
      state.tag = b.dataset.tag;
      const slug = state.tag.toLowerCase().replace(/[^a-z0-9]+/g,'-');
      history.replaceState(null, "", state.tag ? "#" + slug : location.pathname + location.search);
      track("filter-" + (state.tag ? slugify(state.tag) : "all"));
      render();
    });
    tagEl.appendChild(b);
  });
  const sel = $("col");
  DATA.collections.forEach(c => { const o = document.createElement("option"); o.value = c; o.textContent = c; sel.appendChild(o); });
  sel.addEventListener("change", () => {
    state.col = sel.value;
    track("collection-" + (state.col ? slugify(state.col) : "all"));
    render();
  });
  $("q").addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); render(); });
  window.addEventListener("hashchange", () => { readHash(); render(); });
}

function card(t) {
  const anyIcon = Object.values(t.tiers).some(v => v.icon);
  const vars = ["II","III"].map(tier => {
    const v = t.tiers[tier];
    const img = v.icon ? `<img src="${esc(v.icon)}" alt="${esc(t.name)} tier ${tier} icon" width="64" height="64" loading="lazy">` : `<div class="ph" role="img" aria-label="Tier ${tier} not seen yet"></div>`;
    const val = v.value ? `<div class="val">${esc(v.value)}</div>` : `<div class="none">${v.icon ? "Numbers not logged" : "Not seen yet"}</div>`;
    return `<div class="var">${img}<span class="tier ${tier}">Tier ${tier}</span>${val}</div>`;
  }).join("");
  const cols = t.collections.length
    ? t.collections.map(c => { const s = `${esc(c.name)} (${esc(c.tiers)})`; return c.name === state.col ? `<mark>${s}</mark>` : s; }).join(" · ")
    : "None logged yet";
  return `<article class="card${anyIcon ? "" : " missing"}" id="${esc(t.id)}">
    <div class="top"><span class="cat">${esc(t.category)}</span><div class="tags">${cardTags(t.tags).map(x => `<span class="tag">${esc(x)}</span>`).join("")}</div></div>
    <div class="name">${esc(t.name)}</div>
    <div class="vars">${vars}</div>
    <div class="body">
    <p class="effect">${esc(t.effect)}</p>
    <p class="src">${t.effectSource ? `In-game text, ${esc(t.effectSource)}` : "Summary. Not seen in game yet"}</p>
    ${t.trainingCamp ? `<p class="camp">Training Camp: ${esc(t.trainingCamp)}</p>` : ""}
    </div>
    <p class="cols"><b>Found on:</b> ${cols}</p>
  </article>`;
}

function render() {
  document.querySelectorAll("#tags .chip").forEach(b => {
    const on = b.dataset.tag === state.tag;
    b.setAttribute("aria-pressed", String(on));
    if (on) b.scrollIntoView({ block: "nearest", inline: "nearest" });
  });
  const matchTag = (t, tag) => !tag || t.tags.includes(tag);
  const matchCol = (t, col) => !col || t.collections.some(c => c.name === col);
  const matchQ = t => !state.q || (t.name + " " + t.effect).toLowerCase().includes(state.q);
  const list = DATA.traits.filter(t => matchTag(t, state.tag) && matchCol(t, state.col) && matchQ(t));
  // Counts show how many traits each option would give, with the other filters kept as they are.
  document.querySelectorAll("#tags .chip").forEach(b => {
    const n = DATA.traits.filter(t => matchTag(t, b.dataset.tag) && matchCol(t, state.col) && matchQ(t)).length;
    b.querySelector(".n").textContent = n;
    b.classList.toggle("zero", n === 0);
  });
  [...$("col").options].forEach(o => {
    const n = DATA.traits.filter(t => matchTag(t, state.tag) && matchCol(t, o.value) && matchQ(t)).length;
    o.textContent = `${o.value || "All collections"} (${n})`;
  });
  $("grid").innerHTML = list.map(card).join("");
  $("empty").hidden = list.length > 0;
  $("count").textContent = `${list.length} of ${DATA.traits.length} traits`;
}

fetch("data/traits.json").then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }).then(d => {
  DATA = d;
  $("updated").textContent = `Last updated ${d.updated}.`;
  readHash(); buildControls(); render();
  if (state.tag) track("link-filter-" + slugify(state.tag));
}).catch(() => { $("count").textContent = "Couldn't load the trait list. Refresh the page to try again."; });
