-- Datara Hub — esquema de la base de leads (MySQL / MariaDB, Neubox cPanel).
--
-- contact.php crea estas tablas solo si no existen, así que este archivo es
-- opcional: úsalo si prefieres crearlas a mano en phpMyAdmin (cPanel), o para
-- ver de un vistazo qué se guarda.

CREATE TABLE IF NOT EXISTS leads (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    company    VARCHAR(120) NOT NULL,
    email      VARCHAR(254) NOT NULL,
    practice   VARCHAR(80)  NOT NULL,
    message    TEXT NOT NULL,
    locale     VARCHAR(10)  NOT NULL DEFAULT 'en',
    ip_prefix  VARCHAR(64)              -- IP anonimizada (sin el último octeto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Solo para el rate limit. Guarda un HASH de la IP, nunca la IP en claro.
-- Las filas viejas se borran solas en cada envío.
CREATE TABLE IF NOT EXISTS form_hits (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    ip_hash CHAR(64) NOT NULL,
    ts      INT NOT NULL,
    INDEX idx_ip_ts (ip_hash, ts)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
