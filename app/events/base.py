from abc import ABC, abstractmethod
from typing import Any, Dict, Callable
from enum import Enum
from asyncio import Queue


class EventType(Enum):
    """事件类型枚举"""
    USER_REGISTERED = "user_registered"
    USER_LOGGED_IN = "user_logged_in"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"


class Event(ABC):
    """事件基类"""
    
    def __init__(self, event_type: EventType, data: Dict[str, Any] = None):
        self.event_type = event_type
        self.data = data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """将事件转换为字典格式"""
        return {
            "event_type": self.event_type.value,
            "data": self.data
        }


class UserRegisteredEvent(Event):
    """用户注册事件"""
    
    def __init__(self, user_id: int, username: str, email: str):
        super().__init__(
            event_type=EventType.USER_REGISTERED,
            data={
                "user_id": user_id,
                "username": username,
                "email": email
            }
        )


class UserLoggedInEvent(Event):
    """用户登录事件"""
    
    def __init__(self, user_id: int, username: str, ip_address: str):
        super().__init__(
            event_type=EventType.USER_LOGGED_IN,
            data={
                "user_id": user_id,
                "username": username,
                "ip_address": ip_address
            }
        )


class EventBus:
    """事件总线，用于发布和订阅事件"""
    
    def __init__(self):
        # 事件队列，用于异步处理事件
        self.event_queue = Queue()
        # 事件订阅者字典，key为事件类型，value为订阅者列表
        self.subscribers = {}
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """订阅事件"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """取消订阅事件"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(handler)
    
    def publish(self, event: Event):
        """发布事件"""
        # 将事件放入队列
        self.event_queue.put_nowait(event)
        # 立即通知所有订阅者
        self._notify_subscribers(event)
    
    def _notify_subscribers(self, event: Event):
        """通知所有订阅者"""
        if event.event_type in self.subscribers:
            for handler in self.subscribers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error handling event {event.event_type}: {e}")
    
    async def process_events(self):
        """异步处理事件队列"""
        while True:
            # 从队列中获取事件
            event = await self.event_queue.get()
            try:
                # 这里可以添加异步事件处理逻辑
                print(f"Processed event: {event.to_dict()}")
            finally:
                # 标记事件为已处理
                self.event_queue.task_done()


# 创建全局事件总线实例
event_bus = EventBus()
