window.onload = function () {
    alert("Bienvenido a Técnico Angeles mas conocido como TecnicoAngel");
}

let edad = prompt("Ingrese su edad");
edad = parseInt(edad);

if (isNaN(edad)) {
    alert("Por favor ingrese un número válido");
} else if (edad >= 18) {
    alert("Eres mayor de edad");
} else {
    alert("Eres menor de edad");
}