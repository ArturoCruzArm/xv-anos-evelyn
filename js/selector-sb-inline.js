(function () {
'use strict';
const BASE = 'https://nzpujmlienzfetqcgsxz.supabase.co/rest/v1/';
const KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56cHVqbWxpZW56ZmV0cWNnc3h6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2ODYzMzYsImV4cCI6MjA5MDI2MjMzNn0.xl3lsb-KYj5tVLKTnzpbsdEGoV9ySnswH4eyRuyEH1s';
const headers = {apikey:KEY, Authorization:'Bearer ' + KEY, 'Content-Type':'application/json'};
const eid = '68dcc77f-e02d-4bea-beac-6a95f66ae539';
const sid = crypto.randomUUID();
const names = new Set(photos.map(p => p.name));
const clone = v => JSON.parse(JSON.stringify(v));
const data = [{}, {}], engines = [], statuses = ['Cargando…','Cargando…'];
let previous = {};
function clean(raw) {
    return Object.fromEntries(Object.entries(raw || {}).filter(([k,v]) => names.has(k) && Array.isArray(v?.categories) && (v.categories.length || v.notes)));
}
function merged() {
    const out = {};
    for (const name of new Set([...Object.keys(data[0]), ...Object.keys(data[1])])) {
        const before = data[0][name] || {}, now = data[1][name] || {};
        const cats = new Set([...(before.categories || []).map(c => c === 'impresion' ? 'impresion_antes' : c), ...(now.categories || [])]);
        if (cats.size || before.notes || now.notes) out[name] = {categories:[...cats],notes:now.notes || before.notes || ''};
    }
    return out;
}
function paint() {
    const next = merged();
    const changed = JSON.stringify(next) !== JSON.stringify(selections);
    selections = next; previous = clone(next);
    if (changed) { renderGallery(); updateStats(); }
}
function status(index, message) {
    statuses[index] = message;
    const pending = statuses.find(s => /Pendiente|pendientes/.test(s));
    document.getElementById('saveStatus').textContent = pending || (statuses.every(s => s.includes('nube ✓')) ? 'Guardado en la nube ✓' : 'Cargando o guardando selecciones…');
}
async function request(url, options = {}) {
    const response = await fetch(BASE + url, {...options,headers:{...headers,...options.headers},cache:'no-store'});
    if (!response.ok) throw new Error('Respuesta ' + response.status);
    return options.method === 'POST' ? null : response.json();
}
async function row(index) {
    return (await request('selecciones?evento_id=eq.' + eid + '&foto_index=eq.' + index + '&select=datos&limit=1'))[0]?.datos || {};
}
for (const index of [0,1]) {
    data[index] = clean(JSON.parse(localStorage.getItem('xv_evelyn_list_' + index) || '{}'));
    engines[index] = createSelectionSync({
        key:'xv_evelyn_list_' + index,
        status:message => status(index,message),
        read:async () => clean(await row(index)),
        write:async batch => {
            const remote = await row(index), snapshot = clean(remote), revision = crypto.randomUUID();
            Object.entries(batch).forEach(([name,change]) => {if(change.value === null)delete snapshot[name];else snapshot[name]=change.value;});
            snapshot._sync = {clock:Number(remote._sync?.clock || 0)+1,sid,revision,listName:index === 0 ? 'Impresión antes' : 'Impresión ahora',updatedAt:new Date().toISOString()};
            await request('selecciones?on_conflict=evento_id,foto_index',{method:'POST',headers:{Prefer:'resolution=merge-duplicates,return=minimal'},
                body:JSON.stringify([{evento_id:eid,session_id:sid,foto_index:index,impresion:false,ampliacion:false,invitacion:false,descartada:false,datos:snapshot,code_version:6}])});
            if ((await row(index))._sync?.revision !== revision) throw new Error('Guardado no confirmado');
        },
        apply:remote => {data[index]=remote;localStorage.setItem('xv_evelyn_list_' + index,JSON.stringify(remote));paint();}
    });
}
window.saveEvelynSelections = function () {
    const current = clean(selections);
    for (const name of new Set([...Object.keys(previous),...Object.keys(current)])) {
        if (JSON.stringify(previous[name]) === JSON.stringify(current[name])) continue;
        const sel = current[name] || {categories:[],notes:''};
        const before = sel.categories.includes('impresion_antes') ? {categories:['impresion'],notes:''} : null;
        const now = {categories:sel.categories.filter(c => c !== 'impresion_antes'),notes:sel.notes || ''};
        const desired = [before,now.categories.length || now.notes ? now : null];
        desired.forEach((value,index) => {
            if (JSON.stringify(data[index][name] || null) === JSON.stringify(value)) return;
            if (value === null) delete data[index][name]; else data[index][name]=clone(value);
            localStorage.setItem('xv_evelyn_list_' + index,JSON.stringify(data[index]));
            engines[index].change(name,value);
        });
    }
    previous=clone(current);
};
paint();
engines.forEach(e=>e.refresh());
setInterval(()=>engines.forEach(e=>e.refresh()),15000);
window.addEventListener('online',()=>engines.forEach(e=>e.refresh()));
document.addEventListener('visibilitychange',()=>{if(!document.hidden)engines.forEach(e=>e.refresh())});
})();
