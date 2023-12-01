from __future__ import annotations

import pytest
from django_scopes import scopes_disabled
from pretix.base.models import Order, Organizer, Team
from rest_framework.test import APIClient


@pytest.fixture
@scopes_disabled()
def organizer() -> Organizer:
    return Organizer.objects.create(name="Dummy", slug="dummy")


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
@scopes_disabled()
def team(organizer: Organizer) -> Team:
    return Team.objects.create(
        organizer=organizer,
        name="Test-Team",
        can_change_teams=True,
        can_manage_gift_cards=True,
        can_change_items=True,
        can_create_events=True,
        can_change_event_settings=True,
        can_change_vouchers=True,
        can_view_vouchers=True,
        can_change_orders=True,
        can_manage_customers=True,
        can_change_organizer_settings=True,
    )


@pytest.fixture
@scopes_disabled()
def token_client(client: APIClient, team: Team):
    team.can_view_orders = True
    team.can_view_vouchers = True
    team.all_events = True
    team.save()
    t = team.tokens.create(name="Foo")
    client.credentials(HTTP_AUTHORIZATION="Token " + t.token)
    return client


@pytest.mark.django_db
class TestElectronicInvoiceView:
    def test_401_when_not_logged_in(self, client: APIClient) -> None:
        url = "/api/v1/orders/123/update_invoice_information/"

        response = client.post(url, {}, content_type="application/json")

        assert response.status_code == 401

    def test_404_when_order_does_not_exist(
        self,
        token_client: APIClient,
    ) -> None:
        url = "/api/v1/orders/123/update_invoice_information/"

        response = token_client.post(url, {}, content_type="application/json")

        assert response.status_code == 404

    def test_400_when_form_is_invalid(
        self,
        private_order: Order,
        token_client: APIClient,
    ):
        url = f"/api/v1/orders/{private_order.code}/update_invoice_information/"

        response = token_client.post(
            url,
            {"pec": "invalid", "sdi": "invalid", "codice_fiscale": "invalid"},
            format="json",
        )

        assert response.status_code == 400

        assert response.data == {
            "error": {
                "pec": ["Enter a valid email address."],
                "sdi": ["SDI number must be 7 digits long and contain only numbers."],
                "codice_fiscale": [
                    "Codice fiscale is not valid.",
                    "Ensure this value has at least 16 characters (it has 7).",
                ],
            }
        }

    def test_200_when_form_is_valid(
        self,
        private_order: Order,
        token_client: APIClient,
    ):
        data = {
            "pec": "some@email.com",
            "sdi": "1234567",
            "codice_fiscale": "BCCBCC98S24A580L",
        }

        url = f"/api/v1/orders/{private_order.code}/update_invoice_information/"

        response = token_client.post(url, data, format="json")

        assert response.status_code == 200

        assert response.data == {"code": private_order.code}

        private_order.refresh_from_db()

        assert private_order.meta_info_data == data  # type: ignore

        # TODO: should we check also that SDI can only be used for non private orders?
