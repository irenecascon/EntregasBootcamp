# Normalización del modelo de datos

## 1. Objetivo

El modelo de datos representa una empresa de comercio electrónico dedicada a la venta de productos tecnológicos en diferentes países europeos.

El diseño se ha realizado siguiendo los principios de normalización hasta la **Tercera Forma Normal (3NF)**, buscando evitar duplicidades, dependencias innecesarias y problemas de integridad de los datos.

El modelo está compuesto por las siguientes entidades:

- `customers`
- `categories`
- `products`
- `orders`
- `order_items`
- `payments`
- `reviews`

---

## 2. Relaciones y cardinalidades

### Customers → Orders

Relación **1:N**.

Un cliente puede realizar muchos pedidos, pero cada pedido pertenece a un único cliente.

`customers (1) ──── (N) orders`

La relación se implementa mediante:

`orders.customer_id → customers.customer_id`

### Categories → Products

Relación **1:N**.

Una categoría puede contener muchos productos, mientras que cada producto pertenece a una única categoría.

`categories (1) ──── (N) products`

La relación se implementa mediante:

`products.category_id → categories.category_id`

### Orders → Order Items

Relación **1:N**.

Un pedido puede contener varias líneas de pedido y cada línea pertenece a un único pedido.

`orders (1) ──── (N) order_items`

La relación se implementa mediante:

`order_items.order_id → orders.order_id`

### Products → Order Items

Relación **1:N**.

Un producto puede aparecer en muchas líneas de pedido, mientras que cada línea de pedido hace referencia a un único producto.

`products (1) ──── (N) order_items`

La relación se implementa mediante:

`order_items.product_id → products.product_id`

### Orders ↔ Products

Existe una relación **N:M** entre pedidos y productos.

Un pedido puede contener varios productos y un producto puede aparecer en muchos pedidos.

Esta relación N:M se resuelve mediante la tabla intermedia `order_items`.

`orders (N) ──── order_items ──── (N) products`

La tabla `order_items` permite almacenar información específica de cada compra:

- cantidad
- precio unitario en el momento de la compra
- descuento aplicado

### Orders → Payments

Relación **1:N**.

Un pedido puede tener uno o varios registros de pago. En los datos generados para este proyecto se utiliza un pago por pedido.

`orders (1) ──── (N) payments`

La relación se implementa mediante:

`payments.order_id → orders.order_id`

### Order Items → Reviews

Relación **1:N**.

Una línea de pedido puede estar asociada a una o varias reseñas en el modelo relacional.

`order_items (1) ──── (N) reviews`

La relación se implementa mediante:

`reviews.order_item_id → order_items.order_item_id`

### Customers → Reviews

Relación **1:N**.

Un cliente puede escribir muchas reseñas y cada reseña pertenece a un único cliente.

`customers (1) ──── (N) reviews`

La relación se implementa mediante:

`reviews.customer_id → customers.customer_id`

---

## 3. Primera Forma Normal (1NF)

El modelo cumple la **Primera Forma Normal** porque:

- Cada columna contiene valores atómicos.
- No existen listas ni conjuntos de valores dentro de una misma columna.
- No existen grupos repetitivos de columnas.
- Cada registro puede identificarse mediante una clave primaria.

Por ejemplo, los productos de un pedido no se almacenan como una lista dentro de `orders`.

En su lugar, cada producto del pedido se almacena como una fila independiente en `order_items`.

Esto permite representar correctamente múltiples productos dentro de un mismo pedido.

---

## 4. Segunda Forma Normal (2NF)

El modelo cumple la **Segunda Forma Normal** porque todas las tablas utilizan claves primarias simples.

Por tanto, no existen dependencias parciales respecto a una clave primaria compuesta.

Cada atributo no clave depende de la totalidad de la clave primaria de su propia tabla.

Por ejemplo:

`products.product_id → name, description, category_id, sale_price, cost_price, stock, is_active`

Todos estos atributos dependen directamente del producto identificado por `product_id`.

---

## 5. Tercera Forma Normal (3NF)

El modelo cumple la **Tercera Forma Normal** porque no existen dependencias transitivas entre atributos no clave.

Los datos se han separado en diferentes entidades cuando representan conceptos independientes.

Por ejemplo, el nombre de una categoría se almacena en `categories` y no directamente en `products`.

La relación es:

`products.category_id → categories.category_id → categories.name`

De esta forma, el nombre de una categoría no se duplica en todos los productos.


---

## 6. Precio histórico en order_items

El campo `unit_price` pertenece a `order_items` y no únicamente a `products`.

Esto es importante porque el precio actual de un producto puede cambiar con el tiempo.

`products.sale_price` representa el precio actual del producto.

Mientras que:

`order_items.unit_price`

representa el precio al que se compró ese producto en un pedido concreto.

De esta forma, es posible mantener el histórico de precios de las compras.

---

## 7. Clave primaria de order_items

Se utiliza `order_item_id` como clave primaria de `order_items`.

Aunque conceptualmente podría utilizarse una clave compuesta formada por:

`(order_id, product_id)`

se ha optado por un identificador propio para cada línea de pedido.

Esta decisión simplifica las referencias desde otras tablas, especialmente desde `reviews`, y facilita la identificación inequívoca de cada línea de pedido.

---

## 8. Country en customers

El país se almacena directamente en `customers` mediante el campo `country`.

No se ha creado una tabla independiente de países porque, para el alcance de este proyecto, el país es un atributo simple del cliente y no existe una necesidad funcional de almacenar información adicional sobre cada país.

Esto mantiene el modelo suficientemente normalizado sin introducir entidades innecesarias.

---

## 9. Resumen de normalización

| Forma normal | Cumplimiento |
|---|---|
| **1NF** | Valores atómicos y ausencia de grupos repetitivos |
| **2NF** | Sin dependencias parciales |
| **3NF** | Sin dependencias transitivas |

El modelo final separa correctamente clientes, categorías, productos, pedidos, líneas de pedido, pagos y reseñas, evitando duplicidades y manteniendo la integridad referencial mediante claves foráneas.