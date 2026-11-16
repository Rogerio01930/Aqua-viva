# Áqua Viva

Sistema desktop desenvolvido em Python com interface gráfica em Tkinter para o registro, acompanhamento e gestão de ocorrências relacionadas ao saneamento básico e à preservação dos recursos hídricos.

## Sobre o Projeto e o Problema Resolvido

Vazamentos de água potável, esgoto a céu aberto, acúmulo de água parada e falta de abastecimento são problemas urbanos que impactam diretamente a saúde pública e o meio ambiente. Na maioria das vezes, a comunicação entre os moradores e os órgãos públicos responsáveis pelos reparos é demorada e carece de acompanhamento transparente.

O **Áqua Viva** atua como uma ponte direta entre a população e a gestão municipal, permitindo que cidadãos registrem ocorrências com localização, descrição e foto, enquanto a prefeitura acompanha os chamados e atualiza a situação de cada atendimento.

## Objetivo do Sistema

Facilitar a fiscalização colaborativa e agilizar a comunicação entre cidadãos e gestores públicos no combate ao desperdício de água e falhas na rede de saneamento.

## Principais Funcionalidades Implementadas

- **Acesso por Perfil:** Login diferenciado para cidadãos (`usuario`) e gestores públicos (`prefeitura`).
- **Registro de Denúncias:** Formulário para envio de ocorrências contendo endereço/local, categoria do problema, anexo de imagem e descrição detalhada.
- **Feed de Ocorrências e Filtros:** Listagem geral das denúncias registradas com filtro por tipo (Vazamento de água, Esgoto a céu aberto, Água parada e Falta de água).
- **Painel de Gestão (Prefeitura):** Visualização completa dos relatos recebidos com botões para atualizar o status entre *Pendente*, *Em análise* e *Resolvido*.
- **Meu Perfil e Minhas Denúncias:** Área dedicada para alteração do nome de exibição, consulta de resumo geral e gerenciamento (edição de descrição e exclusão) das denúncias criadas pelo próprio usuário.

## Tecnologias Utilizadas

- **Python 3**
- **Tkinter** (construção das janelas, formulários e componentes visuais)
- **OS** (manipulação de caminhos e nomes de arquivos de imagem anexados)

## Instruções para Instalação e Execução

Como o sistema utiliza apenas bibliotecas nativas do próprio Python, não é necessária a instalação de pacotes externos.

1. Certifique-se de ter o **Python 3** instalado em seu computador.
