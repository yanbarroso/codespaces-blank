// Define a URL da API dinamicamente com base no ambiente
const currentHost = window.location.hostname;
const isLocalOrGithub = currentHost === "localhost" || currentHost.endsWith("github.dev");

// Usar URLs relativas em localhost/GitHub Dev ou IP do ZimaOS
let API_URL = isLocalOrGithub ? "" : "http://192.168.15.17:80"; 

// 2. Elementos do DOM (Cache para performance)
const el = {
    titulo: document.getElementById('titulo'),
    arquivo: document.getElementById('arquivo'),
    btnUpload: document.getElementById('btnUpload'),
    totalPalavras: document.getElementById('totalPalavras'),
    listaEstante: document.getElementById('listaEstante'),
    topWordsContainer: document.getElementById('topWordsList')
};

// --- FUNÇÕES DE API ---

// Função para buscar e renderizar os cards de estatísticas
async function carregarStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        if (!response.ok) throw new Error("Erro ao buscar stats");
        const stats = await response.json();
        
        // Formata o número (ex: 1250 vira 1.250)
        el.totalPalavras.innerText = stats.vocabulario_unico.toLocaleString('pt-BR');
    } catch (err) {
        console.error("Erro Stats:", err);
    }
}

// Função para buscar o Top 10 palavras mais frequentes
async function carregarTopWords() {
    try {
        const response = await fetch(`${API_URL}/stats/top-words`);
        const words = await response.json();
        
        el.topWordsContainer.innerHTML = words.length > 0 ? "" : "Nenhum dado disponível.";

        words.forEach(item => {
            const badge = document.createElement('div');
            badge.className = 'word-badge';
            badge.innerHTML = `
                <span class="word-text">${item.word}</span>
                <span class="word-count">${item.count}</span>
            `;
            el.topWordsContainer.appendChild(badge);
        });
    } catch (err) {
        console.error("Erro Top Words:", err);
    }
}

// Função para listar as obras processadas
async function carregarEstante() {
    try {
        const response = await fetch(`${API_URL}/estante`);
        const obras = await response.json();
        
        el.listaEstante.innerHTML = obras.map(obra => `
            <li class="obra-item">
                <div class="obra-info">
                    <strong>${obra.titulo}</strong>
                    <span>${obra.total.toLocaleString()} palavras</span>
                </div>
                <small>${new Date(obra.data).toLocaleDateString('pt-BR')}</small>
            </li>
        `).join('');
    } catch (err) {
        console.error("Erro Estante:", err);
    }
}

// Função principal de Upload
async function fazerUpload() {
    const titulo = el.titulo.value;
    const arquivo = el.arquivo.files[0];

    if (!titulo || !arquivo) {
        alert("Ops! Informe um título e escolha um arquivo.");
        return;
    }

    // Feedback visual de carregamento (Loading State)
    el.btnUpload.disabled = true;
    el.btnUpload.innerText = "⏳ Processando no ZimaOS...";

    const formData = new FormData();
    formData.append('titulo', titulo);
    formData.append('arquivo', arquivo);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            // Limpa os campos após sucesso
            el.titulo.value = "";
            el.arquivo.value = "";
            alert("✅ Obra processada com sucesso!");
            
            // Atualiza o dashboard automaticamente
            await atualizarTudo();
        } else {
            const erro = await response.json();
            alert(`Erro: ${erro.detail || "Falha no processamento"}`);
        }
    } catch (err) {
        alert("❌ Erro de conexão com o servidor.");
    } finally {
        el.btnUpload.disabled = false;
        el.btnUpload.innerText = "🚀 Processar Agora";
    }
}

// Função para atualizar todos os componentes da tela
async function atualizarTudo() {
    await Promise.all([
        carregarStats(),
        carregarEstante(),
        carregarTopWords()
    ]);
}

// --- INICIALIZAÇÃO ---
// Dispara as buscas assim que a página carrega
document.addEventListener('DOMContentLoaded', atualizarTudo);