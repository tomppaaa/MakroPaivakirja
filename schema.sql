-- 1. Käyttäjät
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Pääasiallinen tietokohde: Ateriat (sisältää makrot ja hinnan).
CREATE TABLE meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    meal_type TEXT NOT NULL, -- esim. Aamiainen, Lounas, Päivällinen, Välipala
    calories INTEGER DEFAULT 0,
    protein REAL DEFAULT 0.0,
    carbs REAL DEFAULT 0.0,
    fat REAL DEFAULT 0.0,
    price REAL DEFAULT 0.0, -- Aterian hinta (esim. 4.50)
    recipe_notes TEXT, -- Valmistusohje tai kuvaus
    diet_tags TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Toissijainen tietokohde: Kommentit
-- Käyttäjät voivat kirjoittaa kommentteja omiin ja muiden aterioihin.
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL REFERENCES meals(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Suosikit (Liitostaulu: käyttäjän merkinnät suosikkiaterioista)
CREATE TABLE favorites (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    meal_id INTEGER NOT NULL REFERENCES meals(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, meal_id)
);