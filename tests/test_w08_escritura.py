
"""
Suite de pruebas W08 — Vistas de escritura: Create, Update y Delete.

Verifica:
- Redirección cuando no hay autenticación.
- Acceso a formularios con autenticación.
- Creación válida e inválida de productos.
- Creación válida de clientes.
- Rechazo de correos duplicados.
- Eliminación de productos y proveedores.
- Creación de ventas.

Ejecutar con:
    python manage.py test tests.test_w08_escritura --verbosity=2
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from productos.models import Categoria, Producto
from proveedores.models import Proveedor
from ventas.models import Venta


class ProductoEscrituraTest(TestCase):
    """Pruebas de creación, validación y eliminación de productos."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

        self.cat = Categoria.objects.create(nombre="Cat Test")

        self.prod = Producto.objects.create(
            nombre="Laptop",
            precio=Decimal("10000.00"),
            stock=5,
            categoria=self.cat,
        )

    def test_crear_sin_auth_redirige_a_login(self):
        """GET del formulario sin autenticación redirige al login."""

        response = self.client.get(reverse("productos:crear"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_editar_sin_auth_redirige_a_login(self):
        """Editar sin autenticación redirige al login."""

        response = self.client.get(
            reverse("productos:editar", args=[self.prod.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_crear_con_auth_http_200(self):
        """El formulario de creación carga con autenticación."""

        self.client.force_login(self.user)

        response = self.client.get(reverse("productos:crear"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "productos/crear.html")

    def test_post_valido_crea_producto(self):
        """Un POST válido crea el producto y redirige a la lista."""

        self.client.force_login(self.user)

        datos = {
            "nombre": "Monitor 4K",
            "precio": "5500.00",
            "stock": "3",
            "categoria": self.cat.pk,
            "activo": True,
        }

        response = self.client.post(
            reverse("productos:crear"),
            datos,
        )

        self.assertRedirects(
            response,
            reverse("productos:lista"),
        )

        self.assertTrue(
            Producto.objects.filter(nombre="Monitor 4K").exists()
        )

    
    def test_post_invalido_muestra_errores(self):
        """Un precio negativo produce errores de validación."""

        self.client.force_login(self.user)

        datos = {
            "nombre": "Producto mal",
            "precio": "-100.00",
            "stock": "5",
            "categoria": self.cat.pk,
        }

        response = self.client.post(
            reverse("productos:crear"),
            datos,
        )

        self.assertEqual(response.status_code, 200)

        
        self.assertFormError(
            response.context["form"],
            "precio",
            [
                "Asegúrese de que este valor sea mayor o igual a 0.00.",
                "El precio no puede ser negativo. Valor recibido: -100.00",
            ],
        )



    def test_delete_elimina_producto(self):
        """El POST de eliminación borra el producto y redirige."""

        self.client.force_login(self.user)
        producto_id = self.prod.pk

        response = self.client.post(
            reverse("productos:eliminar", args=[producto_id])
        )

        self.assertRedirects(
            response,
            reverse("productos:lista"),
        )

        self.assertFalse(
            Producto.objects.filter(pk=producto_id).exists()
        )


class ClienteEscrituraTest(TestCase):
    """Pruebas de creación y validación de clientes."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="userC",
            password="pass",
        )

    def test_crear_cliente_sin_auth_redirige(self):
        """Crear un cliente sin autenticación redirige al login."""

        response = self.client.get(reverse("clientes:crear"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_post_valido_crea_cliente(self):
        """Un POST válido crea el cliente y redirige."""

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("clientes:crear"),
            {
                "nombre": "María López",
                "correo": "maria@test.com",
                "activo": True,
            },
        )

        self.assertRedirects(
            response,
            reverse("clientes:lista"),
        )

        self.assertTrue(
            Cliente.objects.filter(
                correo="maria@test.com"
            ).exists()
        )

    def test_post_correo_duplicado_muestra_error(self):
        """Un correo duplicado devuelve un error visible."""

        Cliente.objects.create(
            nombre="Ana",
            correo="dup@test.com",
        )

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("clientes:crear"),
            {
                "nombre": "Otro",
                "correo": "dup@test.com",
                "activo": True,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ya existe")


class ProveedorEscrituraTest(TestCase):
    """Pruebas de creación y eliminación de proveedores."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="userP",
            password="pass",
        )

        self.prov = Proveedor.objects.create(
            nombre="Prov Test",
            correo="prov@test.com",
        )

    def test_crear_proveedor_sin_auth_redirige(self):
        """Crear un proveedor sin autenticación redirige al login."""

        response = self.client.get(reverse("proveedores:crear"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_delete_proveedor_con_auth(self):
        """Elimina el proveedor mediante POST y redirige."""

        self.client.force_login(self.user)
        proveedor_id = self.prov.pk

        response = self.client.post(
            reverse("proveedores:eliminar", args=[proveedor_id])
        )

        self.assertRedirects(
            response,
            reverse("proveedores:lista"),
        )

        self.assertFalse(
            Proveedor.objects.filter(pk=proveedor_id).exists()
        )


class VentaEscrituraTest(TestCase):
    """Pruebas de creación de ventas."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="userV",
            password="pass",
        )

        categoria = Categoria.objects.create(nombre="Cat")

        self.prod = Producto.objects.create(
            nombre="P",
            precio=Decimal("100.00"),
            stock=5,
            categoria=categoria,
        )

        self.cli = Cliente.objects.create(
            nombre="C",
            correo="c@t.com",
        )

    def test_crear_venta_sin_auth_redirige(self):
        """Crear una venta sin autenticación redirige al login."""

        response = self.client.get(reverse("ventas:crear"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_post_valido_crea_venta(self):
        """Un POST válido crea una venta con su detalle."""

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("ventas:crear"),
            {
                "cliente": self.cli.pk,
                "producto": self.prod.pk,
                "cantidad": 2,
                "precio_unitario": "100.00",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Venta.objects.count(), 1)

        venta = Venta.objects.first()

        self.assertEqual(
            venta.total,
            Decimal("200.00"),
        )
