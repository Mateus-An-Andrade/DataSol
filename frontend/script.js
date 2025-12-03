function open_menu(id_btn,id_menu, displayType = "grid"){
    const button_menu = document.getElementById(id_btn)
    const menu_in_work = document.getElementById(id_menu)
    const main_menu = document.getElementById("nav_principal_menu")

    button_menu.addEventListener("click",function(){
        menu_in_work.style.display = displayType
        main_menu.style.display = "none"
    })

}

function open_inner_option(id_btn,id_menu, displayType = "grid"){
    const button_menu = document.getElementById(id_btn)
    const menu_in_work = document.getElementById(id_menu)

    button_menu.addEventListener("click",function(){
        menu_in_work.style.display = displayType
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

function opacity_btns(class_btn,id_menu){
    const btn_in_use = document.querySelectorAll(`#${id_menu} .${class_btn}`)

    btn_in_use.forEach(btn=>{
        btn.addEventListener("click", function(){
            btn_in_use.forEach(btn_out_use => {
                if(btn_out_use !== btn){
                    btn_out_use.style.opacity = "0.5"
                }else{
                    btn_out_use.style.opacity = "1"
                }
            });
        })
    })
}

document.addEventListener("DOMContentLoaded", function () {

//==================================================================================================================================================
    {open_menu("data_prod_cons_btn","production_and_consumption_menu", "grid")
        opacity_btns("btn_prod_consump_container", "conteiner_production")
        open_inner_option("potential_btn_prod_energ", "conteiner_data_analysis_consup_prod", "grid")
        open_inner_option("util_btn_prod_energ", "conteiner_data_analysis_consup_prod", "grid")
        open_inner_option("total_btn_prod_energ", "conteiner_data_analysis_consup_prod", "grid")

        open_inner_option("consumption_total_btn_energ_data", "conteiner_data_analysis_consup_prod", "grid")
        open_inner_option("consumpt_for_sectors_btn_energ_data", "conteiner_data_analysis_consup_prod", "grid")
        open_inner_option("consumpt_for_resident_btn_energ_data", "conteiner_data_analysis_consup_prod", "grid")

                                                                                                //Acima estão as funçoes do menu "Consumo e Produção", as funções somente abrem e escondem interfaces
    }
//==================================================================================================================================================
    open_menu("data_reports_btn","reports_menu", "block")
        {open_inner_option("btn_reports_for_sectors","continer_graphics_and_sectors_reports", "grid")
            open_inner_option("alfa_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("bravo_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("charlie_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("delta_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("echo_sector_graph", "continer_graphics_reports", "grid")}

        {open_inner_option("btn_reports_for_pannels", "continer_graphics_and_sectors_reports", "grid")
            open_inner_option("alfa_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("bravo_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("charlie_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("delta_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("echo_sector_graph", "continer_graphics_reports", "grid")}

        {open_inner_option("btn_reports_for_sectors_consumption", "continer_graphics_and_sectors_reports", "grid")
            open_inner_option("alfa_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("bravo_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("charlie_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("delta_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("echo_sector_graph", "continer_graphics_reports", "grid")}

        {open_inner_option("btn_reports_for_individuals_consumption", "continer_graphics_and_sectors_reports", "grid")
            open_inner_option("alfa_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("bravo_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("charlie_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("delta_sector_graph", "continer_graphics_reports", "grid")
            open_inner_option("echo_sector_graph", "continer_graphics_reports", "grid")}

    open_menu("data_panels_btn","panels_menu", "flex")
    open_menu("management_energ_btn","energetic_management", "block")

    close_menu("production_and_consumption_menu")
    close_menu("reports_menu")
    close_menu("panels_menu")
    close_menu("energetic_management")
})
