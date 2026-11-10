const formulario = document.getElementById("formulario");
const lista = document.getElementById("lista");
const mensagem = document.getElementById("mensagem");
const campoEstado = document.getElementById("estado");

//Utilizei uma função para carregar os estados pela rota que consulta a API do IBGE
async function carregarEstados() {
    try {
        const resposta = await fetch("/api/estados");
        if (!resposta.ok) throw new Error("Falha ao consultar estados");
        const estados = await resposta.json();
        campoEstado.innerHTML = '<option value="">Selecione</option>';
        estados.forEach(estado => {
            const opcao = document.createElement("option");
            opcao.value = estado.sigla;
            opcao.textContent = `${estado.nome} (${estado.sigla})`;
            campoEstado.appendChild(opcao);
        });
    } catch (erro) {
        campoEstado.innerHTML = '<option value="">Não foi possível carregar</option>';
    }
}


function agruparRegioes(ocorrencias) {
    const contagem = {};
    ocorrencias.forEach(item => {
        const regiao = `${item.municipio} - ${item.estado}`;
        contagem[regiao] = (contagem[regiao] || 0) + 1;
    });
    return Object.entries(contagem).sort((a, b) => b[1] - a[1]);
}


function mostrarOcorrencias(ocorrencias) {
    document.getElementById("total").textContent =
        `Total de registros: ${ocorrencias.length}`;

    const resumo = document.getElementById("resumoRegioes");
    resumo.replaceChildren();
    agruparRegioes(ocorrencias).forEach(([regiao, quantidade]) => {
        const item = document.createElement("span");
        item.className = "regiao";
        item.textContent = `${regiao}: ${quantidade}`;
        resumo.appendChild(item);
    });

    lista.replaceChildren();
    if (ocorrencias.length === 0) {
        lista.textContent = "Ainda não existem relatos registrados.";
        return;
    }

    ocorrencias.forEach(item => {
        const artigo = document.createElement("article");
        artigo.className = "ocorrencia";
        const titulo = document.createElement("h3");
        titulo.textContent = item.tipo;
        const local = document.createElement("p");
        local.textContent = `${item.local} — ${item.municipio}/${item.estado}`;
        const data = document.createElement("p");
        data.textContent = `Data: ${String(item.dataOcorrencia).slice(0, 10)}`;
        const descricao = document.createElement("p");
        descricao.textContent = item.descricao || "Sem descrição adicional.";
        artigo.append(titulo, local, data, descricao);
        lista.appendChild(artigo);
    });
}


async function carregarOcorrencias() {
    try {
        const resposta = await fetch("/api/ocorrencias");
        const dados = await resposta.json();
        if (!resposta.ok) throw new Error(dados.erro || "Falha ao consultar relatos");
        mostrarOcorrencias(dados);
    } catch (erro) {
        lista.textContent = "Não foi possível carregar os relatos. Verifique a aplicação.";
    }
}


formulario.addEventListener("submit", async evento => {
    evento.preventDefault();
    const dados = {
        tipo: document.getElementById("tipo").value,
        local: document.getElementById("local").value,
        municipio: document.getElementById("municipio").value,
        estado: campoEstado.value,
        dataOcorrencia: document.getElementById("dataOcorrencia").value,
        descricao: document.getElementById("descricao").value
    };

    try {
        const resposta = await fetch("/api/ocorrencias", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(dados)
        });
        const resultado = await resposta.json();
        if (!resposta.ok) throw new Error(resultado.erro || "Não foi possível registrar.");
        mensagem.textContent = resultado.mensagem;
        mensagem.style.color = "green";
        formulario.reset();
        await carregarOcorrencias();
    } catch (erro) {
        mensagem.textContent = erro.message;
        mensagem.style.color = "darkred";
    }
});

document.getElementById("atualizar").addEventListener("click", carregarOcorrencias);
carregarEstados();
carregarOcorrencias();
