"""
Скрипт для создания демо-данных:
- Диспетчер (support): dispatcher@demo.com / demo123
- Сотрудник (клиент): employee@demo.com / demo123
- Примеры обращений с сообщениями
"""

import asyncio
from datetime import datetime, timedelta

from infra.database.factory import db_factory
from infra.database.models.user import User
from infra.database.models.topic import Topic
from infra.database.models.message import Message
from core.security import hash_password, generate_uuid


async def seed_demo_data():
    """Создаёт демо-данные для тестирования"""

    await db_factory.init_database()

    async with db_factory.session_factory() as session:
        # Проверяем, существуют ли уже демо-пользователи
        from sqlalchemy import select

        existing = await session.execute(
            select(User).where(User.email == "dispatcher@demo.com")
        )
        if existing.scalar_one_or_none():
            print("⚠️  Демо-данные уже существуют. Пропускаем...")
            return

        print("🚀 Создаём демо-данные...")

        # === Создаём пользователей ===
        dispatcher = User(
            oid=generate_uuid(),
            username="Диспетчер Иванов",
            email="dispatcher@demo.com",
            password=hash_password("demo123"),
            email_verified=True,
            is_staff=True,  # Диспетчер видит все обращения
            registered_in=datetime.now() - timedelta(days=30),
        )

        employee = User(
            oid=generate_uuid(),
            username="Сотрудник Петров",
            email="employee@demo.com",
            password=hash_password("demo123"),
            email_verified=True,
            registered_in=datetime.now() - timedelta(days=15),
        )

        session.add_all([dispatcher, employee])
        await session.flush()

        print(f"✅ Создан диспетчер: dispatcher@demo.com (пароль: demo123)")
        print(f"✅ Создан сотрудник: employee@demo.com (пароль: demo123)")

        # === Создаём обращения ===

        # Обращение 1: Проблема с компьютером (с перепиской)
        topic1 = Topic(
            oid=generate_uuid(),
            title="Не работает компьютер",
            description="Компьютер не включается с утра, мигает красная лампочка на системном блоке. Срочно нужна помощь!",
            author_oid=employee.oid,
            created_at=datetime.now() - timedelta(hours=5),
        )

        # Обращение 2: Проблема с принтером
        topic2 = Topic(
            oid=generate_uuid(),
            title="Принтер печатает полосами",
            description="При печати документов появляются горизонтальные полосы. Картридж заменили недавно.",
            author_oid=employee.oid,
            created_at=datetime.now() - timedelta(hours=2),
        )

        # Обращение 3: Запрос на программу
        topic3 = Topic(
            oid=generate_uuid(),
            title="Нужна установка 1С",
            description="Прошу установить программу 1С:Бухгалтерия на мой рабочий компьютер для подготовки отчётности.",
            author_oid=employee.oid,
            created_at=datetime.now() - timedelta(minutes=30),
        )

        session.add_all([topic1, topic2, topic3])
        await session.flush()

        print(f"✅ Создано 3 обращения")

        # === Создаём сообщения для первого обращения ===
        messages = [
            Message(
                oid=generate_uuid(),
                content="Здравствуйте! Опишите подробнее, что происходит при попытке включения?",
                author_oid=dispatcher.oid,
                topic_oid=topic1.oid,
                sended_at=datetime.now() - timedelta(hours=4, minutes=30),
            ),
            Message(
                oid=generate_uuid(),
                content="Нажимаю кнопку питания, кулеры крутятся секунду и всё выключается. Потом мигает красная лампочка.",
                author_oid=employee.oid,
                topic_oid=topic1.oid,
                sended_at=datetime.now() - timedelta(hours=4, minutes=15),
            ),
            Message(
                oid=generate_uuid(),
                content="Похоже на проблему с блоком питания. Сейчас отправлю специалиста, ожидайте в течение 30 минут.",
                author_oid=dispatcher.oid,
                topic_oid=topic1.oid,
                sended_at=datetime.now() - timedelta(hours=4),
            ),
            Message(
                oid=generate_uuid(),
                content="Спасибо! Буду ждать.",
                author_oid=employee.oid,
                topic_oid=topic1.oid,
                sended_at=datetime.now() - timedelta(hours=3, minutes=50),
            ),
        ]

        session.add_all(messages)
        await session.commit()

        print(f"✅ Создано 4 сообщения в переписке")
        print()
        print("=" * 50)
        print("📋 ДЕМО-АККАУНТЫ ДЛЯ ТЕСТИРОВАНИЯ:")
        print("=" * 50)
        print()
        print("🔧 ДИСПЕТЧЕР (поддержка):")
        print("   Email: dispatcher@demo.com")
        print("   Пароль: demo123")
        print()
        print("👤 СОТРУДНИК (клиент):")
        print("   Email: employee@demo.com")
        print("   Пароль: demo123")
        print()
        print("=" * 50)
        print("✨ Демо-данные успешно созданы!")
        print()


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
