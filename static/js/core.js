var eliminando;
function cambiarRuta(ruta) {
    let frm = document.getElementById("formulario");
    frm.action = ruta;
    eliminando = false;
    if (ruta == "/vuelos/delete" || ruta2 == "/usuario/dashboard"){
        eliminando =  true;
    }
}

function cambiarRuta2(ruta2) {
    let frm2 = document.getElementById("formulario2")
    frm2.action = ruta2
    eliminando = false;
    if (ruta == "/vuelos/delete" || ruta2 == "/usuario/dashboard"){
        eliminando =  true;
    }
}

function confirmarBorrado() {
    if (eliminando){
        let resp = confirm("Desea realmente borrar el registro?")
        return resp;
    }
    return true;
}
