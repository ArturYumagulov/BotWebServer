(function() {

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
        const [report_2, categoriesResponse] = await Promise.all([
            fetch(report_2_url, {
                method: 'POST',
                headers: {"X-CSRFToken": csrf},
                body: JSON.stringify({
                    "depart": depart,
                    "user_id": user_id
                })
            }),
            // fetch('/categories')
        ]);
        const report_2_data = await report_2.json();
        // const categories = await categoriesResponse.json();
        return report_2_data;
    }

    async function createTable(table) {
        if (depart === 'director') {
            create_director_buttons()


            let buttons = document.querySelectorAll('.btn')
            let main = document.getElementById('main')
            let div = document.getElementById('buttons')
            console.log(buttons)
            buttons.forEach((button) => {
                button.addEventListener('click', ()=>{
                    div.style.position = 'relative'
                    div.style.top = '0'
                    div.style.left = '0'

                    if (button.id === 'b2c') {
                        create_head(table_column_list, table)
                    }

                })
            })


        } else {
            await create_head(table_column_list, table)

            LoadData(depart).then((report_data) => {
                let data = report_data.data
                let tbody = document.createElement('tbody')
                data.forEach((dt) => {
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
            });
        }
    }

    window.createTable = createTable;
})();






