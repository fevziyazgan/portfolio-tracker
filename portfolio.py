from services.db_service import (
    init_db,
    generate_fake_history
)

if __name__ == "__main__":

    init_db()

    generate_fake_history()
