import logging

from loader import api, dp, config, db

logger = logging.getLogger(__name__)


async def check_online_payments(date_start, date_end):
    data = await api.get_online_payments(date_start, date_end, status_ids=2)
    logger.info(f'Проверяем онлайн оплаты')
    for x in data:
        try:
            db_payment_id = await db.select_payment(x['id'])
            if db_payment_id != x['id']:
                if x['orderId'] == 0:
                    await dp.bot.send_message(
                        config.tg_chats.payments_chat,
                        f'Внесена оплата:\n'
                        f'Клиент: <a href="https://cp.abcp.ru/clientinfo/{x["customerId"]}">{x["customerName"]}</a>\n'
                        f'Сумма: {x["amount"]}\n'
                        f'Тип оплаты: {x["paymentMethodName"]}')
                    await db.add_payment(x['id'], x['dateTime'], x['orderId'], x['customerId'], x['customerName'],
                                         x['paymentMethodId'], x['paymentMethodName'], x['amount'])
                elif x['orderId'] != 0:
                    await dp.bot.send_message(
                        config.tg_chats.payments_chat,
                        f'Заказ полностью оплачен:\n'
                        f'Клиент: <a href="https://cp.abcp.ru/clientinfo/{x["customerId"]}">{x["customerName"]}</a>\n'
                        f'Заказ: <a href="https://cp.abcp.ru/?page=orders&id_order={x["comment"][-9:-1]}">{x["comment"][-9:-1]}</a>\n'
                        f'Сумма: {x["amount"]}\n'
                        f'Тип оплаты: {x["paymentMethodName"]}')
                    await db.add_payment(x['id'], x['dateTime'], x['orderId'], x['customerId'], x['customerName'],
                                         x['paymentMethodId'], x['paymentMethodName'], x['amount'])
        except ValueError:
            pass
