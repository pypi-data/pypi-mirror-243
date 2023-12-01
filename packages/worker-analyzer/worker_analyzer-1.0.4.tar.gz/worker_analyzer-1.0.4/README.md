
# WorkerAnalyzer

## Descrição

WorkerAnalyzer é uma biblioteca Python projetada para monitoramento e análise detalhada de execuções de código, com foco em pipelines de dados e processos automatizados. Ela permite aos desenvolvedores registrar, analisar e reportar métricas de execução, facilitando a identificação de problemas de desempenho e eficiência.

## Componentes Principais
A biblioteca é segmentada em algumas partes, cada uma focada em uma funcionalidade específica:
- **Analyzers:** Inclui classes fundamentais para monitorar sessões de execução, como Session, Task, e SubTask.
- **Builders**: Composto por classes auxiliares (DefaultMetricsBuilder e SimpleMetricsBuilder) para construir e gerenciar métricas de monitoramento de forma eficiente.
- **Report**: Inclui a classe DefaultReport para gerar insights detalhados e relatórios a partir dos dados coletados.
- **Storage**: Contém implementações para armazenamento de dados, como a classe LocalStorage, que lida com o armazenamento local.

## Definições de Sessão, Task e Subtask
- **Session**: Representa uma execução completa de um processo ou pipeline. Mantém um registro de várias Tasks e oferece funcionalidades para iniciar, encerrar e gerenciar atributos personalizados da sessão.
- **Task**: Corresponde a uma tarefa específica dentro de uma Session. Pode conter múltiplas SubTasks e fornece métodos para rastrear seu progresso e status.
- **SubTask**: Representa uma operação mais granular dentro de uma Task, permitindo um monitoramento mais detalhado de partes específicas de uma tarefa.

Uma forma de compreender melhor, em um processo de um pipeline no Airflow, podemos compreender como:
- DAG == Session
- Taks == Task
- Request == Subtask

## Métricas geradas
A lib foi projetada para gerar métricas padrões de tempo e status por atividade, mas permite o input de métricas personalizadas de acordo com a necessidade do projeto atual.
### Métricas Padrões:
* Start Time
* End Time
* Duration
* Status

### Métricas Personalizaveis
* Quantidade de Requests API
* Quantidade de Sucesso
* Quantidade Falha
* Quantidade de Linhas Transacionadas
* Detalhe dos erros

## Uso Geral da Biblioteca
A biblioteca WorkerAnalyzer é projetada para ser integrada em qualquer código Python, especialmente em contextos onde a monitorização detalhada do desempenho e da execução é crucial. Ela é ideal para pipelines de dados, processos automatizados, e sistemas de ETL, onde cada etapa ou tarefa precisa ser cuidadosamente monitorada e analisada.

## Configuração e Personalização
Configuração Inicial: A biblioteca pode ser configurada para atender a requisitos específicos, como definir caminhos de armazenamento personalizados ou integrar com sistemas de alerta.
Personalização: As classes de Builders e Report oferecem flexibilidade para definir métricas personalizadas e formatos de relatórios, adaptando-se a diferentes necessidades de monitoramento.



## Get Started


## Instalação
```bash
pip install worker_analyzer
```


## Uso Básico


### Iniciando uma Sessão

```python
from worker_analyzer.analyzer import Session
# Instance
session = Session()

# Add attributes
session.add_attribute(key="dag_id", value="dag_teste_gooru")
session.add_attribute(key="target", value="api-gooru")
session.add_attribute(key="client", value="gooru")

# Start
session.start()

```
```json
// Session Return
{
    "id":"6c77d295-bb8d-4272-99f3-eecec385af70",
    "start_time": "2023-11-20T18:05:50.609013",
    "end_time": "",
    "duration": 0,
    "status": "In Progress",
    "custom_attributes": {
        "dag_id": "dag_teste_gooru",
        "target": "api-gooru",
        "client": "gooru"
    }
}
```

### Trabalhando com Tarefas e Subtarefas

```python
from worker_analyzer.analyzer import Task, SubTask

task = Task('Nome da Tarefa')
task.start()

subtaks_a = SubTask(name='Nome da Subtarefa A', subtask_type='Tipo')
subtaks_a.start()
# Processamento da subtarefa
subtaks_a.end(status="success")

subtaks_b = SubTask(name='Nome da Subtarefa B', subtask_type='Tipo')
subtaks_b.start()
# Processamento da subtarefa
subtaks_b.end(status="success")

# Adicionar Subtask na Task
task.add_subtask(subtask_a.subtask)
task.add_subtask(subtask_b.subtask)

task.end()
taks.taks
```
```json
// Return Task
{   "id": "d8e9f610-0287-475f-9e6c-e53ea11e9b2f",
    "name": "Nome da Tarefa",
    "start_time": "2023-11-20T18:05:50.609013",
    "end_time": "2023-11-20T18:05:50.611697",
    "duration": 0.002684,
    "status": "success",
    "subtasks": [
        {
            "id": "aa24ab76-d76c-4a43-99f6-58020b3aa5a0",
            "name": "Nome da Subtarefa A",
            "subtask_type": "Tipo",
            "start_time": "2023-11-20T18:05:50.609013",
            "end_time": "2023-11-20T18:05:50.610603",
            "duration": 0.00159,
            "status": "success",
            "metrics": []
        },
        {
            "id": "aa24ab76-d76c-4a43-99f6-58020b3aa5a0",
            "name": "Nome da Subtarefa B",
            "subtask_type": "Tipo",
            "start_time": "2023-11-20T18:05:50.609013",
            "end_time": "2023-11-20T18:05:50.610603",
            "duration": 0.00159,
            "status": "success",
            "metrics": []
        }
    ]
}
```

### Adicionando Resultados da Task na Sessão
```python
from worker_analyzer.analyzer import Session, Task, Subtask
# Instance
session = Session()

# Add attributes
session.add_attribute(key="dag_id", value="dag_teste_gooru")
session.add_attribute(key="target", value="api-gooru")
session.add_attribute(key="client", value="gooru")

# Start
session.start()
task = Task()
# Processamento da Task e Subtask
task.end()
session.add_task(task.task)
session.end()
```
```json
{
    "id":"6c77d295-bb8d-4272-99f3-eecec385af70",
    "start_time": "2023-11-20T18:05:50.609013",
    "end_time": "",
    "duration": 0,
    "status": "In Progress",
    "custom_attributes": {
        "dag_id": "dag_teste_gooru",
        "target": "api-gooru",
        "client": "gooru"
    },
    "tasks": {   
        "id": "d8e9f610-0287-475f-9e6c-e53ea11e9b2f",
        "name": "Nome da Tarefa",
        "start_time": "2023-11-20T18:05:50.609013",
        "end_time": "2023-11-20T18:05:50.611697",
        "duration": 0.002684,
        "status": "success",
        "subtasks": [
            {
                "id": "aa24ab76-d76c-4a43-99f6-58020b3aa5a0",
                "name": "Nome da Subtarefa A",
                "subtask_type": "Tipo",
                "start_time": "2023-11-20T18:05:50.609013",
                "end_time": "2023-11-20T18:05:50.610603",
                "duration": 0.00159,
                "status": "success",
                "metrics": []
            },
            {
                "id": "aa24ab76-d76c-4a43-99f6-58020b3aa5a0",
                "name": "Nome da Subtarefa B",
                "subtask_type": "Tipo",
                "start_time": "2023-11-20T18:05:50.609013",
                "end_time": "2023-11-20T18:05:50.610603",
                "duration": 0.00159,
                "status": "success",
                "metrics": []
            }
        ]
    }
}
```



### Gerando um Relatório
```python
from worker_analyzer import Report

report = Report(session_data)
print(report.generate_report())
```
```json
{
    "Session ID": "6c77d295-bb8d-4272-99f3-eecec385af70", 
    "Start Time": "2023-11-23T07:37:17.600978", 
    "End Time": "2023-11-23T07:37:17.604104", 
    "Duration": 0.003126, 
    "Number of Tasks": 1, 
    "Number of tasks with more than 10% failure": 0, 
    "Number of tasks with more than 50% partial": 0, 
    "Tasks": [
        {
            "task": "e78c4b65-322f-4069-a266-1263a6678678", 
            "status": "success", 
            "count_substasks": 2, 
            "success": "2 (100.00%)", 
            "failure": "0 (0.00%)", 
            "partial": "0 (0.00%)"
        }
    ]
}
```

![Comparation](docs/assets/code_comparation.png)


## Documentação Completa:
**Analyzer:**
- [Session](/docs/sessions.md)
- [Task](/docs/task.md)
- [Subtask](/docs/subtask.md)

**Builders:**
- [Builders](/docs/builders.md)

**Report:**
- [Report](/docs/report.md)

**Storage:**
- [Storage](/docs/storage.md)

## Contribuição

Contribuições para o `worker_analyzer` são bem-vindas! Por favor, leia as diretrizes de contribuição para mais informações.

Veja as issues disponíveis ou sugira novas melhorias.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
