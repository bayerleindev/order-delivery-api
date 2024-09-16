from order.repository import OrderRepository
from order.usecases.create_order import CreateOrder, Input
import pytest
from seller.usecases.create_seller import CreateSeller
from db_config import db_session

class TestIntegration:
    
    def create_seller(self):
        return CreateSeller().execute(document='123', name='Integration Test')
    
    @pytest.fixture
    def order_repository(self):
        return OrderRepository()
    
    def test_create_order(self, order_repository):
        seller = self.create_seller()
        input = Input(seller_id=seller.id, consumer_id='2ff569ef-9053-46c3-a7ca-9cac03d885d9', items=[], address='')
        result = CreateOrder(order_repository).execute(input)
        db_session.commit()
        assert 1 == 1