(function() {
    let loader = document.querySelector('.loader')
    let head_load = document.getElementById('head-load')
    let footer_load = document.getElementById('footer-load')

    async function create_director_buttons() {
        let main = document.getElementById('main')
        let div = document.createElement('div')
        let b2c_but = document.createElement("button")
        let b2b_but = document.createElement("button")
        let industrial_but = document.createElement("button")

        div.id = 'buttons'
        window.addEventListener('resize', () => {

            if (window.innerWidth < 468) {
                div.classList.remove('position-absolute', 'top-50', 'start-50')
                div.classList.add('w-100')
            }

        })
        b2b_but.classList.add('btn', 'btn-outline-secondary', 'me-1', 'mb-1')
        b2c_but.classList.add('btn', 'btn-outline-secondary', 'me-1', 'mb-1')
        industrial_but.classList.add('btn', 'btn-outline-secondary', 'me-1', 'mb-1')

        b2b_but.setAttribute('id', 'b2b')
        b2c_but.setAttribute('id', 'b2c')
        industrial_but.setAttribute('id', 'industrial')

        b2c_but.innerHTML = 'B2C'
        b2b_but.innerHTML = 'B2B'
        industrial_but.innerHTML = 'Industrial'
        div.append(b2c_but, b2b_but, industrial_but)
        main.append(div)
    }

    async function create_head(table_column_list, table) {
        let thead = document.createElement('thead')
        let tr = document.createElement('tr')
        table_column_list.forEach((column) => {
            let th = document.createElement('th')
            th.setAttribute('scope', 'col')
            th.innerHTML = column.name
            th.style.textAlign = 'center'
            th.style.fontSize = '13px'
            tr.append(th)
        })
        thead.append(tr)
        table.append(thead)
    }

    async function LoadData(depart) {
        const [report_2] = await Promise.all([
            fetch(report_2_url, {
                method: 'POST',
                headers: {"X-CSRFToken": csrf},
                body: JSON.stringify({
                    "depart": depart,
                    "user_id": user_id
                })
            }),
        ]);
        return await report_2.json();
    }

    async function create_director_report_2(depart, table) {
        LoadData(depart).then((report_data) => {
            let data = report_data.data
            let tbody = document.createElement('tbody')
            if (data.length === 0) {
                console.log(data)
                table.innerHTML = '<p class="text-center text-secondary m-5">Нет данных</p>'
            } else {
                create_head(table_column_list, table)
                data.forEach((dt) => {
                    console.log(dt)
                    let tr = document.createElement('tr')
                    for (let i = 0; i < table_column_list.length; i++) {
                        let th = document.createElement('td')
                        th.innerHTML = dt[table_column_list[i].id]
                        th.style.textAlign = 'center'
                        tr.append(th)
                    }
                    tbody.append(tr)
                })
                table.append(tbody)
            }

        }).finally(()=> {
            if (depart.length >= 0) {
                head_load.style.height = '0'
                footer_load.style.height = '0'
                loader.style.display = 'none'
            }
        })
    }

    async function createTable(table) {
        console.log(depart)
        if (depart === 'director') {
            loader.style.display = 'none'
            await create_director_buttons()
            let buttons = document.querySelectorAll('.btn')
            let div = document.getElementById('buttons')
            buttons.forEach((button) => {
                button.addEventListener('click', ()=>{
                    loader.style.display = 'block'
                    table.innerHTML = ''
                    div.style.position = 'relative'
                    div.style.top = '0'
                    div.style.left = '0'
                    if (button.id === 'b2c') {
                        create_director_report_2(button.id, table)
                    }  else if (button.id === 'b2b') {
                        create_director_report_2(button.id, table)
                    }  else if (button.id === 'industrial') {
                        create_director_report_2(button.id, table)
                    }
                })
            })
        } else {
            await create_director_report_2(depart, table)
        }
    }

    window.createTable = createTable;
})();






