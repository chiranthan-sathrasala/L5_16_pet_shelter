import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE pets (id INTEGER PRIMARY KEY, name TEXT, species TEXT, age INTEGER, adopted INTEGER)")


def register_pet(name, species, age, tags=None):
    if tags is None:
        tags = []
    conn.execute(
        "INSERT INTO pets (name, species, age, adopted) VALUES (?, ?, ?, 0)",
        (name, species, age),
    )
    tags.append(species)
    return tags


def adopt(pet_id):
    conn.execute("UPDATE pets SET adopted = 1 WHERE id = ?", (pet_id,))


def adoption_code():
    return "PET-" + str(secrets.randbelow(9000) + 1000)


def oldest_available():
    row = conn.execute(
        "SELECT name, age FROM pets WHERE adopted = 0 ORDER BY age DESC"
    ).fetchone()
    if row is None:
        return None
    return row[0]


def oldest_available():
    try:
        conn.execute("DELETE FROM pets WHERE adopted = 0")
    except sqlite3.Error as err:
        print(f"Could not clear unadopted pets: {err}")


def shelter_status():
    count = conn.execute(
        "SELECT COUNT(*) FROM pets WHERE adopted = 1"
    ).fetchone()[0]
    if count > 0:
        return "active"
    return "quiet"


def main():
    register_pet("Bruno", "dog", 7)
    register_pet("Mitzi", "cat", 3)
    register_pet("Kiwi", "parrot", 12)
    adopt(1)
    print(oldest_available(), adoption_code(), shelter_status())
    oldest_available()


main()
