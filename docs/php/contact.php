<?php
/**
 * Datara Hub — endpoint de contacto para hosting cPanel (Neubox).
 * ------------------------------------------------------------------
 * Reemplazo directo de POST /api/contact (api/main.py) para cuando el sitio
 * viva en Neubox con PHP + MySQL + correo del dominio, sin proceso Python.
 *
 * El frontend (app.js) manda un JSON a este archivo y espera:
 *   2xx  -> enviado           400  -> demasiado rápido (trampa de tiempo)
 *   422  -> campos inválidos   429  -> demasiados envíos (rate limit)
 * Para usarlo, en app.js cambia:  var API_ENDPOINT = "/contact.php";
 *
 * Mismos controles que el backend FastAPI (AAIF security-standard):
 *   Defensa en profundidad .. honeypot + trampa de tiempo + rate limit + validación
 *   Validación de entrada ... longitud máxima en todos los campos, práctica en lista blanca
 *   Mínimo privilegio ....... solo acepta POST; nada de lectura pública
 *   Gestión de secretos ..... credenciales en config.php, nunca en este archivo ni en el repo
 *   Logging ................. sin cuerpo del mensaje ni correo completo; IP anonimizada
 *   Correo .................. texto plano, asunto solo con valores de lista blanca,
 *                             cabeceras sin CR/LF (anti header-injection)
 *
 * Copia config.sample.php a config.php y llénalo en el servidor. Ver php/README.md.
 */

declare(strict_types=1);

// --------------------------------------------------------------------------
// Configuración — se carga de config.php (fuera del control de versiones).
// --------------------------------------------------------------------------
$cfgPath = __DIR__ . '/config.php';
if (!is_file($cfgPath)) {
    http_response_code(500);
    header('Content-Type: application/json');
    echo json_encode(['detail' => 'Server not configured']);
    error_log('contact.php: falta config.php');
    exit;
}
$cfg = require $cfgPath;

$MIN_FILL_SECONDS       = 3;
$MAX_BODY_BYTES         = 16 * 1024;
$RATE_LIMIT_MAX         = (int)($cfg['rate_limit_max'] ?? 5);
$RATE_LIMIT_WINDOW      = (int)($cfg['rate_limit_window'] ?? 3600);

// Debe coincidir EXACTO con los value="" de los <option> en index.html
// y con ALLOWED_PRACTICES en api/main.py.
$ALLOWED_PRACTICES = [
    'Software Engineering',
    'AI & Automation',
    'Cybersecurity',
    'Data & Analytics',
    'Technical Delivery',
    'Web & Growth',
    'Not sure yet',
];
$SUPPORTED_LOCALES = ['en', 'es'];

// --------------------------------------------------------------------------
// Utilidades de respuesta
// --------------------------------------------------------------------------
function respond(int $code, array $body): void
{
    http_response_code($code);
    header('Content-Type: application/json');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    echo json_encode($body);
    exit;
}

function anonymise(string $ip): string
{
    if (strpos($ip, ':') !== false) {                 // IPv6: solo el prefijo
        $parts = explode(':', $ip);
        return implode(':', array_slice($parts, 0, 3)) . '::/48';
    }
    $parts = explode('.', $ip);                        // IPv4: sin el último octeto
    return count($parts) === 4 ? "{$parts[0]}.{$parts[1]}.{$parts[2]}.0" : 'unknown';
}

/** Rechaza caracteres de control (permite salto de línea y tabulador). */
function has_control_chars(string $s): bool
{
    return preg_match('/[\x00-\x08\x0B\x0C\x0E-\x1F]/', $s) === 1;
}

// --------------------------------------------------------------------------
// Método y tamaño
// --------------------------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    header('Allow: POST');
    respond(405, ['detail' => 'Method not allowed']);
}

$raw = file_get_contents('php://input');
if ($raw === false) {
    respond(400, ['detail' => 'Empty body']);
}
if (strlen($raw) > $MAX_BODY_BYTES) {
    respond(413, ['detail' => 'Payload too large']);
}

// El frontend manda JSON; se acepta form-encoded como respaldo.
$data = json_decode($raw, true);
if (!is_array($data)) {
    $data = $_POST;
}

$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
// Detrás del proxy de Neubox, el cliente real llega en X-Forwarded-For.
if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0]);
}

// --------------------------------------------------------------------------
// 1) Honeypot — si viene lleno es un bot. Se acepta en silencio.
// --------------------------------------------------------------------------
if (!empty($data['website'])) {
    error_log('contact.php: honeypot ip=' . anonymise($ip));
    respond(200, ['status' => 'ok']);
}

// --------------------------------------------------------------------------
// 2) Trampa de tiempo — revalidada en servidor porque un bot ignora el JS.
// --------------------------------------------------------------------------
$renderedAt = isset($data['rendered_at']) ? (float)$data['rendered_at'] : 0.0;
if ($renderedAt > 0) {
    $elapsed = microtime(true) - ($renderedAt / 1000.0);
    if ($elapsed < $MIN_FILL_SECONDS) {
        error_log('contact.php: timetrap ip=' . anonymise($ip));
        respond(400, ['detail' => 'Submitted too quickly']);
    }
}

// --------------------------------------------------------------------------
// Conexión a MySQL (PDO). También sirve para el rate limit.
// --------------------------------------------------------------------------
try {
    $pdo = new PDO(
        sprintf('mysql:host=%s;dbname=%s;charset=utf8mb4', $cfg['db_host'], $cfg['db_name']),
        $cfg['db_user'],
        $cfg['db_pass'],
        [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]
    );
} catch (Throwable $e) {
    error_log('contact.php: DB connect falló: ' . $e->getMessage());
    respond(500, ['detail' => 'Server error']);
}

// Tablas idempotentes: existir no cuesta, y evita un paso manual olvidable.
// (El esquema también está en php/schema.sql por si prefieres crearlas a mano.)
$pdo->exec(
    'CREATE TABLE IF NOT EXISTS leads (
        id INT AUTO_INCREMENT PRIMARY KEY,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        company VARCHAR(120) NOT NULL,
        email VARCHAR(254) NOT NULL,
        practice VARCHAR(80) NOT NULL,
        message TEXT NOT NULL,
        locale VARCHAR(10) NOT NULL DEFAULT "en",
        ip_prefix VARCHAR(64)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'
);
$pdo->exec(
    'CREATE TABLE IF NOT EXISTS form_hits (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ip_hash CHAR(64) NOT NULL,
        ts INT NOT NULL,
        INDEX idx_ip_ts (ip_hash, ts)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'
);

// --------------------------------------------------------------------------
// 3) Rate limit — N envíos por ventana y por IP. Se guarda un HASH de la IP,
//    nunca la IP en claro (salt en config.php).
// --------------------------------------------------------------------------
$now     = time();
$ipHash  = hash('sha256', ($cfg['ip_salt'] ?? '') . $ip);
$windowStart = $now - $RATE_LIMIT_WINDOW;

$pdo->prepare('DELETE FROM form_hits WHERE ts < ?')->execute([$windowStart]);
$stmt = $pdo->prepare('SELECT COUNT(*) AS c FROM form_hits WHERE ip_hash = ? AND ts >= ?');
$stmt->execute([$ipHash, $windowStart]);
if ((int)$stmt->fetch()['c'] >= $RATE_LIMIT_MAX) {
    error_log('contact.php: rate limited ip=' . anonymise($ip));
    respond(429, ['detail' => 'Too many submissions']);
}
$pdo->prepare('INSERT INTO form_hits (ip_hash, ts) VALUES (?, ?)')->execute([$ipHash, $now]);

// --------------------------------------------------------------------------
// 4) Validación — toda cadena con longitud máxima explícita.
// --------------------------------------------------------------------------
$errors = [];

$company = trim((string)($data['company'] ?? ''));
if ($company === '' || mb_strlen($company) > 120 || has_control_chars($company)) {
    $errors[] = 'company';
}

$email = trim((string)($data['email'] ?? ''));
if ($email === '' || mb_strlen($email) > 254 || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'email';
}

$practice = (string)($data['practice'] ?? '');
if (!in_array($practice, $ALLOWED_PRACTICES, true)) {
    $errors[] = 'practice';
}

$message = trim((string)($data['message'] ?? ''));
if (mb_strlen($message) < 20 || mb_strlen($message) > 4000 || has_control_chars($message)) {
    $errors[] = 'message';
}

$locale = (string)($data['locale'] ?? 'en');
if (!in_array($locale, $SUPPORTED_LOCALES, true)) {
    $locale = 'en';
}

if ($errors) {
    respond(422, ['detail' => 'Invalid fields', 'fields' => $errors]);
}

// --------------------------------------------------------------------------
// 5) Guardar el lead
// --------------------------------------------------------------------------
try {
    $stmt = $pdo->prepare(
        'INSERT INTO leads (company, email, practice, message, locale, ip_prefix)
         VALUES (?, ?, ?, ?, ?, ?)'
    );
    $stmt->execute([$company, $email, $practice, $message, $locale, anonymise($ip)]);
} catch (Throwable $e) {
    error_log('contact.php: INSERT falló: ' . $e->getMessage());
    respond(500, ['detail' => 'Server error']);
}

// --------------------------------------------------------------------------
// 6) Aviso por correo — texto plano. El asunto solo usa la práctica (lista
//    blanca). Las cabeceras se sanean contra inyección de CR/LF.
// --------------------------------------------------------------------------
$mailTo   = (string)($cfg['mail_to'] ?? '');
$mailFrom = (string)($cfg['mail_from'] ?? '');
if ($mailTo !== '' && $mailFrom !== '') {
    // El correo del prospecto ya está validado, pero se recorta cualquier
    // salto de línea antes de meterlo en Reply-To por doble seguridad.
    $replyTo = preg_replace('/[\r\n]+/', ' ', $email);
    $subject = '[Website] ' . $practice;              // práctica = lista blanca

    $body = "New enquiry from the website\n\n"
          . "Company:  {$company}\n"
          . "Email:    {$email}\n"
          . "Practice: {$practice}\n"
          . "Language: {$locale}\n\n"
          . "Problem:\n{$message}\n";

    $headers = implode("\r\n", [
        'From: ' . $mailFrom,
        'Reply-To: ' . $replyTo,
        'Content-Type: text/plain; charset=utf-8',
        'X-Mailer: datarahub-contact',
    ]);

    // El envelope-from (-f) mejora la entrega y el SPF en cPanel.
    $ok = @mail($mailTo, $subject, $body, $headers, '-f' . $mailFrom);
    if (!$ok) {
        // El lead ya quedó guardado; el correo es best-effort.
        error_log('contact.php: mail() no pudo enviar (lead guardado igual)');
    }
}

// Log sin PII: ni el correo completo ni el cuerpo del mensaje.
error_log(sprintf(
    'contact.php: lead stored practice=%s locale=%s domain=%s ip=%s',
    $practice, $locale, substr(strrchr($email, '@') ?: '@', 1), anonymise($ip)
));

respond(201, ['status' => 'ok']);
