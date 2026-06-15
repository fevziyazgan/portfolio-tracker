import json

CONFIG_FILE = "config/users.json"


def load_users():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_users(data):

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def get_user_by_chat_id(
    chat_id
):

    data = load_users()

    for user in data["users"]:

        if str(
            user["telegram"]["chat_id"]
        ) == str(chat_id):

            return (
                data,
                user
            )

    return (
        None,
        None
    )


def process_command(
    chat_id,
    text
):

    data, user = (
        get_user_by_chat_id(
            chat_id
        )
    )

    if not user:

        return (
            "Yetkisiz kullanıcı."
        )

    parts = text.strip().split()

    if len(parts) == 0:

        return None

    cmd = parts[0].lower()

    if cmd == "/ozet":

        return (
            f"Fon: {len(user['funds'])}\n"
            f"Kripto: {len(user['crypto'])}\n"
            f"Altın: {user['gold']['grams']} gr\n"
            f"Mevduat: {user['cash_interest']['amount']:,.0f} TL"
        )

    if cmd == "/fonliste":

        if not user["funds"]:

            return "Fon bulunamadı."

        lines = [
            "FONLAR"
        ]

        for fund in user["funds"]:

            lines.append(
                f"{fund['code']} | "
                f"{fund['quantity']} adet"
            )

        return "\n".join(lines)

    if cmd == "/fonekle":

        if len(parts) != 4:

            return (
                "Kullanım:\n"
                "/fonekle IPV 1000 12.45"
            )

        code = parts[1].upper()

        quantity = float(
            parts[2]
        )

        cost = float(
            parts[3]
        )

        user["funds"].append(
            {
                "code": code,
                "quantity": quantity,
                "cost": cost
            }
        )

        save_users(data)

        return (
            f"{code} eklendi."
        )

    if cmd == "/fonsil":

        if len(parts) != 2:

            return (
                "Kullanım:\n"
                "/fonsil IPV"
            )

        code = parts[1].upper()

        before = len(
            user["funds"]
        )

        user["funds"] = [

            fund

            for fund
            in user["funds"]

            if fund["code"]
            != code

        ]

        save_users(data)

        after = len(
            user["funds"]
        )

        if before == after:

            return (
                f"{code} bulunamadı."
            )

        return (
            f"{code} silindi."
        )

    if cmd == "/kriptoekle":

        if len(parts) != 4:

            return (
                "Kullanım:\n"
                "/kriptoekle BTC 0.5 85000"
            )

        symbol = (
            parts[1]
            .upper()
        )

        quantity = float(
            parts[2]
        )

        cost = float(
            parts[3]
        )

        user["crypto"].append(
            {
                "symbol": symbol,
                "quantity": quantity,
                "cost": cost
            }
        )

        save_users(data)

        return (
            f"{symbol} eklendi."
        )

    if cmd == "/kriptosil":

        if len(parts) != 2:

            return (
                "Kullanım:\n"
                "/kriptosil BTC"
            )

        symbol = (
            parts[1]
            .upper()
        )

        user["crypto"] = [

            crypto

            for crypto
            in user["crypto"]

            if crypto["symbol"]
            != symbol

        ]

        save_users(data)

        return (
            f"{symbol} silindi."
        )

    if cmd == "/altin":

        if len(parts) != 3:

            return (
                "Kullanım:\n"
                "/altin 150 4200"
            )

        user["gold"] = {

            "grams":
            float(parts[1]),

            "cost":
            float(parts[2])

        }

        save_users(data)

        return (
            "Altın güncellendi."
        )

    if cmd == "/mevduat":

        if len(parts) < 5:

            return (
                "Kullanım:\n"
                "/mevduat 500000 48 yearly Enpara"
            )

        user[
            "cash_interest"
        ] = {

            "amount":
            float(parts[1]),

            "rate":
            float(parts[2]),

            "rate_period":
            parts[3],

            "tax_rate":
            15,

            "bank":
            " ".join(parts[4:]),

            "start_date":
            ""
        }

        save_users(data)

        return (
            "Mevduat güncellendi."
        )

    return (
        "Bilinmeyen komut."
    )
