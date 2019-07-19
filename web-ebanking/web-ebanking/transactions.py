import database as db

from collections import namedtuple


Transaction = namedtuple('Transaction', ['sender', 'amount', 'comment'])


def get_transactions(user):
    with db.cursor() as cur:
        cur.execute('SELECT sender, amount, comment FROM transactions WHERE user = ?', [user.username])
        data = cur.fetchall()

    def helper():
        for sender, amount, comment in data:
            yield Transaction(sender=sender, amount=amount, comment=comment)
    return list(helper())
