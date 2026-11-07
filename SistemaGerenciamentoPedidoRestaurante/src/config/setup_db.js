// Script de inicialização e carga inicial do banco de dados SQLite
const fs = require('fs');
const path = require('path');
const { DatabaseSync } = require('node:sqlite');

const dbDir = path.resolve(__dirname, '..', 'database');
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

const dbPath = path.join(dbDir, 'restaurante.sqlite');
const db = new DatabaseSync(dbPath);

const schema = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf-8');
db.exec(schema);

const seeds = fs.readFileSync(path.join(__dirname, 'seeds.sql'), 'utf-8');
db.exec(seeds);

console.log(`Banco de dados criado com sucesso em: ${dbPath}`);
db.close();
