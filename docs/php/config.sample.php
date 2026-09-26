<?php
/**
 * Copia este archivo a config.php EN EL SERVIDOR y llena los valores.
 * config.php NO se sube al repositorio (está en .gitignore).
 *
 * Lo ÚNICO obligatorio para que el formulario envíe correo es mail_from y
 * mail_to. La base de datos (MySQL) es OPCIONAL: si dejas los campos db_*
 * vacíos, solo se envía el correo; si los llenas, además se guarda cada lead.
 */

return [
    // --- Correo (OBLIGATORIO) — buzón del dominio, cPanel → Cuentas de correo ---
    // mail_from DEBE ser un buzón REAL de @datarahub.com para que Neubox lo
    // entregue con buen SPF/DKIM. mail_to es donde quieres recibir el aviso.
    'mail_from' => 'hola@datarahub.com',
    'mail_to'   => 'hola@datarahub.com',

    // --- MySQL (OPCIONAL) — déjalo vacío para "solo correo" ---
    // Cuando quieras GUARDAR los leads, llénalo con lo de cPanel → MySQL Databases
    // (usuario y base suelen llevar el prefijo de tu cuenta, p. ej. "datarahu_leads").
    'db_host' => '',
    'db_name' => '',
    'db_user' => '',
    'db_pass' => '',

    // --- Rate limit ---
    'rate_limit_max'    => 5,      // envíos permitidos por ventana y por IP
    'rate_limit_window' => 3600,   // segundos (1 hora)

    // --- Privacidad ---
    // Cadena larga y aleatoria para hashear la IP del rate limit (nunca se
    // guarda la IP en claro). Genera una con:  openssl rand -hex 32
    'ip_salt' => 'CAMBIA_ESTO_POR_UNA_CADENA_ALEATORIA_LARGA',
];
