<?php
/**
 * Datara Hub — endpoint de contacto para hosting cPanel (Neubox).
 * ------------------------------------------------------------------
 * Reemplazo directo de POST /api/contact (api/main.py) para cuando el sitio
 * viva en Neubox con PHP + correo del dominio, sin proceso Python.
 *
 * El frontend (app.js) manda un JSON a este archivo y espera:
 *   2xx  -> enviado           400  -> demasiado rápido (trampa de tiempo)
 *   422  -> campos inválidos   429  -> demasiados envíos (rate limit)
 * Para usarlo, en app.js:  var API_ENDPOINT = "/contact.php";
 *
 * BASE DE DATOS OPCIONAL
 * ----------------------
 * El correo funciona SIN MySQL. Si en config.php llenas db_host/db_name/db_user,
 * además se guarda cada lead en la tabla `leads` (se crea sola). Si no, solo
 * se envía el correo. El rate-limit usa un archivo temporal, no la base.
 *
 * Controles (AAIF security-standard): honeypot + trampa de tiempo + rate limit
 * + validación con longitudes máximas + práctica en lista blanca + IP anonimizada
 * + correo en texto plano con cabeceras sin CR/LF. Secretos en config.php.
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

$MIN_FILL_SECONDS  = 3;
$MAX_BODY_BYTES    = 16 * 1024;
$RATE_LIMIT_MAX    = (int)($cfg['rate_limit_max'] ?? 5);
$RATE_LIMIT_WINDOW = (int)($cfg['rate_limit_window'] ?? 3600);

// ¿Hay base de datos configurada? Si no, el guardado se omite (el correo sigue).
$dbConfigured = !empty($cfg['db_host']) && !empty($cfg['db_name']) && !empty($cfg['db_user']);

// Debe coincidir EXACTO con los value="" de los <option> en index.html.
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
// Utilidades
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

/**
 * Rate limit basado en archivo temporal (sin base de datos). Guarda las marcas
 * de tiempo de cada IP (hasheada) en un archivo dentro del tmp del sistema.
 * Si no puede escribir el archivo, NO bloquea (mejor dejar pasar que romper).
 */
function rate_limited(string $ipHash, int $max, int $window): bool
{
    $dir = sys_get_temp_dir() . '/datarahub_rate';
    if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
    $file = $dir . '/' . $ipHash;
    $now = time();
    $cutoff = $now - $window;

    $fp = @fopen($file, 'c+');
    if ($fp === false) { return false; }
    @flock($fp, LOCK_EX);
    $raw = stream_get_contents($fp);
    $hits = [];
    foreach (explode("\n", (string)$raw) as $line) {
        $t = (int)trim($line);
        if ($t >= $cutoff) { $hits[] = $t; }
    }
    $blocked = count($hits) >= $max;
    if (!$blocked) { $hits[] = $now; }
    rewind($fp);
    ftruncate($fp, 0);
    fwrite($fp, implode("\n", $hits));
    fflush($fp);
    @flock($fp, LOCK_UN);
    fclose($fp);
    return $blocked;
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
if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {   // detrás del proxy de Neubox
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
// 3) Rate limit (archivo temporal, sin base de datos). Hash de la IP con salt.
// --------------------------------------------------------------------------
$ipHash = hash('sha256', ($cfg['ip_salt'] ?? '') . $ip);
if (rate_limited($ipHash, $RATE_LIMIT_MAX, $RATE_LIMIT_WINDOW)) {
    error_log('contact.php: rate limited ip=' . anonymise($ip));
    respond(429, ['detail' => 'Too many submissions']);
}

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
// 5) Guardar el lead — SOLO si hay base de datos configurada. Best-effort:
//    si la base falla, el correo se envía igual (no rompemos el envío).
// --------------------------------------------------------------------------
if ($dbConfigured) {
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
        $stmt = $pdo->prepare(
            'INSERT INTO leads (company, email, practice, message, locale, ip_prefix)
             VALUES (?, ?, ?, ?, ?, ?)'
        );
        $stmt->execute([$company, $email, $practice, $message, $locale, anonymise($ip)]);
    } catch (Throwable $e) {
        // La base es best-effort: se registra y se sigue al correo.
        error_log('contact.php: guardado en BD falló (el correo sigue): ' . $e->getMessage());
    }
}

// --------------------------------------------------------------------------
// 6) Aviso por correo — texto plano. Asunto solo con la práctica (lista blanca).
//    Cabeceras saneadas contra inyección de CR/LF.
// --------------------------------------------------------------------------
$mailTo   = (string)($cfg['mail_to'] ?? '');
$mailFrom = (string)($cfg['mail_from'] ?? '');
$mailSent = false;
if ($mailTo !== '' && $mailFrom !== '') {
    $replyTo = preg_replace('/[\r\n]+/', ' ', $email);   // anti header-injection
    $subject = '[Website] ' . $practice;                 // práctica = lista blanca

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

    $mailSent = @mail($mailTo, $subject, $body, $headers, '-f' . $mailFrom);
    if (!$mailSent) {
        error_log('contact.php: mail() no pudo enviar');
    }
}

// Log sin PII: ni el correo completo ni el cuerpo del mensaje.
error_log(sprintf(
    'contact.php: lead practice=%s locale=%s domain=%s stored=%s mailed=%s ip=%s',
    $practice, $locale, substr(strrchr($email, '@') ?: '@', 1),
    $dbConfigured ? 'try' : 'no', $mailSent ? 'yes' : 'no', anonymise($ip)
));

respond(201, ['status' => 'ok']);
