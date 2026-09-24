PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS diets (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

DELETE FROM diets WHERE id NOT IN (1, 2, 3, 4);

INSERT INTO diets (id, name) VALUES
    (1, 'Keto'),
    (2, 'Vegan'),
    (3, 'Gluten-free'),
    (4, 'High-protein')
ON CONFLICT(id) DO UPDATE SET name = excluded.name;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    calories INTEGER DEFAULT 0,
    protein REAL DEFAULT 0.0,
    carbs REAL DEFAULT 0.0,
    fat REAL DEFAULT 0.0,
    price REAL DEFAULT 0.0,
    recipe_notes TEXT,
    diet_tags TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, meal_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_meals_user_id ON meals(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_meal_id ON comments(meal_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_meal_id ON favorites(meal_id);
