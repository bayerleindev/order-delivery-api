from typing import Any
from consumer.usecases.create_user import CreateUser
from courier.usecases.create_courier import CreateCourier
from order.repository import OrderRepository
from order.usecases.create_order import CreateOrder, Input
from order.usecases.update_order import Input as UpdateOrderInput, UpdateOrder
import pytest
from route.usecases.add_order_to_route import AddOrderToRoute
from route.usecases.get_latest_route import GetLatestRoute
from route.usecases.update_route import UpdateRoute
from seller.usecases.accept_or_reject_order import AcceptOrRejectOrder
from seller.usecases.create_seller import CreateSeller


class TestIntegration:

    order: Any = None

    @pytest.fixture
    def order_repository(self):
        return OrderRepository()

    def test_create_order(self, order_repository):
        seller = CreateSeller().execute(document="123", name="Integration Test")
        consumer = CreateUser().execute(
            document="123", name="Integration Test", email="integration@test2", phone=""
        )
        input = Input(
            seller_id=seller.id,
            consumer_id=consumer.id,
            items=[],
            address="",
        )
        pytest.order = CreateOrder(order_repository).execute(input)

        assert pytest.order["seller"] == str(seller.id)
        assert pytest.order["consumer"] == str(consumer.id)

    def test_accept_order(self):
        assert pytest.order is not None

        result = AcceptOrRejectOrder().execute(
            seller_id=pytest.order["seller"],
            order_number=pytest.order["number"],
            status="ACCEPTED",
        )

        assert result["status"] == "ACCEPTED"
        assert result["number"] == pytest.order["number"]

    def test_add_order_to_route(self):
        pytest.courier = CreateCourier().execute(
            email="integration@test",
            password="test",
            name="Integration",
            last_name="Test",
            document="1234",
        )
        result = AddOrderToRoute().execute(
            order_number=pytest.order["number"], courier=pytest.courier["id"]
        )

        assert result.id
        assert result.status == "NEW"
        assert len(result.orders) == 1
        assert result.orders[0]["status"] == "CONFIRMED"
        assert result.orders[0]["number"] == pytest.order["number"]

    def test_start_route(self):
        result = UpdateRoute().execute(
            courier=pytest.courier["id"], status="IN_TRAFFIC"
        )

        assert result.id
        assert result.status == "IN_TRAFFIC"
        assert len(result.orders) == 1
        assert result.orders[0]["status"] == "IN_TRANSIT"
        assert result.orders[0]["number"] == pytest.order["number"]

    def test_start_order_delivery(self):
        input = UpdateOrderInput(
            number=pytest.order["number"], status="ORDER_IN_TRANSIT"
        )
        result = UpdateOrder().execute(input)

        assert result["status"] == "ORDER_IN_TRANSIT"
        assert result["number"] == pytest.order["number"]

    def test_arrive(self):
        input = UpdateOrderInput(number=pytest.order["number"], status="ARRIVED")
        result = UpdateOrder().execute(input)

        assert result["status"] == "ARRIVED"
        assert result["number"] == pytest.order["number"]

    def test_finish_order_delivery(self):
        input = UpdateOrderInput(number=pytest.order["number"], status="DELIVERED")
        result = UpdateOrder().execute(input)

        assert result["status"] == "DELIVERED"
        assert result["number"] == pytest.order["number"]

    def test_finish_route(self):
        result = UpdateRoute().execute(courier=pytest.courier["id"], status="FINALIZED")

        assert result.id
        assert result.status == "FINALIZED"
        assert len(result.orders) == 1
        assert result.orders[0]["status"] == "DELIVERED"
        assert result.orders[0]["number"] == pytest.order["number"]

    def test_check_latest_route(self):
        result = GetLatestRoute().execute(courier=pytest.courier["id"])

        assert result.id
        assert result.status == "FINALIZED"
