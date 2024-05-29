let table_div = document.querySelector('.table')

let table_column_list = [
    {'id': 'department', 'name': 'Подразделение', 'filter': true},
    {'id': 'author', 'name': 'Ответственный (Инициатор)', 'filter': true},
    {'id': 'worker', 'name': 'Исполнитель', 'filter': true},
    {'id': 'tasks', 'name': 'Количество задач', 'filter': false},
    {'id': 'ready_task', 'name': 'Выполнено задач', 'filter': false},
    {'id': 'active_task', 'name': 'В работе', 'filter': false},
    {'id': 'active_clients', 'name': 'Действующие торговые точки', 'filter': false},
    {'id': 'potential_clients', 'name': 'Потенциальные торговые точки', 'filter': false},
    {'id': 'contract', 'name': 'Договор', 'filter': false},
    {'id': 'amount_sum', 'name': 'Сумма отгрузки', 'filter': false},
]

function fetchVolume(url) {
   return fetch(url, {
          method: "POST",
          headers: {"X-CSRFToken": csrf},
          body: JSON.stringify({depart: depart}),
      }
  ).then((res) => res.json())
        .then((data) => {
            return data})
}

function create_head(table_column_list) {
    let thead = document.createElement('thead')
    let tr = document.createElement('tr')
    table_column_list.forEach((column) => {
        let th = document.createElement('th')
        th.setAttribute('scope', 'col')
        th.innerHTML = column.name
        tr.append(th)
    })
    thead.append(tr)
    table_div.append(thead)
}

function create_table_row() {

}

create_head(table_column_list)