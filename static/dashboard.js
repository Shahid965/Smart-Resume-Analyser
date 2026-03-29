let currentRole = 'jobseeker';

function setRole(r) {
    currentRole = r;
    document.getElementById('btnJobSeeker').classList.toggle('active', r === 'jobseeker');
    document.getElementById('btnRecruiter').classList.toggle('active', r === 'recruiter');
}

function updateFileName(input) {
    const label = document.getElementById('fileLabel');
    if (input.files[0]) {
        label.innerText = "√ " + input.files[0].name.toUpperCase();
        label.classList.add('text-emerald-600');
    }
}

function toggleChat() {
    const modal = document.getElementById('chatModal');
    modal.classList.toggle('hidden');
    if(!modal.classList.contains('hidden')) modal.classList.add('flex');
}

async function analyze() {
    const file = document.getElementById('resumeFile').files[0];
    const btn = document.getElementById('btn');
    if (!file) return alert("Please select your CV.");

    btn.innerText = "SCANNING...";
    btn.disabled = true;

    const fd = new FormData();
    fd.append('resume', file);
    fd.append('jd', document.getElementById('jd').value);
    fd.append('role', currentRole);

    try {
        const res = await fetch('/analyze', { method: 'POST', body: fd });
        const data = await res.json();

        // --- THE CINEMATIC SHIFT ---
        const wrapper = document.getElementById('layoutWrapper');
        const results = document.getElementById('resultsArea');
        
        // 1. Move the console to the left sidebar
        wrapper.classList.remove('state-centered');
        wrapper.classList.add('state-dashboard');

        // 2. Wait for the slide animation (1s), then reveal results
        setTimeout(() => {
            results.classList.add('visible');
            
            // Populate Data with staggered logic
            document.getElementById('pName').innerText = data.profile.name;
            document.getElementById('pInitial').innerText = data.profile.name[0];
            document.getElementById('pPhoneText').innerText = `ENCRYPTED ID: ${data.profile.phone}`;
            document.getElementById('pEmailBtn').href = `https://mail.google.com/mail/?view=cm&fs=1&to=${data.profile.email}`;
            document.getElementById('pPhoneBtn').href = `tel:${data.profile.phone}`;

            document.getElementById('score').innerText = data.score + "%";
            document.getElementById('rating').innerText = data.rating;

            document.getElementById('roleList').innerHTML = (data.ai.suggested_roles || []).map(r => 
                `<div class="bg-indigo-600 text-white p-3 rounded-2xl text-[10px] font-black shadow-lg">🎯 ${r}</div>`
            ).join('');
            document.getElementById('pathwayList').innerHTML = (data.ai.career_pathways || []).map(p => 
                `<div class="bg-emerald-500 text-white p-3 rounded-2xl text-[10px] font-black shadow-lg">🚀 ${p}</div>`
            ).join('');

            const expCont = document.getElementById('experienceTimeline');
            expCont.innerHTML = (data.ai.experience_summary || []).map(exp => `
                <div class="relative pl-8 pb-4">
                    <div class="absolute -left-1.5 top-0 h-3 w-3 rounded-full bg-white ring-4 ring-indigo-400"></div>
                    <p class="text-xs font-bold text-indigo-50">${exp}</p>
                </div>
            `).join('');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 1000);

    } catch (err) {
        alert("Strategic error. Check API configuration.");
    } finally {
        btn.innerText = "INITIALIZE SCAN";
        btn.disabled = false;
    }
}

async function sendChat() {
    const inp = document.getElementById('chatInput');
    const win = document.getElementById('chatWindow');
    if (!inp.value) return;
    const msg = inp.value;
    win.innerHTML += `<div class="text-right mb-4"><span class="bg-indigo-600 text-white px-5 py-3 rounded-3xl inline-block shadow-lg font-bold">${msg}</span></div>`;
    inp.value = "";
    const res = await fetch('/chat', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({message:msg}) });
    const d = await res.json();
    win.innerHTML += `<div class="text-left mb-4"><span class="bg-white px-5 py-3 rounded-3xl inline-block text-slate-800 font-bold shadow-sm">${d.reply}</span></div>`;
    win.scrollTop = win.scrollHeight;
}