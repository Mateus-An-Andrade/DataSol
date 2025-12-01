function open_menu(id_btn,id_menu, displayType = "grid"){
    const button_menu = document.getElementById(id_btn)
    const menu_in_work = document.getElementById(id_menu)
    const main_menu = document.getElementById("nav_principal_menu")

    button_menu.addEventListener("click",function(){
        menu_in_work.style.display = displayType
        main_menu.style.display = "none"
    })

}

function close_menu(id_menu){
    const icon_close = document.querySelectorAll(".close_windows")
    const menu_in_work = document.getElementById(id_menu)
    const main_menu = document.getElementById("nav_principal_menu")

    icon_close.forEach(icon => {
            icon.addEventListener("click",function(){
                menu_in_work.style.display = "none"
                main_menu.style.display = "grid"
        })
    })
}

document.addEventListener("DOMContentLoaded", function () {
    open_menu("data_prod_cons_btn","production_and_consumption_menu", "grid")
    open_menu("data_reports_btn","reports_menu", "block")
    open_menu("data_panels_btn","panels_menu", "flex")
    open_menu("management_energ_btn","energetic_management", "block")

    close_menu("production_and_consumption_menu")
    close_menu("reports_menu")
    close_menu("panels_menu")
    close_menu("energetic_management")
})
