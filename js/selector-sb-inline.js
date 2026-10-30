(function () {
'use strict';
const BASE = 'https://nzpujmlienzfetqcgsxz.supabase.co/rest/v1/';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56cHVqbWxpZW56ZmV0cWNnc3h6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2ODYzMzYsImV4cCI6MjA5MDI2MjMzNn0.xl3lsb-KYj5tVLKTnzpbsdEGoV9ySnswH4eyRuyEH1s';
const headers = {apikey: KEY, Authorization: 'Bearer ' + KEY, 'Content-Type':'application/json'};
const eid = '68dcc77f-e02d-4bea-beac-6a95f66ae539';
const sid = crypto.randomUUID();
const names = new Set(photos.map(p => p.name));
const clone = v => JSON.parse(JSON.stringify(v));
let list = Number(localStorage.getItem('evelyn_active_list') || '1');
let previous = {};
let engine;
const engines = {};
const labels = {0: 'Selección anterior', 1: 'Lista enviada'};
const status = document.getElementById('saveStatus');
function showCount(index, data) {
    const count = Object.values(data).filter(v => v.categories?.some(c => c !== 'descartada')).length;
    document.querySelector('[data-list="' + index + '"]').textContent = 'Ver ' + labels[index].toLowerCase() + ' · ' + count + ' fotos';
}
function clean(data) {
    return Object.fromEntries(Object.entries(data || {}).filter(([k,v]) => names.has(k) && v && Array.isArray(v.categories)));
}
async function request(url, options = {}) {
    const r = await fetch(BASE + url, {...options, headers:{...headers,...options.headers}, cache:'no-store'});
    if (!r.ok) throw new Error('No se pudo guardar: ' + r.status);
    return r.status === 204 || options.method === 'POST' ? null : r.json();
}
async function row(index) {
    return (await request('selecciones?evento_id=eq.' + eid + '&foto_index=eq.' + index + '&select=datos&limit=1'))[0]?.datos || {};
}
function useList(index) {
    list = index; localStorage.setItem('evelyn_active_list', String(index));
    activeFilter = 'selected';
    document.querySelectorAll('.btn-filter').forEach(b => b.classList.toggle('active', b.dataset.filter === 'selected'));
    document.querySelectorAll('[data-list]').forEach(b => b.classList.toggle('active', Number(b.dataset.list) === index));
    document.getElementById('currentList').textContent = labels[index];
    selections = clean(JSON.parse(localStorage.getItem('xv_evelyn_list_' + index) || '{}'));
    previous = clone(selections); renderGallery(); updateStats();
    if (!engines[index]) engines[index] = createSelectionSync({
        key: 'xv_evelyn_list_' + index,
        status: text => { if (list === index) status.textContent = text; },
        read: async () => clean(await row(index)),
        write: async batch => {
            const remote = await row(index);
            const data = clean(remote);
            Object.entries(batch).forEach(([name, change]) => {
                if (change.value === null) delete data[name]; else data[name] = change.value;
            });
            const revision = crypto.randomUUID();
            data._sync = {clock: Number(remote._sync?.clock || 0) + 1, sid, revision,
                listName:labels[index], updatedAt:new Date().toISOString()};
            await request('selecciones?on_conflict=evento_id,foto_index', {
                method:'POST', headers:{Prefer:'resolution=merge-duplicates,return=minimal'},
                body: JSON.stringify([{evento_id:eid, session_id:sid, foto_index:index,
                    impresion:false, ampliacion:false, invitacion:false, descartada:false,
                    datos:data, code_version:6}])
            });
            const saved = await row(index);
            if (saved._sync?.revision !== revision) throw new Error('Cambio sin confirmar; se reintentará');
        },
        apply: data => {
            showCount(index, data);
            localStorage.setItem('xv_evelyn_list_' + index, JSON.stringify(data));
            if (list !== index) return;
            const changed = JSON.stringify(selections) !== JSON.stringify(data);
            selections = data; previous = clone(data);
            if (changed) { renderGallery(); updateStats(); }
        }
    });
    engine = engines[index]; engine.refresh();
}
window.saveEvelynSelections = function () {
    const data = clean(selections);
    showCount(list, data);
    localStorage.setItem('xv_evelyn_list_' + list, JSON.stringify(data));
    for (const name of new Set([...Object.keys(previous), ...Object.keys(data)])) {
        if (JSON.stringify(previous[name]) !== JSON.stringify(data[name])) engine.change(name, data[name] || null);
    }
    previous = clone(data);
};
// Preserve the legacy browser snapshot for recovery, never merge it into both lists.
if (!localStorage.getItem('xv_evelyn_respaldo'))
    localStorage.setItem('xv_evelyn_respaldo', localStorage.getItem('xv_evelyn') || '{}');
document.querySelectorAll('[data-list]').forEach(b => b.addEventListener('click', () => { closeModal(); useList(Number(b.dataset.list)); }));
useList(list === 0 ? 0 : 1);
const otherList = list === 0 ? 1 : 0;
row(otherList).then(data => showCount(otherList, clean(data))).catch(() => {});
setInterval(() => { for (const e of Object.values(engines)) e.refresh(); }, 15000);
window.addEventListener('online', () => { for (const e of Object.values(engines)) e.refresh(); });
document.addEventListener('visibilitychange', () => { if (!document.hidden) engine.refresh(); });
})();
