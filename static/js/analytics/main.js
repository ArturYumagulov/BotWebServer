function create_director_buttons() {
    let main = document.getElementById('main')
    let div = document.createElement('div')
    let b2c_but = document.createElement("button")
    let b2b_but = document.createElement("button")
    let industrial_but = document.createElement("button")
    let filters = document.getElementById('filters')
    let update = document.getElementById('update')


    filters.style.display = 'none'
    update.style.display = 'none'

    // div.classList.add()
    div.id = 'buttons'
    window.addEventListener('resize', ()=> {

        if (window.innerWidth < 468) {
            div.classList.remove('position-absolute', 'top-50', 'start-50')
            div.classList.add('w-100')
    }

    })
    b2b_but.classList.add('btn', 'btn-outline-secondary', 'me-1')
    b2c_but.classList.add('btn', 'btn-outline-secondary', 'me-1')
    industrial_but.classList.add('btn', 'btn-outline-secondary', 'me-1')

    b2b_but.setAttribute('id', 'b2b')
    b2c_but.setAttribute('id', 'b2c')
    industrial_but.setAttribute('id', 'Industrial')

    b2c_but.innerHTML = 'B2C'
    b2b_but.innerHTML = 'B2B'
    industrial_but.innerHTML = 'Industrial'
    div.append(b2c_but, b2b_but, industrial_but)
    main.append(div)
}