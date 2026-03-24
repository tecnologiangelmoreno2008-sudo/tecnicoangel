/*
let numero1 = prompt("ingrese el primer numero");


let numero2 = prompt("ingrese el segundo  numero");


numero1 = parseFloat(numero1);
numero2 = parseFloat(numero2);


alert(numero1 + numero2);
*/

/*
let usuario = prompt("nombre de usuario")
let password = prompt("Ingrese su contraseña");
let role = prompt("Ingrese su rol ( Administrador, editor,Invitado):")

if (role === "administrador") {
  alert("Bienvenido, " + user + ". Tienes aceceso completo.");
} else if (role === "Editor") {
  alert("Bienvenido, " + user + ". Puiedes editar contenido.");
} else {
  alert("Bienvenido, " + user + ". Tienes aceceso limitado.");
}
  */
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