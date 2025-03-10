// Buscar os dados do ranking via API
async function fetchRanking() {
    const response = await fetch('/ranking');  // Aqui você faz a requisição GET para a rota /ranking
    const data = await response.json();  // A resposta é convertida para JSON

    // Exibir os dados no HTML
    let rankingList = '';
    data.forEach(user => {
        rankingList += `<li>${user.nome}: ${user.total_respostas} respostas, ${user.acertos} acertos</li>`;
    });

    document.getElementById("ranking").innerHTML = rankingList;  // Preenche a lista de ranking no HTML
}

fetch("/questao", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        enunciado: "Qual é a capital do Brasil?",
        resposta_correta: "Brasília"
    })
})
.then(response => response.json())  // Converte a resposta em JSON
.then(data => {
    console.log(data);  // Verifica o conteúdo da resposta
    alert(data.message || data.error);  // Exibe a mensagem ou erro retornado do backend
})
.catch(error => console.error('Erro:', error));
