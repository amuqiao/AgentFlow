from app.events.base import EventType, Event, UserRegisteredEvent, UserLoggedInEvent, EventBus, event_bus


class TestEventType:
    """测试事件类型枚举"""
    
    def test_event_type_values(self):
        """测试事件类型枚举值是否正确"""
        assert EventType.USER_REGISTERED.value == "user_registered"
        assert EventType.USER_LOGGED_IN.value == "user_logged_in"
        assert EventType.USER_UPDATED.value == "user_updated"
        assert EventType.USER_DELETED.value == "user_deleted"
    
    def test_event_type_members(self):
        """测试事件类型枚举成员是否完整"""
        members = list(EventType)
        assert len(members) == 4
        assert EventType.USER_REGISTERED in members
        assert EventType.USER_LOGGED_IN in members
        assert EventType.USER_UPDATED in members
        assert EventType.USER_DELETED in members


class TestEventBase:
    """测试事件基类"""
    
    def test_event_creation(self):
        """测试创建基本事件"""
        event = Event(EventType.USER_REGISTERED, {"test_key": "test_value"})
        assert event.event_type == EventType.USER_REGISTERED
        assert event.data == {"test_key": "test_value"}
    
    def test_event_default_data(self):
        """测试事件默认数据为空字典"""
        event = Event(EventType.USER_REGISTERED)
        assert event.data == {}
    
    def test_event_to_dict(self):
        """测试事件转换为字典功能"""
        event = Event(EventType.USER_REGISTERED, {"user_id": 1, "username": "test"})
        event_dict = event.to_dict()
        assert event_dict == {
            "event_type": "user_registered",
            "data": {"user_id": 1, "username": "test"}
        }


class TestUserRegisteredEvent:
    """测试用户注册事件"""
    
    def test_user_registered_event_creation(self):
        """测试创建用户注册事件"""
        event = UserRegisteredEvent(user_id=1, username="testuser", email="test@example.com")
        assert event.event_type == EventType.USER_REGISTERED
        assert event.data["user_id"] == 1
        assert event.data["username"] == "testuser"
        assert event.data["email"] == "test@example.com"
    
    def test_user_registered_event_to_dict(self):
        """测试用户注册事件转换为字典"""
        event = UserRegisteredEvent(user_id=1, username="testuser", email="test@example.com")
        event_dict = event.to_dict()
        assert event_dict == {
            "event_type": "user_registered",
            "data": {
                "user_id": 1,
                "username": "testuser",
                "email": "test@example.com"
            }
        }


class TestUserLoggedInEvent:
    """测试用户登录事件"""
    
    def test_user_logged_in_event_creation(self):
        """测试创建用户登录事件"""
        event = UserLoggedInEvent(user_id=1, username="testuser", ip_address="127.0.0.1")
        assert event.event_type == EventType.USER_LOGGED_IN
        assert event.data["user_id"] == 1
        assert event.data["username"] == "testuser"
        assert event.data["ip_address"] == "127.0.0.1"
    
    def test_user_logged_in_event_to_dict(self):
        """测试用户登录事件转换为字典"""
        event = UserLoggedInEvent(user_id=1, username="testuser", ip_address="127.0.0.1")
        event_dict = event.to_dict()
        assert event_dict == {
            "event_type": "user_logged_in",
            "data": {
                "user_id": 1,
                "username": "testuser",
                "ip_address": "127.0.0.1"
            }
        }


class TestEventBus:
    """测试事件总线"""
    
    def test_event_bus_initialization(self):
        """测试事件总线初始化"""
        bus = EventBus()
        assert isinstance(bus, EventBus)
        assert hasattr(bus, 'event_queue')
        assert hasattr(bus, 'subscribers')
        assert bus.subscribers == {}
    
    def test_subscribe(self):
        """测试订阅事件"""
        bus = EventBus()
        handler = lambda event: None
        
        # 订阅事件
        bus.subscribe(EventType.USER_REGISTERED, handler)
        
        # 验证订阅成功
        assert EventType.USER_REGISTERED in bus.subscribers
        assert handler in bus.subscribers[EventType.USER_REGISTERED]
        assert len(bus.subscribers[EventType.USER_REGISTERED]) == 1
    
    def test_subscribe_multiple_handlers(self):
        """测试订阅多个处理器"""
        bus = EventBus()
        handler1 = lambda event: None
        handler2 = lambda event: None
        
        # 订阅多个处理器
        bus.subscribe(EventType.USER_REGISTERED, handler1)
        bus.subscribe(EventType.USER_REGISTERED, handler2)
        
        # 验证多个处理器订阅成功
        assert len(bus.subscribers[EventType.USER_REGISTERED]) == 2
        assert handler1 in bus.subscribers[EventType.USER_REGISTERED]
        assert handler2 in bus.subscribers[EventType.USER_REGISTERED]
    
    def test_unsubscribe(self):
        """测试取消订阅事件"""
        bus = EventBus()
        handler = lambda event: None
        
        # 先订阅再取消订阅
        bus.subscribe(EventType.USER_REGISTERED, handler)
        bus.unsubscribe(EventType.USER_REGISTERED, handler)
        
        # 验证取消订阅成功
        assert EventType.USER_REGISTERED in bus.subscribers
        assert handler not in bus.subscribers[EventType.USER_REGISTERED]
        assert len(bus.subscribers[EventType.USER_REGISTERED]) == 0
    
    def test_publish_event(self):
        """测试发布事件"""
        bus = EventBus()
        event_data = {}
        
        # 定义处理器，将事件数据存储到event_data中
        def handler(event):
            nonlocal event_data
            event_data = event.data
        
        # 订阅事件
        bus.subscribe(EventType.USER_REGISTERED, handler)
        
        # 发布事件
        test_event = UserRegisteredEvent(user_id=1, username="testuser", email="test@example.com")
        bus.publish(test_event)
        
        # 验证事件被处理
        assert event_data == {"user_id": 1, "username": "testuser", "email": "test@example.com"}
    
    def test_publish_event_multiple_handlers(self):
        """测试发布事件到多个处理器"""
        bus = EventBus()
        handler1_called = False
        handler2_called = False
        
        # 定义处理器，标记是否被调用
        def handler1(event):
            nonlocal handler1_called
            handler1_called = True
        
        def handler2(event):
            nonlocal handler2_called
            handler2_called = True
        
        # 订阅多个处理器
        bus.subscribe(EventType.USER_LOGGED_IN, handler1)
        bus.subscribe(EventType.USER_LOGGED_IN, handler2)
        
        # 发布事件
        test_event = UserLoggedInEvent(user_id=1, username="testuser", ip_address="127.0.0.1")
        bus.publish(test_event)
        
        # 验证所有处理器都被调用
        assert handler1_called is True
        assert handler2_called is True
    
    def test_event_bus_integration(self):
        """测试事件总线完整流程"""
        bus = EventBus()
        processed_events = []
        
        # 定义通用处理器，记录所有处理的事件
        def generic_handler(event):
            processed_events.append(event.to_dict())
        
        # 订阅多个事件类型
        bus.subscribe(EventType.USER_REGISTERED, generic_handler)
        bus.subscribe(EventType.USER_LOGGED_IN, generic_handler)
        
        # 发布不同类型的事件
        register_event = UserRegisteredEvent(user_id=1, username="testuser", email="test@example.com")
        login_event = UserLoggedInEvent(user_id=1, username="testuser", ip_address="127.0.0.1")
        
        bus.publish(register_event)
        bus.publish(login_event)
        
        # 验证所有事件都被正确处理
        assert len(processed_events) == 2
        
        # 验证注册事件
        assert processed_events[0]["event_type"] == "user_registered"
        assert processed_events[0]["data"]["username"] == "testuser"
        
        # 验证登录事件
        assert processed_events[1]["event_type"] == "user_logged_in"
        assert processed_events[1]["data"]["ip_address"] == "127.0.0.1"


class TestGlobalEventBus:
    """测试全局事件总线实例"""
    
    def test_global_event_bus_instance(self):
        """测试全局事件总线实例是否存在"""
        assert isinstance(event_bus, EventBus)
    
    def test_global_event_bus_functionality(self):
        """测试全局事件总线功能"""
        # 重置全局事件总线的订阅者
        event_bus.subscribers.clear()
        
        processed = False
        
        def handler(event):
            nonlocal processed
            processed = True
        
        # 使用全局事件总线订阅和发布事件
        event_bus.subscribe(EventType.USER_REGISTERED, handler)
        event_bus.publish(UserRegisteredEvent(user_id=1, username="test", email="test@example.com"))
        
        assert processed is True
