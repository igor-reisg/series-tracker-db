# Sistema de Acompanhamento e Avaliação de Séries de TV

Projeto final da disciplina de **Banco de Dados I** — UNESP/FC

O repositório contém a documentação em LaTeX da modelagem **conceitual**, **lógica** e
**física** de um banco de dados relacional para uma rede social de acompanhamento e
avaliação de séries de televisão.

## O minimundo

O sistema não exibe conteúdo audiovisual: ele registra e organiza o que as pessoas
assistem e o que elas acham do que assistiram — algo como Letterboxd ou Goodreads,
transposto para o formato seriado. O domínio se organiza em três pilares:

- **Acervo** — séries, divididas em temporadas, divididas em episódios; classificadas
  por gêneros e com a participação de pessoas do meio audiovisual (ator, diretor,
  roteirista, criador).
- **Acompanhamento** — a relação entre usuário e obra, em duas faces: a *intenção
  declarada* (watchlist, assistindo, abandonada) e o *histórico efetivo* (registro de
  exibição episódio a episódio, com data).
- **Social** — seguir outros usuários, curtir avaliações alheias e comentar nelas,
  inclusive respondendo a outros comentários.

Uma **avaliação** (nota de 0,5 a 5,0 e/ou texto) incide sobre exatamente um alvo: uma
série, uma temporada ou um episódio. Como o ato de avaliar é idêntico nos três casos,
o modelo o trata como um conceito único especializado em três formas.

O modelo possui **11 conjuntos de entidades**, **24 regras de negócio** (RN01–RN24) e
resulta em **17 tabelas** no esquema físico.

## Requisitos da disciplina

Enunciado da atividade (entrega de 16/09, via Classroom):

| Requisito | Situação |
| --- | --- |
| Grupo de 4 pessoas | 4 frentes definidas no apêndice do documento |
| Minimundo definido pelo grupo, com 10 a 15 entidades | 11 entidades |
| **Modelo conceitual** — minimundo, regras de negócio e DER | Texto pronto; falta o DER |
| **Modelo lógico** — diagrama lógico já normalizado, com justificativas | A escrever |
| **Modelo físico** — arquivo `.sql` comentado | A escrever |
| Script `.sql` que crie um novo esquema com o nome do projeto | `CREATE SCHEMA serie_tracker` (previsto, não escrito) |
| Script que crie as tabelas com todas as restrições necessárias | 17 tabelas previstas |
| Carga de dados inicial de exemplo (DML) | A escrever |
| 3 `SELECT`s que exemplifiquem a utilidade no minimundo | Os três já estão enunciados no Cap. 3: ranking de séries por nota média, atividade recente de quem o usuário segue, e séries na watchlist ainda não iniciadas |

Entregável final: **um PDF** com as três partes, acompanhado do **script `.sql`** — que
ainda não existe no repositório. O lugar previsto para ele é `projeto/script.sql`, com o
Capítulo 3 reproduzindo apenas os trechos mais representativos e comentando as decisões.

## Estrutura do repositório

```
projeto/
├── documentacao-bd.tex     # documento principal (fonte única)
├── documentacao-bd.pdf     # PDF gerado, versionado
├── script.sql              # script PostgreSQL (a criar)
├── .latexmkrc              # configuração de build do latexmk
├── diagramas/              # DER e diagrama lógico (brModelo)
├── images/                 # imagens usadas no documento
└── build/                  # artefatos de compilação (ignorado pelo git)
```

## Estado atual

| Capítulo | Conteúdo | Situação |
| --- | --- | --- |
| 1 — Modelagem Conceitual | minimundo, regras de negócio, dicionário de dados, cardinalidades, especialização, agregação, DER | Texto completo; falta desenhar o DER no brModelo |
| 2 — Modelagem Lógica | mapeamento ER→relacional, esquema relacional, dependências funcionais, normalização, diagrama lógico | Esqueleto a ser escrito |
| 3 — Modelagem Física | DDL, restrições de integridade, gatilhos, visões, carga de dados, consultas, rastreabilidade | Esqueleto a ser escrito |

O Capítulo 1 **fixa o vocabulário do projeto**: nomes de entidades, atributos, tabelas e
colunas definidos ali valem para todo o restante do documento e para o script SQL. Se
alguma etapa posterior precisar renomear algo, a alteração deve ser feita *também* no
Capítulo 1 — um esquema físico que não corresponde ao diagrama conceitual torna o
documento internamente contraditório.

## Compilação

Requer uma distribuição LaTeX (TeX Live ou MiKTeX) com `latexmk`.

```bash
cd projeto && latexmk -pdf documentacao-bd.tex
```

O `.latexmkrc` manda os arquivos intermediários (`.aux`, `.log`, `.toc`, …) para
`projeto/build/` — ignorado pelo git — e mantém o PDF final em
`projeto/documentacao-bd.pdf`. Não é preciso configurar nada no editor; quem usa o
LaTeX Workshop no VS Code encontra o alinhamento equivalente em `.vscode/settings.json`.

Para limpar os artefatos de compilação:

```bash
cd projeto && latexmk -C
```

## Orientações e versão de entrega

Antes da entrega, o apêndice traz uma lista de verificação: o script SQL deve rodar do
zero em banco vazio sem erro, toda regra de negócio deve aparecer na tabela de
rastreabilidade, os nomes do DDL devem coincidir com o dicionário de dados, as figuras
dos diagramas devem estar presentes, e o sumário deve ser regenerado (compilar duas
vezes).

## Convenções do esquema

- Tabelas no singular e em minúsculas.
- Chave primária no formato `id_<tabela>`.
- `snake_case` para colunas compostas.
- Objetos criados em um esquema próprio (`serie_tracker`), não em `public`.
- SGBD alvo: PostgreSQL.

