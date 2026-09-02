let carrito = JSON.parse(localStorage.getItem("natusiembras_carrito") || "[]");

function guardarCarrito() {
    localStorage.setItem("natusiembras_carrito", JSON.stringify(carrito));
    actualizarContador();
}

function actualizarContador() {
    const cantidad = carrito.reduce((sum, item) => sum + item.cantidad, 0);
    const contador = document.getElementById("cart-count");
    if (contador) contador.textContent = cantidad;
}

async function agregarProducto(id) {
    const response = await fetch(`/api/productos/${id}`);
    const producto = await response.json();

    if (producto.error) {
        alert(producto.error);
        return;
    }

    const existente = carrito.find(item => item.id === producto.id);

    if (existente) {
        existente.cantidad += 1;
        existente.subtotal = existente.cantidad * existente.precio;
    } else {
        carrito.push({
            id: producto.id,
            nombre: producto.nombre,
            precio: Number(producto.precio),
            unidad: producto.unidad,
            cantidad: 1,
            subtotal: Number(producto.precio)
        });
    }

    guardarCarrito();
    abrirCarrito();
}

function quitarProducto(id) {
    carrito = carrito.filter(item => item.id !== id);
    guardarCarrito();
    renderCarrito();
}

function cambiarCantidad(id, cantidad) {
    const item = carrito.find(i => i.id === id);
    if (!item) return;

    item.cantidad = Math.max(1, cantidad);
    item.subtotal = item.cantidad * item.precio;

    guardarCarrito();
    renderCarrito();
}

function renderCarrito() {
    const contenedor = document.getElementById("cart-items");
    const totalEl = document.getElementById("cart-total");

    if (!contenedor || !totalEl) return;

    if (carrito.length === 0) {
        contenedor.innerHTML = "<p>No tienes productos en el pedido.</p>";
        totalEl.textContent = "0.00";
        return;
    }

    contenedor.innerHTML = carrito.map(item => `
        <div class="cart-row">
            <div>
                <strong>${item.nombre}</strong><br>
                <small>$${item.precio.toFixed(2)} / ${item.unidad}</small>
            </div>
            <div>
                <input type="number" min="1" value="${item.cantidad}"
                    style="width:55px"
                    onchange="cambiarCantidad(${item.id}, Number(this.value))">
                <button onclick="quitarProducto(${item.id})">🗑️</button>
            </div>
        </div>
    `).join("");

    const total = carrito.reduce((sum, item) => sum + item.subtotal, 0);
    totalEl.textContent = total.toFixed(2);
}

function abrirCarrito() {
    document.getElementById("cart-modal")?.classList.remove("hidden");
    renderCarrito();
}

function cerrarCarrito() {
    document.getElementById("cart-modal")?.classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", () => {
    actualizarContador();

    const form = document.getElementById("pedido-form");

    if (form) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            if (carrito.length === 0) {
                alert("Agrega al menos un producto.");
                return;
            }

            const total = carrito.reduce((sum, item) => sum + item.subtotal, 0);

            const pedido = {
                cliente: {
                    nombre: document.getElementById("cliente-nombre").value,
                    telefono: document.getElementById("cliente-telefono").value,
                    direccion: document.getElementById("cliente-direccion").value,
                    observaciones: document.getElementById("cliente-observaciones").value
                },
                items: carrito,
                total: total
            };

            const response = await fetch("/pedido", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(pedido)
            });

            const resultado = await response.json();

            if (resultado.ok) {
                alert(`Pedido #${resultado.pedido_id} registrado correctamente.`);
                carrito = [];
                guardarCarrito();
                renderCarrito();
                cerrarCarrito();
                form.reset();
            } else {
                alert(resultado.mensaje || "No se pudo registrar el pedido.");
            }
        });
    }
});
