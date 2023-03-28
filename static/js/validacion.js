function validarFormulario() {
    var cedula = document.getElementById("cedula").value;
    if (cedula === "" || isNaN(cedula)) {
        document.getElementById("cedula").classList.add("is-invalid");
        document.getElementById("cedula").focus();
        return false;
    }
    return true;
}


function validarCedula() {
    var cedula = document.getElementById("cedula").value;
    var nombre = document.getElementById("nombre").value;
    var telefono = document.getElementById("telefono").value;
    var direccion = document.getElementById("direccion").value;

    if (cedula === "" || isNaN(cedula)) {
        document.getElementById("cedula").classList.add("is-invalid");
    } else {
        document.getElementById("cedula").classList.remove("is-invalid");
    }

    if (telefono === "" || isNaN(telefono)) {
        document.getElementById("telefono").classList.add("is-invalid");
    } else {
        document.getElementById("telefono").classList.remove("is-invalid");
    }

    if (nombre === "") {
        document.getElementById("nombre").classList.add("is-invalid");
    } else {
        document.getElementById("nombre").classList.remove("is-invalid");
    }

    if (direccion === "") {
        document.getElementById("direccion").classList.add("is-invalid");
    } else {
        document.getElementById("direccion").classList.remove("is-invalid");
    }
}

document.getElementById("cedula").addEventListener("input", validarCedula);
document.getElementById("telefono").addEventListener("input", validarCedula);
document.getElementById("nombre").addEventListener("input", validarCedula);
document.getElementById("direccion").addEventListener("input", validarCedula);